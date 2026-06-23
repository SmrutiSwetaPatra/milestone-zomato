import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import sqlite3
import logging
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

app = FastAPI(title="Zomato Restaurant Recommendation API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "data/zomato.db"

class RecommendationRequest(BaseModel):
    location: str
    budget: Optional[str] = None  # "low", "medium", "high"
    cuisine: Optional[str] = None
    min_rating: Optional[float] = 0.0
    additional_preferences: Optional[str] = None

class RecommendedRestaurant(BaseModel):
    restaurant_name: str = Field(description="Name of the restaurant")
    cuisine: str = Field(description="Cuisine type")
    rating: float = Field(description="Rating of the restaurant")
    estimated_cost: float = Field(description="Estimated cost for two")
    explanation: str = Field(description="A personalized explanation of why this restaurant fits the user's criteria, based on their preferences")

class LLMRecommendationResponse(BaseModel):
    recommendations: List[RecommendedRestaurant] = Field(description="Ranked list of top recommended restaurants")
    summary: str = Field(description="A brief summary wrapping up the choices")

def filter_restaurants(req: RecommendationRequest) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Use MAX() or GROUP BY to get distinct restaurants
    query = "SELECT name, location, cuisines, cost, MAX(rating) as rating FROM restaurants WHERE 1=1"
    params = []
    
    if req.location:
        query += " AND location LIKE ?"
        params.append(f"%{req.location}%")
        
    if req.min_rating and req.min_rating > 0:
        query += " AND rating >= ?"
        params.append(req.min_rating)
        
    if req.cuisine:
        query += " AND cuisines LIKE ?"
        params.append(f"%{req.cuisine}%")
        
    if req.budget:
        budget = req.budget.lower()
        if budget == "low":
            query += " AND cost <= 500"
        elif budget == "medium":
            query += " AND cost > 500 AND cost <= 1000"
        elif budget == "high":
            query += " AND cost > 1000"

    query += " GROUP BY LOWER(TRIM(name)) ORDER BY rating DESC LIMIT 15"
    
    logger.info(f"Executing query: {query} with params: {params}")
    
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        return results
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()

def get_llm_recommendations(filtered_data: List[Dict[str, Any]], req: RecommendationRequest) -> LLMRecommendationResponse:
    if not os.environ.get("GROQ_API_KEY"):
        logger.error("GROQ_API_KEY is not set.")
        raise HTTPException(status_code=500, detail="LLM configuration error (missing GROQ_API_KEY in environment)")
        
    # Phase 3: LangChain & Groq integration
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)
    parser = PydanticOutputParser(pydantic_object=LLMRecommendationResponse)
    
    prompt = PromptTemplate(
        template="""You are an expert AI restaurant recommendation assistant.
Based on the user's preferences and the list of available filtered restaurants, recommend UP TO 5 best matching restaurants. Rank them in order of best match.
CRITICAL: You must return strictly UNIQUE and DISTINCT restaurants. Do not recommend the same restaurant more than once.
If there are fewer than 5 restaurants in the provided list, only return those available. DO NOT hallucinate or invent restaurants to reach 5. Only choose from the provided list.

User Preferences:
- Location: {location}
- Budget: {budget}
- Cuisine: {cuisine}
- Minimum Rating: {min_rating}
- Additional Preferences: {additional_preferences}

Available Restaurants (Filtered Data):
{restaurant_data}

{format_instructions}""",
        input_variables=["location", "budget", "cuisine", "min_rating", "additional_preferences", "restaurant_data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    
    try:
        # Convert filtered data to a clean string for the prompt
        restaurant_str = json.dumps(filtered_data, indent=2)
        
        response = chain.invoke({
            "location": req.location,
            "budget": req.budget or "Any",
            "cuisine": req.cuisine or "Any",
            "min_rating": req.min_rating or "Any",
            "additional_preferences": req.additional_preferences or "None",
            "restaurant_data": restaurant_str
        })
        return response
    except Exception as e:
        logger.error(f"LLM Generation failed: {e}")
        raise Exception(f"Failed to generate AI recommendations: {str(e)}")

@app.post("/recommend")
async def recommend_restaurants(request: RecommendationRequest):
    logger.info(f"Received recommendation request: {request}")
    
    # Phase 2: Data Filtering Engine
    filtered_data = filter_restaurants(request)
    
    if not filtered_data:
        return {
            "status": "success",
            "message": "No restaurants found matching your exact criteria. Please try relaxing your constraints (e.g., lower rating, different budget).",
            "data": []
        }
        
    # Phase 3: LLM Reasoning
    try:
        llm_result = get_llm_recommendations(filtered_data, request)
        return {
            "status": "success",
            "data": {
                "recommendations": [r.dict() for r in llm_result.recommendations],
                "summary": llm_result.summary
            }
        }
    except Exception as e:
        logger.error(f"Fallback to basic filtering due to LLM error: {e}")
        # Graceful fallback to basic filtered data if LLM fails (e.g. no API key)
        return {
            "status": "partial_success",
            "message": f"Found {len(filtered_data)} candidate restaurants, but AI explanation failed. Returning raw filtered data. Error: {str(e)}",
            "data": filtered_data[:5] # return top 5
        }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/locations")
async def get_locations():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT location FROM restaurants WHERE location IS NOT NULL AND location != '' ORDER BY location")
        rows = cursor.fetchall()
        locations = [row["location"].strip() for row in rows if row["location"]]
        # Deduplicate after stripping just in case
        locations = sorted(list(set(locations)))
        return {"status": "success", "data": locations}
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

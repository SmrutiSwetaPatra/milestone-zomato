import asyncio
import json
from main import RecommendationRequest, filter_restaurants, get_llm_recommendations

def predict():
    print("Initializing Prediction Request...")
    req = RecommendationRequest(
        location="Bellandur",
        budget="high", # 1500 falls into high in our logic (cost > 1000)
        min_rating=4.2,
        additional_preferences="Max budget is strictly 1500 for two people."
    )
    
    print("Filtering database records...")
    filtered = filter_restaurants(req)
    print(f"Found {len(filtered)} candidate restaurants matching hard filters.")
    
    if len(filtered) == 0:
        print("No candidates found! Cannot predict.")
        return
        
    print("Sending candidate data to Groq LLM for intelligent prediction...")
    try:
        response = get_llm_recommendations(filtered, req)
        print("\n" + "="*50)
        print("LLM PREDICTION RESULTS")
        print("="*50)
        
        for i, rec in enumerate(response.recommendations, 1):
            print(f"{i}. {rec.restaurant_name} (Rating: {rec.rating}, Cost: {rec.estimated_cost})")
            print(f"   Cuisine: {rec.cuisine}")
            print(f"   Why: {rec.explanation}")
            print("-" * 50)
            
        print("\nSUMMARY:")
        print(response.summary)
        
    except Exception as e:
        print(f"Failed to get LLM prediction: {e}")

if __name__ == "__main__":
    predict()

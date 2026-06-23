# Edge Cases and Corner Scenarios

This document outlines potential edge cases and corner scenarios that the AI-Powered Restaurant Recommendation System must handle to ensure a robust and reliable user experience.

## 1. Data Ingestion & Preprocessing

* **Missing Critical Data:** A restaurant in the dataset is missing a crucial field such as `cost`, `rating`, or `cuisine`.
  * *Mitigation:* The data preprocessor should handle null values by either dropping incomplete rows (if they lack critical identity fields) or assigning default values (e.g., "Not Rated", "Cost Unknown").
* **Inconsistent Text Formatting:** Locations or cuisines have inconsistent capitalization, spacing, or spelling (e.g., "New Delhi", "new delhi", "Delhi").
  * *Mitigation:* Apply text normalization (lowercasing, stripping whitespace) during the data loading phase.
* **Dataset Unavailability:** The Hugging Face dataset is temporarily unavailable or the download times out.
  * *Mitigation:* Keep a cached fallback version of the dataset locally, and implement retry logic for the ingestion script.

## 2. User Input & Hard Filtering

* **The "Zero Match" Scenario (Over-Constrained):** A user asks for an impossible combination, such as a 5-star fine-dining restaurant with a budget of "Low" in a tiny neighborhood.
  * *Mitigation:* The filtering engine should detect when zero records match and gracefully inform the user, suggesting they relax their constraints (e.g., "We couldn't find any 5-star places for a low budget. How about these highly-rated medium budget places?").
* **The "Too Many Matches" Scenario (Under-Constrained):** A user provides almost no constraints (e.g., Location: Delhi, Budget: Any, Cuisine: Any), returning thousands of results.
  * *Mitigation:* Implement a default sorting mechanism (e.g., sort by highest rating or number of reviews) and strictly cap the number of results sent to the LLM (e.g., top 15) to prevent context window overflow.
* **Ambiguous or Vague Preferences:** The user types "I want something hot" in the additional preferences field.
  * *Mitigation:* Pass this context to the LLM. The LLM is excellent at interpreting "hot" as "spicy" and can look for restaurants known for spicy cuisines like Mexican or Sichuan.

## 3. LLM Integration & Reasoning Layer

* **Context Window Limit Exceeded:** The filtered list of restaurants is too large, causing the prompt to exceed the Groq model's context window.
  * *Mitigation:* Strictly enforce a maximum number of candidate restaurants (e.g., 10-20) passed into the prompt.
* **LLM Hallucinations (Inventing Restaurants):** The LLM recommends a restaurant that does not exist in the provided context, or invents details about it.
  * *Mitigation:* Use strict prompt engineering instructions: *"ONLY recommend restaurants from the provided JSON list. DO NOT invent details."* Ground the LLM firmly in the context.
* **Output Parsing Failures:** The LLM fails to return valid JSON, or the JSON schema is broken, causing the backend parser to crash.
  * *Mitigation:* Use an LLM output parser with retry logic. If the LLM returns broken JSON, prompt it again to fix the formatting, or use a robust JSON extraction regex as a fallback.
* **Groq API Timeout or Rate Limiting:** The Groq API is down, heavily loaded, or rate-limiting requests.
  * *Mitigation:* Implement exponential backoff and retry mechanisms. If the LLM layer completely fails, gracefully degrade by returning the hard-filtered list directly to the user without the AI-generated explanations.

## 4. UI / Presentation Layer

* **Long Inference Times:** The LLM takes too long to generate a response, leaving the user staring at a blank screen.
  * *Mitigation:* Implement skeleton loaders, progress bars, or streaming text to indicate that the AI is "thinking" and keep the user engaged.
* **Special Characters & Localization:** Restaurant names or AI explanations contain unexpected Unicode characters or emojis.
  * *Mitigation:* Ensure the frontend and API layers properly encode and decode UTF-8.

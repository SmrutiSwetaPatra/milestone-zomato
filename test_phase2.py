from main import RecommendationRequest, filter_restaurants

def run_test():
    # Test 1: Banashankari, Chinese, Medium budget, high rating
    req1 = RecommendationRequest(
        location="Banashankari",
        budget="medium",
        cuisine="Chinese",
        min_rating=4.0
    )
    print("--- Test 1 ---")
    res1 = filter_restaurants(req1)
    for r in res1:
        print(f"{r['name']} | {r['location']} | {r['cuisines']} | Rating: {r['rating']} | Cost: {r['cost']}")
        
    # Test 2: Indiranagar, low budget
    req2 = RecommendationRequest(
        location="Indiranagar",
        budget="low",
        min_rating=4.2
    )
    print("\n--- Test 2 ---")
    res2 = filter_restaurants(req2)
    for r in res2:
        print(f"{r['name']} | {r['location']} | {r['cuisines']} | Rating: {r['rating']} | Cost: {r['cost']}")

if __name__ == "__main__":
    run_test()

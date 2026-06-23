import pandas as pd
from datasets import load_dataset

def main():
    print("Loading Zomato dataset from Hugging Face...")
    try:
        dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
        print("Dataset loaded successfully!")
        
        # Check available splits
        print("Splits:", dataset.keys())
        
        # Usually datasets have a 'train' split
        df = pd.DataFrame(dataset['train'])
        
        print(f"\nOriginal dataset shape: {df.shape}")
        print("\nColumns:")
        for col in df.columns:
            print(f" - {col}")
            
        print("\nSample Data (first 2 rows):")
        print(df.head(2).to_string())
        
    except Exception as e:
        print(f"Error loading dataset: {e}")

if __name__ == "__main__":
    main()

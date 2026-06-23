import os
import pandas as pd
import sqlite3
from datasets import load_dataset

def clean_cost(cost_str):
    if pd.isna(cost_str):
        return None
    if isinstance(cost_str, str):
        # Remove commas and non-numeric characters if any
        cost_str = cost_str.replace(',', '')
        try:
            return float(cost_str)
        except ValueError:
            return None
    return cost_str

def clean_rate(rate_str):
    if pd.isna(rate_str):
        return None
    if isinstance(rate_str, str):
        # rate comes as "4.1/5" or "NEW" or "-"
        if '/' in rate_str:
            try:
                return float(rate_str.split('/')[0].strip())
            except ValueError:
                return None
    return None

def main():
    print("Loading Zomato dataset from Hugging Face...")
    try:
        dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
        df = pd.DataFrame(dataset['train'])
        
        # Select required columns
        columns_to_keep = [
            'name', 'location', 'cuisines', 
            'approx_cost(for two people)', 'rate'
        ]
        
        # Verify columns exist
        missing_cols = [c for c in columns_to_keep if c not in df.columns]
        if missing_cols:
            print(f"Missing columns: {missing_cols}")
            return
            
        df = df[columns_to_keep].copy()
        
        # Rename for easier use
        df.rename(columns={
            'approx_cost(for two people)': 'cost',
            'rate': 'rating'
        }, inplace=True)
        
        print("Preprocessing data...")
        # Drop rows where essential columns are null
        df.dropna(subset=['name', 'location', 'cuisines'], inplace=True)
        
        # Clean cost and rating
        df['cost'] = df['cost'].apply(clean_cost)
        df['rating'] = df['rating'].apply(clean_rate)
        
        # Drop rows with null cost or rating
        df.dropna(subset=['cost', 'rating'], inplace=True)
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Save to SQLite
        db_path = 'data/zomato.db'
        print(f"Saving cleaned data ({len(df)} rows) to SQLite database at {db_path}...")
        
        conn = sqlite3.connect(db_path)
        df.to_sql('restaurants', conn, if_exists='replace', index=False)
        
        # Create indices for faster querying
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_location ON restaurants(location)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rating ON restaurants(rating)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cost ON restaurants(cost)")
        conn.commit()
        conn.close()
        
        print("Data ingestion and storage completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

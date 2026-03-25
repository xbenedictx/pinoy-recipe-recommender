import sqlite3
import pandas as pd
import ast  # to safely convert string back to list later if needed

def init_db():
    conn = sqlite3.connect('recipes.db')
    
    # Read the CSV safely
    df = pd.read_csv('data/filipino_recipes.csv', 
                     quoting=1, 
                     encoding='utf-8')
    
    print(f"Loaded {len(df)} recipes from CSV")
    
    # Clean and prepare columns
    df['ingredients'] = df['ingredients'].astype(str).str.lower().str.strip()
    
    # Create ingredients_list as string (comma-separated) instead of Python list
    df['ingredients_list'] = df['ingredients'].str.split(',').apply(
        lambda x: ','.join([ing.strip() for ing in x]) if isinstance(x, list) else ''
    )
    
    # Save to SQLite (now all columns are strings or numbers - no lists)
    df.to_sql('recipes', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"✅ Database initialized successfully with {len(df)} recipes!")

if __name__ == "__main__":
    init_db()
import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('recipes.db')
    df = pd.read_csv('data/filipino_recipes.csv')
    
    # Convert ingredients to list for easier matching
    df['ingredients_list'] = df['ingredients'].str.lower().str.split(',')
    
    df.to_sql('recipes', conn, if_exists='replace', index=False)
    conn.close()
    print("Database initialized with", len(df), "recipes!")

if __name__ == "__main__":
    init_db()
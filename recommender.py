import sqlite3
import pandas as pd

def get_recommendations(user_ingredients=None, max_time=60, limit=8):
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql_query("SELECT * FROM recipes", conn)
    conn.close()
    
    # Simple scoring
    if user_ingredients:
        user_set = set([ing.strip().lower() for ing in user_ingredients])
        df['match_score'] = df['ingredients_list'].apply(
            lambda x: len(user_set.intersection(set(x))) if isinstance(x, list) else 0
        )
        df = df.sort_values('match_score', ascending=False)
    
    # Filter by time
    df = df[df['total_time'] <= max_time]
    
    return df.head(limit)
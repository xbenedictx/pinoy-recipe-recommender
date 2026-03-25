import sqlite3
import pandas as pd

def get_recommendations(user_ingredients=None, max_time=60, limit=8):
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql_query("SELECT * FROM recipes", conn)
    conn.close()
    
    if df.empty:
        return pd.DataFrame()

    # Calculate match score properly
    if user_ingredients:
        user_set = {ing.strip().lower() for ing in user_ingredients}
        
        def calculate_match(ing_list_str):
            if not ing_list_str or ing_list_str == '':
                return 0
            ing_set = {ing.strip().lower() for ing in str(ing_list_str).split(',')}
            return len(user_set.intersection(ing_set))
        
        df['match_score'] = df['ingredients_list'].apply(calculate_match)
        df = df.sort_values('match_score', ascending=False)
    
    # Apply time filter
    df = df[df['total_time'] <= max_time].copy()
    
    # Reset index for clean display
    df = df.reset_index(drop=True)
    
    return df.head(limit)
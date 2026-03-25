import streamlit as st
import pandas as pd
from recommender import get_recommendations

st.set_page_config(page_title="Pinoy Recipe Recommender", page_icon="🍲", layout="centered")

st.title("🍲 Pinoy Recipe Recommender")
st.markdown("**What’s in your kusina?** Get Filipino recipe recommendations instantly!")

# Sidebar
st.sidebar.header("Filters")
max_time = st.sidebar.slider("Maximum Total Time (minutes)", 15, 180, 60)

all_ingredients = [
    "chicken", "pork", "beef", "garlic", "onion", "soy sauce", "vinegar", "ginger",
    "tamarind", "tomato", "eggplant", "okra", "string beans", "rice", "noodles",
    "carrots", "cabbage", "potato", "banana ketchup", "peanut butter"
]

selected_ingredients = st.sidebar.multiselect(
    "Ingredients you have:", 
    options=all_ingredients,
    default=["chicken", "garlic", "soy sauce"]
)

if st.sidebar.button("🔍 Recommend Recipes", type="primary"):
    with st.spinner("Finding the best matches..."):
        results = get_recommendations(selected_ingredients, max_time)
    
    if results.empty:
        st.warning("No recipes found with your current filters. Try removing some ingredients or increasing time.")
    else:
        st.success(f"Found {len(results)} delicious recommendations!")
        
        for _, row in results.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.subheader(row['recipe_name'])
                    st.caption(f"⏱️ {row['total_time']} mins | {row['difficulty']} | {row['meal_type']}")
                    st.write(row['description'])
                    st.write("**Ingredients:**", row['ingredients'])
                with col2:
                    st.metric("Match Score", f"{row.get('match_score', 'N/A')}")
                    st.button("View Recipe", key=row['recipe_name'])

# Home message
else:
    st.info("👈 Use the sidebar to select ingredients you have and click **Recommend Recipes**!")
    st.markdown("""
    ### Popular right now:
    - Chicken Adobo  
    - Sinigang na Baboy  
    - Pancit Bihon  
    - Halo-Halo (dessert)
    """)

st.caption("Simple Data Pipeline Project | Filipino Cuisine 🍚")
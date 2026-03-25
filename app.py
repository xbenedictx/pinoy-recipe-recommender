import streamlit as st
import pandas as pd
from recommender import get_recommendations

st.set_page_config(page_title="Pinoy Recipe Recommender", page_icon="🍲", layout="centered")

st.title("🍲 Pinoy Recipe Recommender")
st.markdown("**What’s in your kusina?** Get Filipino recipe recommendations instantly!")

# Sidebar Filters
st.sidebar.header("Filters")

max_time = st.sidebar.slider("Maximum Total Time (minutes)", 15, 180, 60)

all_ingredients = [
    "chicken", "pork", "beef", "garlic", "onion", "soy sauce", "vinegar", "ginger",
    "tamarind", "tomato", "eggplant", "okra", "string beans", "rice", "noodles",
    "carrots", "cabbage", "potato", "banana ketchup", "peanut butter", "calamansi"
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
        
        for i, row in results.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.subheader(row['recipe_name'])
                    st.caption(f"⏱️ {row['total_time']} mins | {row['difficulty']} | {row['meal_type']}")
                    st.write(row['description'])
                    st.write("**Ingredients:**", row['ingredients'])
                
                with col2:
                    score = int(row.get('match_score', 0))
                    total_selected = len(selected_ingredients) if selected_ingredients else 1
                    st.metric("Match Score", f"{score}/{total_selected}")
                    
                    # Improved button with expander
                    if st.button("View Full Recipe", key=f"view_{i}"):
                        with st.expander(f"📖 Full Recipe: {row['recipe_name']}", expanded=True):
                            st.markdown("### Ingredients")
                            st.write(row['ingredients'])
                            st.markdown("### Description")
                            st.write(row['description'])
                            st.markdown("### Instructions")
                            st.info("🔪 Full step-by-step instructions will be added soon! "
                                    "For now, you can follow the description and common cooking knowledge.")
                            st.caption(f"Difficulty: {row['difficulty']} • Time: {row['total_time']} mins")

else:
    st.info("👈 Use the sidebar to select ingredients you have and click **Recommend Recipes**!")
    st.markdown("""
    ### Popular right now:
    - Chicken Adobo  
    - Sinigang na Baboy  
    - Pancit Bihon  
    - Halo-Halo  
    - Pork Sisig
    """)

st.caption("Simple Data Pipeline Project | Filipino Cuisine 🍚")
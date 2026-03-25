import streamlit as st
from recommender import get_recommendations

st.set_page_config(page_title="Pinoy Recipe Recommender", page_icon="🍲", layout="centered")

st.title("🍲 Pinoy Recipe Recommender")
st.markdown("**What's in your kusina?** Get Filipino recipe recommendations instantly!")

# Sidebar Filters
st.sidebar.header("Filters")

max_time = st.sidebar.slider("Maximum Total Time (minutes)", 15, 180, 90)

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

instructions = {
    "Chicken Adobo": "1. Marinate chicken with soy sauce, garlic, and vinegar.\n2. Brown the chicken in oil.\n3. Add marinade, bay leaves, peppercorns, and water.\n4. Simmer 35-45 mins until tender.\n5. Reduce sauce and serve with rice.",
    "Sinigang na Baboy": "1. Boil pork until tender.\n2. Add onion, tomato, and tamarind.\n3. Add vegetables (okra, eggplant, string beans).\n4. Season with fish sauce.",
    "Pancit Bihon": "1. Soak bihon noodles.\n2. Sauté garlic, onion, chicken.\n3. Add vegetables and broth.\n4. Mix in noodles until sauce absorbed.",
    "Halo-Halo": "1. Put fruits & beans in glass.\n2. Add shaved ice.\n3. Top with milk and ube ice cream.\n4. Mix well.",
    "Adobo Flakes": "1. Cook adobo until tender.\n2. Shred chicken.\n3. Fry until crispy.",
    "Lechon Kawali": "1. Boil pork belly.\n2. Cool and dry.\n3. Deep fry until crispy.",
    "Lumpia Shanghai": "1. Wrap pork mixture.\n2. Deep fry until golden.",
    "Pork Sisig": "1. Boil/grill pork.\n2. Chop finely.\n3. Sauté with onion, chili, calamansi & mayo.",
    "Kare-Kare": "1. Boil oxtail.\n2. Make peanut sauce.\n3. Add vegetables and simmer.",
    "Chicken Tinola": "1. Sauté ginger & garlic.\n2. Add chicken.\n3. Add green papaya and chili leaves.",
    "Arroz Caldo": "1. Sauté ginger.\n2. Add chicken and rice.\n3. Simmer until creamy.",
    "Beef Caldereta": "1. Brown beef.\n2. Add tomato sauce & liver spread.\n3. Simmer with potatoes & carrots.",
    "Pinakbet": "1. Sauté pork & bagoong.\n2. Add all vegetables.\n3. Simmer until cooked.",
    "Ginataang Gulay": "1. Sauté garlic & shrimp.\n2. Add coconut milk & vegetables.",
    "Pork Barbecue": "1. Marinate pork.\n2. Skewer and grill.",
    "Turon": "1. Wrap banana & jackfruit.\n2. Deep fry and roll in sugar."
}

# === RECOMMEND BUTTON ===
if st.sidebar.button("🔍 Recommend Recipes", type="primary"):
    with st.spinner("Finding the best matches..."):
        results = get_recommendations(selected_ingredients, max_time)
    st.session_state["results"] = results
    st.session_state["selected_ingredients"] = selected_ingredients
    # Clear any open recipe panels
    for key in list(st.session_state.keys()):
        if key.startswith("show_recipe_"):
            st.session_state[key] = False

# Show results if we have them
if "results" in st.session_state and not st.session_state["results"].empty:
    results = st.session_state["results"]
    total_ingredients = st.session_state.get("selected_ingredients", selected_ingredients)

    st.success(f"Found {len(results)} delicious recommendations! 🍲")

    for i, row in results.iterrows():
        state_key = f"show_recipe_{i}"
        if state_key not in st.session_state:
            st.session_state[state_key] = False

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.subheader(row['recipe_name'])
                st.caption(f"⏱️ {row['total_time']} mins | {row['difficulty']} | {row['meal_type']}")
                st.write(row['description'])
                st.write("**Ingredients:**", row['ingredients'])

            with col2:
                score = int(row.get('match_score', 0))
                total = len(total_ingredients) if total_ingredients else 1
                st.metric("Match Score", f"{score}/{total}")

                if st.button(f"📖 View Full Recipe - {row['recipe_name']}", key=f"btn_{i}"):
                    st.session_state[state_key] = not st.session_state[state_key]

        if st.session_state[state_key]:
            with st.expander(f"🔪 How to Cook: {row['recipe_name']}", expanded=True):
                st.markdown("### Ingredients")
                st.write(row['ingredients'])
                st.markdown("### Step-by-Step Instructions")
                st.write(instructions.get(row['recipe_name'], "Instructions coming soon."))
                st.caption("💡 Tip: Taste and adjust seasoning while cooking!")

elif "results" not in st.session_state:
    st.info("👈 Use the sidebar to select ingredients you have and click **Recommend Recipes**!")
    st.markdown("### Popular right now:")
    st.markdown("""
    - Chicken Adobo  
    - Sinigang na Baboy  
    - Pancit Bihon  
    - Halo-Halo  
    - Pork Sisig
    """)

else:
    st.warning("No recipes found. Try increasing time or selecting fewer ingredients.")

st.caption("Simple Data Pipeline Project | Filipino Cuisine 🍚")

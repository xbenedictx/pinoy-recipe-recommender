import pandas as pd

df = pd.read_csv('data/filipino_recipes.csv')
print("Total recipes:", len(df))
print(df.head())
# Add cleaning logic here if needed
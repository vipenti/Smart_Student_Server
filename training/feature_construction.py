import pandas as pd

# Read the CSV files into dataframes
prof_df = pd.read_csv("data/professor.csv")
guy_df = pd.read_csv("data/random_guy.csv")

# Combine the dataframes
combined_df = pd.concat([prof_df, guy_df])

# Shuffle the rows
shuffled_df = combined_df.sample(frac=1).reset_index(drop=True)

# Save the shuffled dataframe to a new CSV file
shuffled_df.to_csv("data/mixed.csv", index=False)

# Features

# Embeddings
# [NER] Named Entities Recognition and Disambiguation
# Topic Modelling
# Acoustic features?
# TODO: implement own model

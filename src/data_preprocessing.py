import pandas as pd
from sklearn.model_selection import train_test_split
import os

data_path = os.path.join("data", "phishing_dataset.csv")
df = pd.read_csv(data_path)

print(f"Loaded {len(df)} samples")

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
os.makedirs("data/processed", exist_ok=True)
train_df.to_csv("data/processed/train.csv", index=False)
test_df.to_csv("data/processed/test.csv", index=False)

print("Preprocessing complete.")

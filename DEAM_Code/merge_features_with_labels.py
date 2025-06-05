import pandas as pd
import os

# Paths
FEATURE_CSV = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/deam_features.csv"
ANNOTATION_CSV = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/annotations/static_annotations_averaged.csv"
OUTPUT_CSV = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/deam_dataset_merged.csv"

# Load audio features
df_feat = pd.read_csv(FEATURE_CSV)

# Load mood annotations
df_labels = pd.read_csv(ANNOTATION_CSV)

# Add .mp3 extension to annotation filenames to match feature filenames
df_labels["filename"] = df_labels["song_id"].astype(str).str.zfill(3) + ".mp3"

# Merge on filename
df = pd.merge(df_feat, df_labels, on="filename")

# Optional: drop unused columns like song_id
df.drop(columns=["song_id"], inplace=True)

# Save
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Merged dataset saved to: {OUTPUT_CSV}")
print(f"🎧 Total rows: {len(df)}")

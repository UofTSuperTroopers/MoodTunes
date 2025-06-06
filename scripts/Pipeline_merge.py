import pandas as pd
import os

# Paths to your CSVs
MFCC_PATH = r"resources\mfcc_features.csv"
DEAM_PATH_1 = r"deam_data\deam_dataset_merged_complete.csv"


# Load Librosa MFCC features
mfcc_df = pd.read_csv(MFCC_PATH)
mfcc_df['song_id'] = mfcc_df['filename'].str.extract(r'(\d+)').astype(int)  # Extract numeric ID

# Load DEAM data 
deam_df = pd.read_csv(DEAM_PATH_1)

# Merge on song ID
merged_df = pd.merge(mfcc_df, deam_df, on='song_id', how='inner')

# Optional: save to file
merged_df.to_csv("merged_mfcc_deam.csv", index=False)

print("✅ Merged dataset shape:", merged_df.shape)

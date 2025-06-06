import pandas as pd

# Reload the updated features and label files
features_path = "deam_features.csv"
labels_path = "annotations/static_annotations_averaged.csv"

# Read both datasets
df_features = pd.read_csv(features_path)
df_labels = pd.read_csv(labels_path)

# Format song_id to filename in label file
df_labels["filename"] = df_labels["song_id"].astype(str).str.zfill(3) + ".mp3"

# Merge features with labels
df_merged = pd.merge(df_features, df_labels, on="filename")

# Drop song_id if no longer needed
df_merged.drop(columns=["song_id"], inplace=True)

# Save the merged dataset
merged_output = "deam_dataset_merged_complete.csv"
df_merged.to_csv(merged_output, index=False)


merged_output

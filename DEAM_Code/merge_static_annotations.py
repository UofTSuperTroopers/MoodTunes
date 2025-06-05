import pandas as pd
import os

# Input files — adjust the paths if needed
file1 = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv"
file2 = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_2000_2058.csv"
# Output file
output_file = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/annotations/static_annotations_averaged.csv"

# Load and clean both CSVs
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Strip column names of leading/trailing spaces
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Concatenate and select only necessary columns
merged = pd.concat([df1, df2], ignore_index=True)
merged = merged[["song_id", "valence_mean", "arousal_mean"]]

# Save to final CSV
merged.to_csv(output_file, index=False)

print(f"✅ Merged file saved to: {output_file}")
print(f"🎧 Total songs: {len(merged)}")

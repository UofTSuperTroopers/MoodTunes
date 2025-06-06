import os
import librosa
import numpy as np
import pandas as pd

# === Configuration ===
AUDIO_DIR = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/DEAM_audio/MEMD_audio"
EXISTING_CSV = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/deam_features.csv"
MISSING_CSV = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/missing_audio_files.csv"

# === Load missing filenames
df_missing = pd.read_csv(MISSING_CSV)
missing_files = df_missing["filename"].tolist()

# === Extract features
def extract_features(filename):
    path = os.path.join(AUDIO_DIR, filename)
    try:
        y, sr = librosa.load(path, sr=None)
        return {
            "filename": filename,
            "zcr": np.mean(librosa.feature.zero_crossing_rate(y)),
            "spectral_centroid": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "spectral_bandwidth": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
            "rolloff": np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
            "rmse": np.mean(librosa.feature.rms(y=y)),
            "tempo": librosa.beat.tempo(y=y, sr=sr)[0],
            "mfcc_mean": np.mean(librosa.feature.mfcc(y=y, sr=sr).T, axis=0).tolist()  # MFCCs as a list
        }
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return None

# === Process each file
features = []
for fname in missing_files:
    result = extract_features(fname)
    if result:
        flat = {**{k: v for k, v in result.items() if k != "mfcc_mean"},
                **{f"mfcc_{i+1}": mfcc for i, mfcc in enumerate(result["mfcc_mean"])}}
        features.append(flat)

# === Convert to DataFrame and append
df_new = pd.DataFrame(features)
df_existing = pd.read_csv(EXISTING_CSV)
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# === Save final dataset
df_combined.to_csv(EXISTING_CSV, index=False)
print(f"✅ Extracted features for {len(df_new)} missing files.")
print(f"🎯 Final total files: {len(df_combined)}")
print(f"📁 Updated: {EXISTING_CSV}")

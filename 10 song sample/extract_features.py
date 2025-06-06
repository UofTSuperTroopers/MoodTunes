import librosa
import pathlib
import soundfile as sf
import os
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm

# Parameters
AUDIO_DIR = r"C:\Users\a_lip\OneDrive\Desktop\module-challenges\MoodTunes\10 song sample"  # Folder where cropped clips go
SOURCE_DIR = r"C:\Users\a_lip\OneDrive\Desktop\module-challenges\MoodTunes\10 song sample"        # Folder with full .mp3 songs
SAMPLE_RATE = 22050
DURATION = 45  # seconds
N_MFCC = 13


def extract_music_pathnames():
    """Find all .mp3 files in SOURCE_DIR"""
    return glob.glob(os.path.join(SOURCE_DIR, "*.mp3"), recursive=True)


def cut_and_extract_features(duration=45.0, num_songs=10):
    """Extract features from the first `num_songs`, save audio snippets, and return MFCCs"""
    songs = extract_music_pathnames()[:num_songs]
    feature_list = []

    os.makedirs(AUDIO_DIR, exist_ok=True)

    for song in tqdm(songs, desc="Processing songs"):
        try:
            y, sr = librosa.load(song, sr=SAMPLE_RATE, duration=duration)

            # Save cropped audio
            out_path = os.path.join(AUDIO_DIR, pathlib.Path(song).name)
            sf.write(out_path, y, sr)
            print(f"✅ Wrote cropped audio: {out_path}")

            # Extract MFCCs
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
            mfcc_mean = np.mean(mfcc, axis=1)

            # Store features
            feature_dict = {"filename": pathlib.Path(song).name}
            for i in range(N_MFCC):
                feature_dict[f"mfcc_{i+1}"] = mfcc_mean[i]

            feature_list.append(feature_dict)

        except Exception as e:
            print(f"⚠️ Could not process {song}: {e}")

    return pd.DataFrame(feature_list)


def extract_mfcc_features():
    """Wrapper to extract and save MFCC features to CSV"""
    df = cut_and_extract_features(duration=DURATION, num_songs=10)
    csv_path = os.path.join(AUDIO_DIR, "mfcc_features.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ Saved MFCC features to: {csv_path}")


# Run this to generate your features
if __name__ == "__main__":
    extract_mfcc_features()

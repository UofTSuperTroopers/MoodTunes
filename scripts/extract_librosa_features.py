import librosa
import pathlib
import soundfile as sf
import os
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm

# Parameters
AUDIO_DIR = "audio_samples"  # Folder where cropped clips go
SOURCE_DIR = "audio_samples"        # Folder with full .mp3 songs
SAMPLE_RATE = 22050
DURATION = 45  # seconds
N_MFCC = 13


def extract_music_pathnames():
    """Find all .mp3 files in SOURCE_DIR"""
    return glob.glob(os.path.join(SOURCE_DIR, "*.mp3"), recursive=True)


def cut_and_extract_features(duration=DURATION, num_songs=10):
    """Extract features from the first `num_songs`, save audio snippets, and return MFCCs"""
    songs = extract_music_pathnames()[:num_songs]
    feature_list = []

    os.makedirs(AUDIO_DIR, exist_ok=True)

    for song in tqdm(songs, desc="Processing songs"):
        try:
            y, sr = librosa.load(song, sr=SAMPLE_RATE, duration=DURATION)

            # Save cropped audio
            out_path = os.path.join(AUDIO_DIR, pathlib.Path(song).name)
            sf.write(out_path, y, sr)
            print(f"✅ Wrote cropped audio: {out_path}")

            # Extract MFCCs
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
            mfcc_mean = np.mean(mfcc, axis=1)

            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
            mfcc_mean = np.mean(mfcc, axis=1)

            # New features
            chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
            spec_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spec_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
            spec_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr), axis=1)
            spec_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            zero_crossings = np.mean(librosa.feature.zero_crossing_rate(y))
            rms = np.mean(librosa.feature.rms(y=y))
            tempo = librosa.beat.tempo(y=y, sr=sr)[0]

            # Store features
            feature_dict = {"filename": pathlib.Path(song).name}
            for i in range(N_MFCC):
                feature_dict[f"mfcc_{i+1}"] = mfcc_mean[i]
            
            # Add new features
            for i, val in enumerate(chroma):
                feature_dict[f"chroma_{i+1}"] = val
                
            for i, val in enumerate(spec_contrast):
                feature_dict[f"spectral_contrast_{i+1}"] = val
               
            feature_dict["spectral_centroid"] = spec_centroid
            feature_dict["spectral_bandwidth"] = spec_bandwidth
            feature_dict["spectral_rolloff"] = spec_rolloff
            feature_dict["zero_crossing_rate"] = zero_crossings
            feature_dict["rms_energy"] = rms
            feature_dict["tempo"] = tempo
            
            feature_list.append(feature_dict)

        except Exception as e:
            print(f"⚠️ Could not process {song}: {e}")

    return pd.DataFrame(feature_list)


def extract_mfcc_features():
    """Wrapper to extract and save MFCC features to CSV"""
    df = cut_and_extract_features(duration=DURATION, num_songs=10)
    csv_path = os.path.join("../data/librosa_features", "mfcc_features.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ Saved MFCC features to: {csv_path}")


# Run this to generate your features
if __name__ == "__main__":
    extract_mfcc_features()

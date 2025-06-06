import os
import librosa
import pandas as pd

AUDIO_DIR = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/DEAM_audio\MEMD_audio"
OUTPUT_CSV = "C:/Users/a_lip/OneDrive/Desktop/Deam_Dataset/deam_features.csv"

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=30.0)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=3).mean(axis=1)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        zcr = librosa.feature.zero_crossing_rate(y).mean()
        rms = librosa.feature.rms(y=y).mean()
        return {
            "filename": os.path.basename(file_path),
            "tempo": tempo,
            "mfcc_1": mfccs[0],
            "mfcc_2": mfccs[1],
            "mfcc_3": mfccs[2],
            "spectral_centroid": spectral_centroid,
            "zero_crossing_rate": zcr,
            "rms_energy": rms,
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    rows = []
    print(f"Found {len(os.listdir(AUDIO_DIR))} files in {AUDIO_DIR}")

    for fname in os.listdir(AUDIO_DIR):
        if fname.endswith(".mp3"):
            file_path = os.path.join(AUDIO_DIR, fname)
            print(f"Processing {fname}...")
            features = extract_features(file_path)
            if features:
                rows.append(features)
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Saved features to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

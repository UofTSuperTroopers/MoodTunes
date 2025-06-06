import h5py
import glob
import pandas as pd
import os

def extract_track_summary(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            analysis = f['analysis/songs'][0]
            metadata = f['metadata/songs'][0]
            musicbrainz = f['musicbrainz/songs'][0]

            return {
                'track_id': analysis['track_id'].decode('utf-8'),
                'title': metadata['title'].decode('utf-8'),
                'artist_name': metadata['artist_name'].decode('utf-8'),
                'duration': analysis['duration'],
                'danceability': analysis['danceability'],
                'energy': analysis['energy'],
                'tempo': analysis['tempo'],
                'key': analysis['key'],
                'mode': analysis['mode'],
                'loudness': analysis['loudness'],
                'song_hotttnesss': metadata['song_hotttnesss'],
                'artist_hotttnesss': metadata['artist_hotttnesss'],
                'year': musicbrainz['year']
            }
    except Exception as e:
        print(f"❌ Error in {file_path}: {e}")
        return None

# --- CONFIGURATION ---
base_dir = 'MillionSongSubset'
output_csv = 'track_summary_features.csv'
# ----------------------

# 1. Find all .h5 files
h5_files = glob.glob(os.path.join(base_dir, '**/*.h5'), recursive=True)
print(f"🔍 Found {len(h5_files)} HDF5 files.")

# 2. Extract track summaries
all_tracks = []

for i, file_path in enumerate(h5_files):
    if i % 100 == 0:
        print(f"Processing file {i}/{len(h5_files)}")
    track_info = extract_track_summary(file_path)
    if track_info:
        all_tracks.append(track_info)

# 3. Save to CSV
df = pd.DataFrame(all_tracks)
df.to_csv(output_csv, index=False)
print(f"✅ Saved {len(df)} tracks to '{output_csv}'")

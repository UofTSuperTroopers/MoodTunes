import h5py
import numpy as np
import pandas as pd

def is_numeric_dtype(dtype):
    """Check if dtype is numeric (int or float)"""
    return np.issubdtype(dtype, np.number)

def extract_all_features(h5_file_path, output_csv_path):
    data = {}

    def recurse(name, obj):
        if isinstance(obj, h5py.Dataset):
            arr = obj[()]
            # Structured array
            if obj.dtype.names is not None:
                # Extract each field from the structured array
                for field in obj.dtype.names:
                    val = arr[0][field] if arr.shape else arr[field]
                    if isinstance(val, bytes):
                        val = val.decode('utf-8', errors='ignore')
                    data[f"{name}/{field}"] = val

            # Numeric array (int, float)
            elif is_numeric_dtype(obj.dtype):
                if arr.size == 0:
                    # Empty array, assign NaN
                    data[f"{name}_mean"] = np.nan
                    data[f"{name}_std"] = np.nan
                    data[f"{name}_len"] = 0
                else:
                    if arr.ndim == 1:
                        data[f"{name}_mean"] = np.mean(arr)
                        data[f"{name}_std"] = np.std(arr, ddof=0)  # ddof=0 to avoid warnings if length=1
                        data[f"{name}_len"] = arr.shape[0]
                    elif arr.ndim == 2:
                        mean_vals = np.mean(arr, axis=0)
                        std_vals = np.std(arr, axis=0, ddof=0)
                        for i in range(mean_vals.shape[0]):
                            data[f"{name}_mean_{i}"] = mean_vals[i]
                            data[f"{name}_std_{i}"] = std_vals[i]

            # Byte strings or other non-numeric types
            else:
                if arr.dtype.kind == 'S':
                    try:
                        strings = [x.decode('utf-8', errors='ignore') for x in arr]
                        data[f"{name}_all_strings"] = ", ".join(strings)
                    except Exception:
                        data[f"{name}_byte_count"] = arr.size
                else:
                    # Other non-numeric data: save size info
                    data[f"{name}_size"] = arr.size

    with h5py.File(h5_file_path, 'r') as f:
        f.visititems(recurse)

    # Save to CSV
    df = pd.DataFrame([data])
    df.to_csv(output_csv_path, index=False)
    print(f"✅ Features extracted to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    file_path = 'MillionSongSubset/A/P/E/TRAPEXA128F428B4F1.h5'
    output_csv = 'TRAPEXA128F428B4F1_features.csv'
    extract_all_features(file_path, output_csv)

import pandas as pd
from io import StringIO

# Paste your CSV data string (header + one row) here as a multi-line string
csv_data = """
analysis/bars_confidence_mean,analysis/bars_confidence_std,analysis/bars_confidence_len,analysis/bars_start_mean,analysis/bars_start_std,analysis/bars_start_len,analysis/beats_confidence_mean,analysis/beats_confidence_std,analysis/beats_confidence_len,analysis/beats_start_mean,analysis/beats_start_std,analysis/beats_start_len,analysis/sections_confidence_mean,analysis/sections_confidence_std,analysis/sections_confidence_len,analysis/sections_start_mean,analysis/sections_start_std,analysis/sections_start_len,analysis/segments_confidence_mean,analysis/segments_confidence_std,analysis/segments_confidence_len,analysis/segments_loudness_max_mean,analysis/segments_loudness_max_std,analysis/segments_loudness_max_len,analysis/segments_loudness_max_time_mean,analysis/segments_loudness_max_time_std,analysis/segments_loudness_max_time_len,analysis/segments_loudness_start_mean,analysis/segments_loudness_start_std,analysis/segments_loudness_start_len,analysis/segments_pitches_mean_0,analysis/segments_pitches_std_0,analysis/segments_pitches_mean_1,analysis/segments_pitches_std_1,analysis/segments_pitches_mean_2,analysis/segments_pitches_std_2,analysis/segments_pitches_mean_3,analysis/segments_pitches_std_3,analysis/segments_pitches_mean_4,analysis/segments_pitches_std_4,analysis/segments_pitches_mean_5,analysis/segments_pitches_std_5,analysis/segments_pitches_mean_6,analysis/segments_pitches_std_6,analysis/segments_pitches_mean_7,analysis/segments_pitches_std_7,analysis/segments_pitches_mean_8,analysis/segments_pitches_std_8,analysis/segments_pitches_mean_9,analysis/segments_pitches_std_9,analysis/segments_pitches_mean_10,analysis/segments_pitches_std_10,analysis/segments_pitches_mean_11,analysis/segments_pitches_std_11,analysis/segments_start_mean,analysis/segments_start_std,analysis/segments_start_len,analysis/segments_timbre_mean_0,analysis/segments_timbre_std_0,analysis/segments_timbre_mean_1,analysis/segments_timbre_std_1,analysis/segments_timbre_mean_2,analysis/segments_timbre_std_2,analysis/segments_timbre_mean_3,analysis/segments_timbre_std_3,analysis/segments_timbre_mean_4,analysis/segments_timbre_std_4,analysis/segments_timbre_mean_5,analysis/segments_timbre_std_5,analysis/segments_timbre_mean_6,analysis/segments_timbre_std_6,analysis/segments_timbre_mean_7,analysis/segments_timbre_std_7,analysis/segments_timbre_mean_8,analysis/segments_timbre_std_8,analysis/segments_timbre_mean_9,analysis/segments_timbre_std_9,analysis/segments_timbre_mean_10,analysis/segments_timbre_std_10,analysis/segments_timbre_mean_11,analysis/segments_timbre_std_11,analysis/songs/analysis_sample_rate,analysis/songs/audio_md5,analysis/songs/danceability,analysis/songs/duration,analysis/songs/end_of_fade_in,analysis/songs/energy,analysis/songs/idx_bars_confidence,analysis/songs/idx_bars_start,analysis/songs/idx_beats_confidence,analysis/songs/idx_beats_start,analysis/songs/idx_sections_confidence,analysis/songs/idx_sections_start,analysis/songs/idx_segments_confidence,analysis/songs/idx_segments_loudness_max,analysis/songs/idx_segments_loudness_max_time,analysis/songs/idx_segments_loudness_start,analysis/songs/idx_segments_pitches,analysis/songs/idx_segments_start,analysis/songs/idx_segments_timbre,analysis/songs/idx_tatums_confidence,analysis/songs/idx_tatums_start,analysis/songs/key,analysis/songs/key_confidence,analysis/songs/loudness,analysis/songs/mode,analysis/songs/mode_confidence,analysis/songs/start_of_fade_out,analysis/songs/tempo,analysis/songs/time_signature,analysis/songs/time_signature_confidence,analysis/songs/track_id,analysis/tatums_confidence_mean,analysis/tatums_confidence_std,analysis/tatums_confidence_len,analysis/tatums_start_mean,analysis/tatums_start_std,analysis/tatums_start_len,metadata/artist_terms_all_strings,metadata/artist_terms_freq_mean,metadata/artist_terms_freq_std,metadata/artist_terms_freq_len,metadata/artist_terms_weight_mean,metadata/artist_terms_weight_std,metadata/artist_terms_weight_len,metadata/similar_artists_all_strings,metadata/songs/analyzer_version,metadata/songs/artist_7digitalid,metadata/songs/artist_familiarity,metadata/songs/artist_hotttnesss,metadata/songs/artist_id,metadata/songs/artist_latitude,metadata/songs/artist_location,metadata/songs/artist_longitude,metadata/songs/artist_mbid,metadata/songs/artist_name,metadata/songs/artist_playmeid,metadata/songs/genre,metadata/songs/idx_artist_terms,metadata/songs/idx_similar_artists,metadata/songs/release,metadata/songs/release_7digitalid,metadata/songs/song_hotttnesss,metadata/songs/song_id,metadata/songs/title,metadata/songs/track_7digitalid,musicbrainz/artist_mbtags_all_strings,musicbrainz/artist_mbtags_count_mean,musicbrainz/artist_mbtags_count_std,musicbrainz/artist_mbtags_count_len,musicbrainz/songs/idx_artist_mbtags,musicbrainz/songs/year
0.16105298013245034,0.10539951041515597,151,126.3266469536424,72.65431801635441,151,0.4010043956043956,0.14443180063830718,455,126.88085226373626,72.97460092445095,455,0.505375,0.34984458603071167,8,124.10226499999999,84.96069365903786,8,0.5435526315789474,0.2525866827796671,912,-9.484201754385966,4.9397780863747816,912,0.053268201754385965,0.03955674564940316,912,-16.094457236842107,5.679268938113156,912,0.5962828947368416,0.33648209561925124,0.5034945175438594,0.3375173549348581,0.32876315789473676,0.2709206178689967,0.288760964912281,0.23056654548592848,0.38464473684210543,0.29796376739936886,0.30152960526315814,0.2838955500427133,0.2520263157894739,0.2382931248327716,0.2949013157894735,0.2588950989859995,0.2407280701754387,0.2385381708425455,0.32306907894736786,0.2961810335891271,0.25498464912280727,0.2652343423150516,0.3625855263157895,0.29677198134817157,123.73686228070176,70.55601748850397,912,47.318428728070245,4.954597326098256,6.98164912280701,51.783355906427175,28.293787280701736,32.652358844574124,0.7996622807017532,27.345471886776924,-28.937171052631548,28.845609555504893,-7.405957236842099,23.587756324933565,-0.21718311403508825,20.199476539607282,-1.9464714912280676,26.602521543797735,-8.256419956140347,17.598516386648537,3.205872807017543,22.449265462362277,-2.7001864035087686,14.611592922798303,-7.409627192982459,14.875228050339643,22050,0fc78443754d268b0d0484633ac628a3,0.0,257.4624,0.0,0.0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.344,-7.088,1,0.473,248.889,107.961,3,1.0,TRAPEXA128F428B4F1,0.426223076923077,0.13480203521544046,910,127.01983172527471,72.97396129877579,910,"cantonese pop, chinese music, soundtrack, female vocalist, pop, chinese, female, female vocals, idol, hong kong, cantonese, cpop, mandarin, china, bad taste, chinese pop, canto, canton music",0.5922030610553892,0.27358712317015865,18,0.6777311367123402,0.1580983788828225,18,"AR8QHU51187B9A3341, ARISRD71187FB57AE8, ARAMB6Q1187B99DE68, AR41E9U1187FB5573B, ARMO54H1187FB52A77, ARNNC731187FB55D14, ARL77521187B9A2655, ARQ2PMX1187FB38D62, ARHNL9K1187FB5730C, ARG0Q881187FB3A557, ARG1UAO1187FB55E50, AR8B3231187FB4A88D, ARN3X4T1187B99EA39, AR5GQ5I1187FB38769, AR5K75Y1187B9B5F7E, ARG74ES1187B9AFC8B, ARA8DDQ1187B9AE3A0, ARBIC7R1187B98AFAE, ARCABPN1187B9A2299, ARDZCBP11F4C845357, ARE3JFT1187FB589B6, ARHCB1C1187FB560A1, ARFERPC1187FB557F6, AR0730D1187FB5624D, AR126G61187B9B88A6, ARLD1PE1187FB5489F, ARXGWZP11F4C83C075, ARVMRVW1187FB392FF, AR0QS8F1187B9ADC96, ARW37071187FB53D11, ARXC5ZT11C8A42B81B, ARIRFES12131B4B6EF, ARCXFXM1187B995206, ARGP7WY1187FB45464, ARB12XW1187FB58A71, ARPDWU91187FB45185, AROI04B1187B991762, ARNHONS1187FB396CB, AR269TJ1187B99E1C5, AR3YA6F1187FB55106, ARVHT5F1187B9A2F2A, AREDCT51187B9A6DA6, AR8S6L11187B992C40, AR6PGIZ1187B9A4430, AR5SDVN1187B99176A, ARIZR2N1187FB583CB, ARX3UPJ1187FB567DA, ARKONHD1187FB39730, ARGOBGK1187FB58824, AR6WT5S1187B9929AB, ARI9SVN1187FB55AA8, ARMLH0C1187FB5400C, ARBVYDX1187FB40A09, ARBVIM21187FB520A2, AR83KGZ1187B9B2B38, AR4TU3B1187B99F335, ARAO0RA1187FB587F2, ARZG3LZ1187FB58A73, ARWENXU12454A2DE56, ARH5ANE1187B98E894, ARGVDLY1187B9A5481, ARPFC0M1187B9B969D, ARF9OK31187FB53B1A, AREMCUO1187FB54D2F, AR6G0HT11C8A415C9C, ARN6Q841187FB55D82, ARJ2D1X1187FB5660B, AR0E39C1187FB51C58, ARMPIH61187FB44227, ARI3JQ41187B9A27D2, ARJPRQQ1187B99AFA4, ARSW0NA1187B9B2127, ARLBRSK1187B9B0A5A, ARRUGT71187B98F222, AR3Y1IR1187FB4F445, AR4AWYZ1187B99C3CC, ARGJHTT1187FB56EF6, ARXNDB61187B9B2208, ARM35UF1187FB58AE1, ARRGFFD1187B9AF330, ARWY36G11A348EFDFC, ARUCX881187FB4E2D5, ARZ8IPU1187FB38846, AR825YT1187FB3956B, AR23SSG1187FB3AC75, AR54H421187FB5B26D, ARON1HK1187B9B89D5, AREUFRU1187FB49BEF, AR18AJW1187FB3F9FA, ARJ41O41187B9A0F53, ARHNRO71187FB58A7C, ARJVG7D1187B9B0AF8, AR08K181187FB568F0, ARW74FW1187FB554AD, ARI8PQM1187B99577F, AROONIV1187B998C67, ARGHFOP1187FB3964A, ARYPE7X1187FB58A6B, ARYP55K11C8A42BA63, ARL04XN1187FB5623A",,17528,0.49225313243508523,0.25680336879461524,ARGGEGH11F4C83C076,,,,,Miriam Yeung,59132,,0,0,Unlimited,166132,,SOUDGKB12A8C13EDA8,Yi Xing,1756482,,,,0,0,0
"""

# Use StringIO to simulate a file object for pandas
df = pd.read_csv(StringIO(csv_data))

print(df.head())

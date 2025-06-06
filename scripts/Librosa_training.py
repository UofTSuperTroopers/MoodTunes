import pandas as pd
import joblib  # or pickle
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
#from tensorflow.keras import layers, models

# 1. Load Librosa features
librosa_df = pd.read_csv("../data/librosa_features/mfcc_features.csv")

# 2. Drop any non-feature columns (e.g., filename)
X_librosa = librosa_df.drop(columns=["filename"])

# 3. Load your saved scaler and model (from DEAM training)
scaler = StandardScaler()
model = joblib.load("../resources/mood_model.pkl")  # This can be RF/XGB/etc.

# 4. Apply same scaling
X_scaled = scaler.fit_transform(X_librosa)

# 5. Predict mood
y_pred = model.predict(X_scaled)

# 6. Format predictions
pred_df = pd.DataFrame(y_pred, columns=["valence_pred", "arousal_pred"])
pred_df["filename"] = librosa_df["filename"]

# 7. Save to CSV
pred_df.to_csv("../data/librosa_features/librosa_mood_predictions.csv", index=False)
print("✅ Predicted moods saved.")

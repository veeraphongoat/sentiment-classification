import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
from tensorflow.keras.models import load_model
import librosa
import librosa.display
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle

# Set the backend to a non-interactive one
matplotlib.use('Agg')

# Load model and label encoder
model = load_model('mymodel_3.h5')
with open('Enc_labels.sav', 'rb') as file:
    lb = pickle.load(file)
scaler = StandardScaler()

# Feature extraction and audio processing functions
def zcr(data, frame_length=2048, hop_length=512):
    zcr = librosa.feature.zero_crossing_rate(y=data, frame_length=frame_length, hop_length=hop_length)
    return np.squeeze(zcr)

def rmse(data, frame_length=2048, hop_length=512):
    rmse = librosa.feature.rms(y=data, frame_length=frame_length, hop_length=hop_length)
    return np.squeeze(rmse)

def mfcc(data, sr, frame_length=2048, hop_length=512, flatten=True):
    mfcc_feature = librosa.feature.mfcc(y=data, sr=sr)
    return np.squeeze(mfcc_feature.T) if not flatten else np.ravel(mfcc_feature.T)

def extract_features(data, sr, frame_length=2048, hop_length=512):
    zcr_feat = zcr(data, frame_length, hop_length)
    rmse_feat = rmse(data, frame_length, hop_length)
    mfcc_feat = mfcc(data, sr, frame_length, hop_length)

    expected_mfcc_length = 13 * (1 + (len(data) - frame_length) // hop_length)
    if len(mfcc_feat) < expected_mfcc_length:
        mfcc_feat = np.pad(mfcc_feat, (0, expected_mfcc_length - len(mfcc_feat)), 'constant')
    elif len(mfcc_feat) > expected_mfcc_length:
        mfcc_feat = mfcc_feat[:expected_mfcc_length]

    features = np.hstack((zcr_feat, rmse_feat, mfcc_feat))
    expected_length = 2376
    if len(features) < expected_length:
        features = np.pad(features, (0, expected_length - len(features)), 'constant')
    elif len(features) > expected_length:
        features = features[:expected_length]

    return features

def predict_emotion(audio_data, sr):
    features = extract_features(audio_data, sr)
    features = features.reshape(1, -1)

    y_pred = model.predict(features)
    predicted_class = lb.classes_[np.argmax(y_pred)]
    return predicted_class

def deploy():
    st.markdown(
        """
        <style>
        .main {
            background-color: #F0F2F6;
        }
        .stApp {
            background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
            color: black;
        }
        .stApp header {
            background: linear-gradient(to right, violet, indigo, blue, green, yellow, orange, red);
        }
        .stApp .block-container {
            background: rgba(255, 255, 255, 0.8);
            padding: 2rem;
            border-radius: 10px;
        }
        .stApp .stButton>button {
            background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
            color: black;
        }
        h1, h2, h3, h4, h5, h6, .stApp .stMarkdown {
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Sentiment Classification from Audio")

    with st.sidebar:
        st.header("Instructions")
        st.write("""
        Upload an audio file in WAV format. The application will predict the emotion conveyed in the audio.
        """)
        st.header("Upload Audio File")
        uploaded_file = st.file_uploader("Choose an audio file...", type=["wav"])

    if uploaded_file is not None:
        audio_data, sr = librosa.load(uploaded_file, sr=None)
        emotion_label = predict_emotion(audio_data, sr)

        st.subheader(f"Predicted Emotion: {emotion_label}")

        col1, col2 = st.columns(2)
        with col1:
            st.header("Waveform")
            fig, ax = plt.subplots()
            librosa.display.waveshow(audio_data, sr=sr, color="purple", ax=ax)
            ax.set(xlabel='Time (s)', ylabel='Amplitude', title='Waveform')
            st.pyplot(fig)
            st.audio(uploaded_file)

        with col2:
            st.header("Spectrogram")
            fig, ax = plt.subplots()
            spec = librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max),
                                            sr=sr, x_axis='time', y_axis='log', ax=ax, cmap='coolwarm')
            ax.set(title='Spectrogram')
            st.pyplot(fig)

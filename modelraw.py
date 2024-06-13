import pyaudio
import wave
import time
import os
import librosa as lb
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

def record_audio():
    audio = pyaudio.PyAudio()

    filename = "recording.wav"
    filepath = os.path.join("C:\\Users\\sinha\\Desktop\\Voice-Biometric\\data\\akshat\\", filename)
    print("Recording...")
    
    # Start recording
    stream = audio.open(format=pyaudio.paInt16, channels=2,
                        rate=44100, input=True,
                        frames_per_buffer=1024)
    frames = []

    for i in range(0, int(44100 / 1024 * 3)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording")

    # Stop recording
    stream.stop_stream()
    stream.close()

    # Save the recording to a WAV file
    waveFile = wave.open(filepath, 'wb')
    waveFile.setnchannels(2)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(44100)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    audio.terminate()



    # Extract MFCCs from the recorded audio file
    audio, sample_rate = lb.load(filepath)
    mfccs = lb.feature.mfcc(y=audio, sr=sample_rate)
    mfccs_scaled = np.mean(mfccs.T, axis=0)

    # Load the authorized user's MFCC data from CSV file
    authorized_mfccs = pd.read_csv("C:\\Users\\sinha\\Desktop\\Voice-Biometric\\data\\mfccs.csv")

    # Scale the MFCCs using StandardScaler
    scaler = StandardScaler()
    mfccs_scaled = scaler.fit_transform(mfccs_scaled.reshape(1, -1))
    authorized_mfccs_scaled = scaler.transform(authorized_mfccs)

    # Train an MLPClassifier on the authorized user's MFCC data
    mlp = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000)
    mlp.fit(authorized_mfccs_scaled, np.ones((authorized_mfccs_scaled.shape[0],)))

    # Evaluate the recorded audio file using the MLPClassifier
    prediction = mlp.predict(mfccs_scaled)

    # Check if the prediction is 1 (authorized user)
    if prediction > 0.5 :  # Use any() to check if any element in the array is True
        print("Authorized user detected!")
    else:
        print("Unauthorized user detected!")

if __name__ == "__main__":
    record_audio()
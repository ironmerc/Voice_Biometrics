from model_testing import verifyUser
import sounddevice as sd
from scipy.io.wavfile import write
from creatingData import extract_mfcc
from sklearn.naive_bayes import BernoulliNB
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import time
import warnings
import pyttsx3

#setup voice engine of py text to speech
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 200)


def speaker_identifier():

    fs = 44100
    duration = 3
    print("speak Hello when the recording starts")
    engine.say("Speak Hello when the recording starts!")
    engine.runAndWait()

    time.sleep(0.1)
    print("recording started")

    rec = sd.rec(int((duration * fs)), samplerate=fs, channels=1)

    sd.wait()

    print("recording stopped")

    file = "C:\\Users\\sinha\\Desktop\\Voice-Biometric\\data\\history\\last_try.wav"
    #this will save the audio of the last person tried to access the software,
    # will help later to identify the person
    write(filename=file, rate=fs, data=rec)

    mfcc = extract_mfcc(file, n_mfcc=40) #defined in creatingData.py

    input = pd.DataFrame(columns=range(0, 40))

    lst = list(mfcc)
    input.loc[len(input)] = lst

    df = pd.read_csv("C:/Users/sinha/Desktop/Voice-Biometric/data/complete_data.csv")  # target variable is boolean : 1 means sahil, 0 means unknown
    

    Y = df["speaker"]
    X = df.drop(columns=["speaker", "Unnamed: 0"])



    # NOTE: Below are 5 models i researched upon out of which i found MLP neural netowrks best and also optimized them
    # to their highest accuracy through many iterations.

    # MLPClassifier, working fair.
    #Please optimize the classifier according to your requirements.
    classifier = MLPClassifier(solver='adam', alpha=0.001,
                               random_state=1, max_iter=500,
                               hidden_layer_sizes=100, activation="logistic")

    warnings.simplefilter("ignore")
    classifier.fit(X, Y)

    pred_mlp = classifier.predict(input)
    return pred_mlp[0]


    # random forest, average
    # warnings.simplefilter("ignore")
    # clf_forest = RandomForestClassifier(max_depth=100, random_state=1
    #                                     , n_estimators=75, criterion="entropy",
    #                                     max_features="auto")
    # clf_forest.fit(X, Y)
    # pred_rf = clf_forest.predict(input)
    # return pred_rf[0]


    # K nearest neighbours classifier, not working for true cases
    # warnings.simplefilter("ignore")
    # neigh = KNeighborsClassifier(n_neighbors=3)
    # neigh.fit(X, Y)
    # pred_knn = neigh.predict(input)
    # return pred_knn[0]


    # Naive Bayes gaussian, less accuracy
    # warnings.simplefilter("ignore")
    # gnb = GaussianNB()
    # gnb.fit(X, Y)
    # pred_gnb = gnb.predict(input)
    # return pred_gnb[0]


    # Naive bayes bernoulli, not working properly, rejected

    # warnings.simplefilter("ignore")
    # bnb = BernoulliNB()
    # bnb.fit(X, Y)
    # pred_bnb = bnb.predict(input)
    # return pred_bnb[0]

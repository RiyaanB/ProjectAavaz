import speech_recognition as sr
import time

"""class SpeechRecognizer:
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.pause_threshold = 0.85
        self.r.phrase_threshold = 0.15
        self.r.non_speaking_duration = 0.2
        self.is_recording = False
        self.is_fetching = False

    def get_word(self):
        self.is_recording = True
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.r.listen(source)
        print("Done listening")
        self.is_recording = False
        self.is_fetching = True
        try:
            print("getting text")
            words = str(self.r.recognize_google(audio)).lower()
            print("got text")
        except:
            print("Unknown Value Error")
            return ""        
        return words
"""


class SpeechRecognizer:
    s = sr.Recognizer()
    print("Calibrating...")
    temp_a = time.time()
    with sr.Microphone() as source:
        s.adjust_for_ambient_noise(source)
    print("Done calibrating. Took " + str(time.time() - temp_a))
    s.pause_threshold = 0.85
    s.phrase_threshold = 0.15
    s.non_speaking_duration = 0.2
    
    def __init__(self):
        self.r = SpeechRecognizer.s
        self.is_recording = False
        self.is_fetching = False

    def get_word(self):
        self.is_recording = True
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.r.listen(source)
        print("Done listening")
        self.is_recording = False
        self.is_fetching = True
        try:
            print("getting text")
            words = str(self.r.recognize_google(audio)).lower()
            print("got text")
        except:
            print("Unknown Value Error")
            return ""        
        return words


class Word:
    def __init__(self, actual_word, variation_list):
        self.actual_word = actual_word
        self.variation_list = variation_list


def get_words():
    lines = open("Words", "r").read().split("\n")
    words = []
    for line in lines:
        data = line.split(",")
        for d in range(0, len(data)):
            data[d] = data[d].lower()
        words.append(Word(data[0], data))
    return words

if __name__ == "__main__":
    while True:
        print(SpeechRecognizer().get_word())

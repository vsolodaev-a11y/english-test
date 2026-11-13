import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time
words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "другой", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]}
duration = 5  # секунды записи
sample_rate = 44100
print("Привет, ясоздал эту игру для проверки твоих знаний по английскому!")
level = input('Выбери сложность (easy, medium, hard)')
words = words_by_level[level]
random.shuffle(words)
recognizer = sr.Recognizer()
translator = Translator()
count = 0
for word in words:
    print(f'как будет {word} на английском?')
    time.sleep(2) 
    print('Говори')
    recording = sd.rec(
    int(duration * sample_rate), # длительность записи в сэмплах
    samplerate=sample_rate,      # частота дискретизации
    channels=1,                  # 1 — это моно
    dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи
    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...")
    
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-EN").lower()
        print("Ты сказал:", text)
        translated = translator.translate(word, dest='en')  # здесь 'en' — это английский
        print("🌍 Перевод на английский:", translated.text)
        word = translated.text.lower()
        if text == word:
            print('5 из 5')
            count += 1
        else:
            print('0 из 5')
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("микро всё съел")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")
print(count)


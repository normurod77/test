import webbrowser
import random
import pyttsx3
import vosk
import sys
import sounddevice as sd
import queue
import json
import winsound
import datetime

model = vosk.Model("model")
samplerate = 16000
device = 1

ctime = 'подскажи время время который час алло'
hello = 'привет доброе утро здарово'
joke = 'расмеши меня раскажи шутку ты знаешь шуток'
cmd_list = ctime, hello, joke

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
                
def talk(words):
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()

def va_respond(voice: str):
    cmd = voice
    if 'а' in cmd or 'е' in cmd or 'ё' in cmd or 'и' in cmd or 'о' in cmd or 'у' in cmd or 'э' in cmd or 'ю' in cmd or 'я' in cmd or 'ы' in cmd:
        print(voice)
    if voice.startswith("джарвис"):
        # обращаются к ассистенту
        #cmd = recognize_cmd(filter_cmd(voice))
        cmd = voice
        makeSomething(cmd)#['cmd']

def makeSomething(cmd: str):
    if 'открой ютуб' in cmd:
        winsound.PlaySound('Запрос выполнен сэр.wav', winsound.SND_FILENAME)
        u = 'https://youtube.com'
        webbrowser.open(u)
    
    elif 'привет' in cmd or ' доброе утро' in cmd or ' здарово' in cmd:
        now = datetime.datetime.now()
        if 0<now.hour<10:
            winsound.PlaySound('Доброе утро.wav', winsound.SND_FILENAME)
        else:
            winsound.PlaySound('helloo.wav', winsound.SND_FILENAME)
    
    elif 'подскажи время' in cmd or 'время' in cmd or 'который час' in cmd:
        now = datetime.datetime.now()
        text = "Сейчас " + str(now.hour) + " " + str(now.minute)
        talk(text)
    
    elif 'пока' in cmd:
        talk("Без проблем")
        sys.exit()
    
    elif 'подскажи время' in cmd or 'время' in cmd or 'который час'in cmd:
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']
        talk(random.choice(jokes))

    elif "как будет " in cmd:
        mpt=str(zadanie[zadanie.find("как будет "):])
        leng = Translator(from_lang="ru", to_lang="en")
        text = leng.translate(mpt)
        talk(text)

va_listen(va_respond)
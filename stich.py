import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from translate import Translator
from kivy.uix.image import Image
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
            winsound.PlaySound('Доброе утро.wav', winsound.SND_FILENAME)
    
    elif 'подскажи время' in cmd or 'время' in cmd or 'который час' in cmd:
        now = datetime.datetime.now()
        text = "Сейчас " + str(now.hour) + " " + str(now.minute)
        talk(text)
    
    elif 'пока' in cmd:
        talk("Без проблем")
        sys.exit()
    
    elif 'расмеши меня' in cmd or 'шутка' in cmd or 'раскажи шутку'in cmd:
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                 'Программист это машина для преобразования кофе в код']
        talk(random.choice(jokes))

    elif "как будет " in cmd:
        mpt=str(zadanie[zadanie.find("как будет "):])
        leng = Translator(from_lang="ru", to_lang="en")
        text = leng.translate(mpt)
        talk(text)
    elif 'заряд' in cmd:
        self.lbl1.text = str(battery.status['isCharging'])
        self.lbl2.text = str(battery.status['percentage']) + "%"
        talk(self.lbl2.text)
        winsound.PlaySound('Другой информации нет.wav', winsound.SND_FILENAME)
class myapp(App):
    """docstring for ClassName"""
    
    def btnpress(self, *args):
        va_listen(va_respond)
    
    def build(self):
        box = BoxLayout()
        btn = Button(text='click me')
        btn.bind(on_press=self.btnpress)
        label = Label(text='Jarvis 1.0')
        box.add_widget(label)
        box.add_widget(btn)
        return box

if __name__ == '__main__':
    myapp().run()
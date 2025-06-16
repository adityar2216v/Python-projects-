import sys
import webbrowser

import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
from requests import get
import wikipedia
import pywhatkit as kit
import pyjokes
import sys
import smtplib

engine= pyttsx3.init("sapi5")
voices= engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.......")
        r.pause_threshold=1
        audio=r.listen(source,timeout=2,phrase_time_limit=5)
    try:
        print("Recognizing......")
        query=r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")
    except Exception as e:
        speak("Say that again please...")
        return"none"
    return query
def wish():
    hour=int(datetime.datetime.now().hour)
    if  hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon")
    else:
        speak("Good evening")
    speak("i am jarvis sir. please tell me how can i help you:")



if __name__=="__main__":
    #speak("Hello Sir")
    wish()
    while True:
        query=takecommand().lower()
        #logic building for task
        if "open chrome" in query:
            path="C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
            os.startfile(path)
        elif "open calculator" in query:
            path="C:\Windows\System32\calc.exe"
            os.startfile(path)
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "open camera" in query:
            cap=cv2.VideoCapture(0)
            while True:
                ret,img=cap.read()
                cv2.imshow('webcam',img)
                k=cv2.waitKey(50)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif "ip address" in query:
            ip=get('https://api.ipify.org').text
            speak(f'your IP address is{ip}')
        elif "wikipedia" in query:
            speak("searching wikipedia")
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia .........")
            speak(results)
            print(results)
        elif "open youtube"in query:
            webbrowser.open("www.youtube.com")

        elif "open spotify"in query:
            webbrowser.open("open.spotify.com")

        elif "open google"in query:
            speak("sir , what should i search on google ")
            cm=takecommand().lower()
            webbrowser.open(f"{cm}")
        elif "send messages" in query:
            kit.sendwhatmsg("+9170806003","this is testing protocol",2,25)
        elif "Play songs " in query:
            kit.playonyt("one dance")
        elif "no thanks" in  query:
            speak("thanks for using me sir , have a good day. ")
            sys.exit()
        speak("sir,do you have any other work")
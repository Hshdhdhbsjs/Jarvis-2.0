import os
import sys
import webbrowser
import pyautogui
import pyttsx3
import datetime
import time
import speech_recognition as sr 
import json
import pickle
import shutil
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer 
import random
import numpy as np
import psutil
import subprocess

import wikipedia

#from elevenlabs import ElevenLabs
#from api_key import API_KEY

# Initialize the client
#client = ElevenLabs(api_key=API_KEY)

# Example: generate and play speech
#audio = client.generate(text="Hello, how are you?", voice="Grace")
#client.play(audio)

#play(audio)
    

#set_api_key(api_key_data)

with open("intents.json") as file:
    data=json.load(file)

model=load_model("chat_model.h5")

with open("tokenizer.pk1","rb")as f:
    tokenizer=pickle.load(f)

print(type(tokenizer))


with open("label_encoder.pk1","rb")as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)


    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()


def command():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        print("Listening....." ,end="",flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate=48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit=10
        print(sr.Microphone.list_microphone_names())
        audio=r.listen(source)

    try:
        print("\r", end="",flush=True)
        print("Recognizing....",end="",flush=True)
        
        query=r.recognize_google(audio,language='en-in')
        print("\r", end="",flush=True)
        print(f"User said :{query}\n")
    except Exception as e:
        print("Say that again please")    

        return "None"
    return query

def cal_day():
    day=datetime.datetime.today().weekday()+1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week=day_dict[day]
        print(day_of_week)
    return day_of_week


def wishMe():
    hour=int(datetime.datetime.now().hour)
    t= time.strftime("%I:%M:%p")
    day=cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Pavan D A, its {day} and the time is {t}")
    elif(hour>=12) and (hour<=23) and ('PM' in t):
        speak(f"Good afternoon Pavan D A, its {day} and the time is {t}")
   
    


    speak("Hi Boss, how can i help u")
    



def social_media(command):
    if'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    
    elif'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    
      
    elif'telegram' in command:
        speak("opening your telegram")
        webbrowser.open("https://telegram.org/")

      
    elif'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")

    else:
        speak("No result found")


def schedule():
    day = cal_day().lower()
    speak("Boss, today's schedule is ")
    week = {
        "monday": "Boss, from 8:45 am to 3:45 pm you have college. You will take 3 hours to reach home by hanging out with your stupid friends.",
        "tuesday": "Boss, Tuesday will be same as Monday but you will reach one hour early because you don't have the last period.",
        "wednesday": "Boss, Wednesday is your chill day and you play cricket or drink some booze with your friends and come back home at the same time as Monday.",
        "thursday": "Boss, it will be same as Tuesday and you will have some homework to do.",
        "friday": "Boss, you will reach home same as Monday and will watch a movie or web series at night.",
        "saturday": "Boss, today you're resting at home because college is a holiday — watch movies or do some other stuff.",
        "sunday": "Boss, today is chicken day and you eat, drink, and sleep."
    }

    # Speak the schedule for today
    if day in week:
        speak(week[day])
    else:
        speak("Boss, I don't know what day it is.")

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Users\\dapav\\AppData\\Local\Microsoft\\WindowsApps\\mspaint.exe')
    
    elif "edge" in command:
        speak("opening microsoft edge")
        os.startfile('C:\\Program Files (x86)\\Microsoft\Edge\\Application\\msedge.exe')
    
    
    elif "movie" in command:
        movies_path = r'C:\Users\dapav\OneDrive\Desktop - Copy\Desktop\MOVIES'
        vlc_path = r'C:\Program Files\VideoLAN\VLC\vlc.exe'

        try:
            all_files = os.listdir(movies_path)
            print("All files:", all_files)

            movie_files = [file for file in all_files if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))]
            print("Filtered movie files:", movie_files)

            if not movie_files:
                speak("No movie files found in the folder.")
            else:
                speak("Please type the movie name you want to play:")
                movie_name = input("Enter movie name: ").lower()

                matched_movie = None
                for movie in movie_files:
                    if movie_name in movie.lower():
                        matched_movie = os.path.join(movies_path, movie)
                        break

                if matched_movie:
                    print(f"Opening: {matched_movie}")
                    speak(f"Playing {movie_name}")
                    subprocess.run([vlc_path, matched_movie])
                
                else:
                    speak("Movie not found.")
        except Exception as e:
            print("Error:", e)
            speak("Something went wrong while trying to open the movie.")

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system('taskkill /f /im calc.exe')
    elif "notepad" in  command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')

def browsing(query):
    if'google' in query:
        speak("Boss, what should i search in google..")
        s = command().lower()
        webbrowser.open(f"{s}")

def search_youtube(query):
    if 'youtube' in query:
        speak("Boss, what should I search on YouTube?")
        s = command().lower()
        search_query = s.replace(' ', '+')
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

   # elif 'edge' in query:
       # speak("opening your microsoft edge")
        #ege_path = shutil.which("msedge")

    #if edge_path: # type: ignore
       # print("Edge path:", edge_path)
       # os.startfile(edge_path)
   # else:
       # print("Microsoft Edge not found.")


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percent")

    battery = psutil.sensors_battery()
    if battery is not None:
        percentage = battery.percent
        speak(f"Boss, our system has {percentage} percent battery.")
    else:
        speak("Boss, I couldn't fetch the battery status. Maybe you're on a desktop.")

    if percentage>=80:
        speak("Boss, we could have enough charging to continue our work")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very less power , please connect to the charger")




if __name__=="__main__":
    wishMe()
    #engine_talk("Allow me to introduce myself i am jarvis, the virtual Artificial intelligence and iam here to assist you with a variety of takes as best i can,24 hours a day seven days a week.")
    while True:
        query=command().lower()
        #query=input("Enter your command->")
        if('facebook'in query) or ('telegram'in query) or ('instagram'in query) or ('whatsapp' in query):
            social_media(query)
        elif("my time table" in query) or ("schedule"in query):
            schedule()
        elif("volume up"in query) or ("increase volume"in query):
            pyautogui.press("volumeup")
            speak("volume increased")
        elif("volume down"in query) or ("decrease volume"in query):
            pyautogui.press("volumedown")
            speak("volume decreased")
        elif("volume mute"in query) or ("mute the sound"in query):
            pyautogui.press("volumemute")
            speak("volume muted")
        elif("open calculator"in query) or ("open notepad"in query) or ("open paint"in query) or ("open movies"in query) or ("open microsoft edge"in query):
            openApp(query)
        elif("close calculator"in query) or ("close notepad"in query) or ("close paint"in query):
            closeApp(query)

        elif("what"in query)or("who"in query) or ("how "in query)or ("hi"in query) or ("thanks"in query) or ("hello" in query) or ("joke"in query):
             padded_sequences= pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')

             result=model.predict(padded_sequences)
             tag=label_encoder.inverse_transform([np.argmax(result)])

             for i in data['intents']:
                if i['tag']==tag:
                    speak(np.random.choice(i['responses']))

        elif ("open the google"in query) :
            browsing(query)

        elif ("system condition"in query)or ("condition of the system"in query):
            speak("checking the system conditions")
            condition()
        elif "youtube" in query:
            search_youtube(query)
 
                    
                    
                    
        
        
        elif "exit"in query:
            speak("Goodbye BOss, have a nice day")
            break
            sys.exit()
 

 

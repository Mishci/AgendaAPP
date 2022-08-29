import tkinter
from urllib.request import urlopen
import requests
import os
import io
from tkinter import Label

from PIL import ImageTk, Image


class Weather(Label):

    def __init__(self, master, city: str, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self.master = master
        self.config(bg="LightSeaGreen", width=600, height=50)
        self.pack(fill="x", expand=True, side=tkinter.BOTTOM)

        self.endpoint = "https://api.openweathermap.org/data/2.5/weather?"
        self.params = {
            "q": city,
            "appid": os.environ["APPID"],
            "units": "metric"
        }
        self.weather_data = {}
        self.icon = None

    # ------------------------------------------FETCHING DATA FROM API ----------------------------------------
    def return_weather(self, endpoint="https://api.openweathermap.org/data/2.5/weather?"):
        response = requests.get(endpoint, params=self.params)
        self.weather_data = response.json()


        # using the data to fetch and display current weather icon
        weather_icon_id = self.weather_data['weather'][0]['icon']
        url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=weather_icon_id)
        response = urlopen(url).read()
        io_icon = Image.open(io.BytesIO(response))
        icon = ImageTk.PhotoImage(io_icon)
        self.icon = icon # holding the refference in attribute -> updated in idletasks in root crucial for displaying

        act_temp = self.weather_data ['main']['temp']
        self.config(text = f"Aktualni pocasi: {act_temp}°C ", image= self.icon, compound=tkinter.RIGHT, font=("Courier", 16), fg="yellow")




import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

from data import insert_weather_data

# from data import insert_weather_dat
load_dotenv()
API_KEY = os.getenv("API_GEO_KEY")
API_OPENAI_KEY = os.getenv("API_OPENAI_KEY")

client = OpenAI(api_key=API_OPENAI_KEY)


class WeatherApp:

    def __init__(self, city, country):
        self.longitude = None
        self.latitude = None
        self.temperatur = None
        self.windspeed = None
        self.ai_clothing_advice = None
        self.city = city
        self.country = country
        self.forecast_list = []  # list of days for the forecast

    def run(self):
        self.get_coordinates()
        self.get_weather()
        self.ai_clothing_advice = self.suggest_clothing()

    def get_coordinates(self):
        url = f"https://api.api-ninjas.com/v1/geocoding?city={self.city}&country={self.country}"  # API for geoposition: lat and long
        headers = {'X-Api-Key': API_KEY}
        response = requests.get(url, headers)

        if response.status_code == 200:
            geo_data = response.json()
            if not geo_data:
                print("API works, but no location found.")
            self.longitude = geo_data[0]["longitude"]
            self.latitude = geo_data[0]["latitude"]
        else:
            print(f"Error fetching data, the status code is:{response.status_code}")

    def get_weather(self):
        url = "https://api.open-meteo.com/v1/forecast"

        parameters = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current_weather": True
        }
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            weather_data = response.json()
            self.temperatur = int(weather_data["current_weather"]["temperature"])
            self.windspeed = int(weather_data["current_weather"]["windspeed"])
            insert_weather_data(self.temperatur, self.windspeed, self.longitude, self.latitude, self.city, self.country,
                                self.ai_clothing_advice)
        else:
            print(f"Error fetching data, the status code is:{response.status_code}")

    def suggest_clothing(self):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": 'system', "content": "You are a helpfull weather stylist assistant with sense of humor."},
                {"role": "user",
                 "content": f"for {self.city} with {self.temperatur} degrees and {self.windspeed} kmh, "
                            f"suggest me some clothes to wear. ! mind it that i read it in console, "
                            f"so make each line 100 char max, so i can see it in my console."}
            ]
        )
        return response.choices[0].message.content

    def get_weather_forecast(self, user_num):
        url = "https://api.open-meteo.com/v1/forecast"

        parameters = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "daily": "temperature_2m_min,temperature_2m_max",
            "timezone": "auto",
            "forecast_days": "16"
        }
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            for i in range(user_num):
                weather_data = response.json()
                date = weather_data["daily"]["time"][i]
                min_temp = weather_data["daily"]["temperature_2m_min"][i]
                max_temp = weather_data["daily"]["temperature_2m_max"][i]
                forecast = f"On the date: {date}, the temperature is: min: {min_temp} | max: {max_temp}"
                self.forecast_list.append(forecast)
                print(f"On the date: {date}, the temperature is: min: {min_temp} | max: {max_temp}")
        else:
            print(f"Error fetching data, the status code is:{response.status_code}")

    def get_clothes_forecast(self, user_num):
        self.get_weather_forecast(user_num)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": 'system', "content": "You are a helpfull weather stylist assistant with sense of humor and "
                                              "high fashion for traveling."},
                {"role": "user",
                 "content": f"this list: {self.forecast_list} is the weather forecast list for {self.city} city in {self.country} for {user_num} "
                            f"days of the trip. Suggest me short instructions for clothing for this period.! mind it that i read it in console, "
                            f"so make each line 100 char max, so i can see it in my console."
                 }
            ]
        )
        print(response.choices[0].message.content)

from idlelib.rpc import response_queue
from idlelib.run import flush_stdout
from random import choice
from traceback import print_tb
import os
from dotenv import load_dotenv
from openai import OpenAI

from weather_oop import WeatherApp
from data import create_table, export_to_csv
from voice_recording import record, voice_to_text
import time
import threading
import sys
import json
# Initialize database table
create_table()
load_dotenv()

client = OpenAI(api_key=os.getenv("API_OPENAI_KEY"))

# def get_city():
#     """Getting initial city via CLI user input"""
#     """Prompt user for city and country and return a WeatherApp instance."""
#
#     city = input("Please enter the city: ").strip()
#     country = input("Please enter the country: ").strip()
#     return WeatherApp(city, country)

def extract_location(user_voice_to_text):
    # print(user_voice_to_text) - for debugging
    sys_message = "you are helpful assistant that extract geographical location from text"
    user_message = f"""extract the city and the country from the following sentence. If either is missing, return null.
    return a python dictionary with exactly two fields: 'city' and 'country'.
    text:{user_voice_to_text}"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {"role": 'system', "content": sys_message},
                {"role": "user", "content": user_message},
                    ],
            temperature = 0)
    #print(response.choices[0].message.content) - for debugging
    return response.choices[0].message.content

def countdown(seconds):
    print("speak now: Recording...")
    for i in range (10,0,-1):
        print(f"\r {i}", end="",flush=True)
        time.sleep(1)
    print("\nRecording complete")


def get_input_from_voice():
    print(f"\n Please speak 🚨you have 10 seconds🚨...")
    timer = threading.Thread(target=countdown, args=(10,))
    timer.start()
    audio_file = record()
    timer.join()

    try:
        text = voice_to_text(audio_file)
        print(f"finding weather information for the city in the country...")
        return text
    except Exception as e:
        print(f"transcription failed {e}")
        #return input(f"fallback - enter {label.capitalize()} name manually: ").strip()


def main():
    #weather = get_city()  # Getting initial city via CLI user input
    text = get_input_from_voice()
    #country = get_input_from_voice("country") - for debugging
    data_dict = extract_location(text)
    data_dict = json.loads(data_dict)
    # if not data_dict.strip(): - for debugging and blow
    #     print("no data found")
    # try:
    #     data_dict = json.loads(data_dict)
    # except json.JSONDecodeError as e:
    #     print("json decode error")
    #     print(f"response was {data_dict}") - for debugging up to here
    city = data_dict["city"]
    country = data_dict["country"]
    weather = WeatherApp(city, country)
    weather.run()

    while True:
        print("\n MENU")
        print("1. Get coordinates")
        print("2. Get current weather")
        print("3. Suggest clothing") # clothing reco
        print("4. Get weekly forecast")
        print("5. Export database to CSV")
        print("6. Choose another city")
        print("7. Get weekly clothing recommendations") # clothing reco
        print("0. Exit")

        choice = input("Choose an option (0-6): ").strip()

        try:
            if choice == "1":
                weather.get_coordinates()
                print(f"Latitude: {weather.latitude}, Longitude: {weather.longitude}")

            elif choice == "2":
                weather.get_coordinates()
                weather.get_weather()
                print(f"""\nThe weather report in {weather.city}, {weather.country} is:
                      - Temperature: {weather.temperatur}
                      - Wind speed: {weather.windspeed}""")

            elif choice == "3":
                weather.get_coordinates()
                weather.get_weather()
                print(weather.suggest_clothing())

            elif choice == "4":
                num = int(input("Please enter the number of days: "))
                weather.get_coordinates()
                weather.get_weather_forecast(num)  # Uncomment when implemented

            elif choice == "5":
                export_to_csv()
                print("Data exported to CSV successfully!")

            elif choice == "6":
                weather = get_input_from_voice()  # Update the weather variable with new city

            elif choice == "7":
                num = int(input("Please enter the number of days for trip: "))
                weather.get_coordinates()
                weather.get_clothes_forecast(num)

            elif choice == "0":
                print("Thank you for using the Weather App. Goodbye!")
                break

            else:
                print("Invalid input. Please enter a number between 0-6.")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
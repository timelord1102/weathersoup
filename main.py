import configparser
import json
import threading
from  datetime import datetime, timedelta
from startup import StartUp
from commands import Commands

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}


config = configparser.ConfigParser()
config.read('user.prefs')

print("Running Startup...")
StartUp.getLocationData(config)
print("Done!")

commandDict = { "help": (lambda : Commands.printHelp()), "setlocation": (lambda : Commands.setLocation(config)), "setlocationauto" : (lambda : Commands.setLocationAuto(config)) }

command = ''
with open('weatherData.json', 'r+') as f:
        json_data = json.load(f)
while (True):
    if(datetime.today() - datetime.strptime(json_data['weather_data']["currentDate"] + json_data['weather_data']['lastChecked'][0:-7], '%Y-%m-%d%H:%M:%S') > timedelta(minutes=10)):
        download_thread = threading.Thread(target=StartUp.checkWeatherDataThread, args=(config,))
        download_thread.start()
    command = input("Enter a command ('help' for list of commands): ")
    if(command.lower() == "exit" or command.lower() == "quit" or command.lower() == "q" or command.lower() == "e"):
        exit()
    else:
        commandDict.get(command.lower(), lambda: print('Invalid command'))()


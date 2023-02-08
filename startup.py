import weather
import geocoder
from commands import Commands

class StartUp:
    def getLocationData(config):

        if(config.get('RESTART DATA', 'locPermissions') == 'False' and config.get('RESTART DATA', 'locManual') == 'False'):
            command = input("Would you like to turn on automatic location for faster weather data? (Y/n)\n")
            if(command.lower() == 'y' or command.lower() == 'yes' or command.lower() == ''):
                config.set('RESTART DATA', 'locPermissions', 'True')
                config.set('RESTART DATA', 'locPermissions', 'True')
                with open('user.prefs', 'w') as configfile:
                    config.write(configfile)
            else:
                print("You can turn on automatic location at any time by entering the command 'setlocationauto'")
                print("Alternatively, You can set your location manually at any time by entering the command 'setlocation'")


        if(config.get('USER INFO','country') == '' or config.get('USER INFO','city') == '' or config.get('USER INFO', 'region') == '' or 
        (config.get('RESTART DATA', 'locPermissions')=='True')):
            Commands.setLocationAuto(config)



    def checkWeatherData(config):
        if(config.get('RESTART DATA', 'checkWeather') == 'True' and config.get('USER INFO','country') != '' and config.get('USER INFO','city') != '' and config.get('USER INFO', 'region') != ''):
            weatherData = weather.collectWeatherData(config)
            if (weatherData == None):
                command = input("ERROR: The program failed to get weather information. Would you like to try again on the next restart? (Y/n)")
                if (command.lower() == 'n' or command.lower() == 'no'):
                    config.set('RESTART', 'checkWeather', 'False')
                elif(command.lower() == 'y' or command.lower() == 'yes' or command.lower() == ''):
                    pass
                else:
                    print("Invalid Command. Using default (Y)")


    def checkWeatherDataThread(config):
        if(config.get('RESTART DATA', 'checkWeather') == 'True' and config.get('USER INFO','country') != '' and config.get('USER INFO','city') != '' and config.get('USER INFO', 'region') != ''):
            weather.collectWeatherData(config)


    def stateToAbbrev(state):
        us_state_to_abbrev = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "District of Columbia": "DC",
            "American Samoa": "AS",
            "Guam": "GU",
            "Northern Mariana Islands": "MP",
            "Puerto Rico": "PR",
            "United States Minor Outlying Islands": "UM",
            "U.S. Virgin Islands": "VI",
        }
        return us_state_to_abbrev[state]
           
                    
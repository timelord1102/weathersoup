import geocoder
import startup

class Commands:

    def clearConfig(config):
        config.set('USER INFO', 'country', '')
        config.set('USER INFO', 'city', '')
        config.set('USER INFO', 'region', '')

    def setLocationAuto(config):
        print("Gathering location data...")
        Commands.clearConfig(config)
        try:
            g = geocoder.ip('me')
            city = g.city
            country = g.country
            region = startup.StartUp.stateToAbbrev(g.state)
            postal = g.postal

            config.set('USER INFO', 'city', str(city))
            config.set('USER INFO', 'country', str(country))
            config.set('USER INFO', 'region', str(region))
            config.set('USER INFO', 'postal', str(postal))
            config.set('RESTART DATA', 'locManual', 'False')
            config.set('RESTART DATA', 'locPermissions', 'True')

            
            with open('user.prefs', 'w') as configfile:
                config.write(configfile)

            startup.StartUp.checkWeatherData(config)
            
            print("Your location has been set to " + city + ", " + region + ", " + country + ". You can change your location manually with the command 'setlocation'.")

        except:
            print("ERROR: The program failed to get your location. Please check your connection or set your location later with command 'setlocation'")

    def setLocation(config):
        Commands.clearConfig(config)
        country = input("Enter your country: ")
        while(country == ''): 
            print("ERROR: You must enter a country.")
            country = input("Enter your country: ")
        if (country.lower() == 'united states' or country.lower() == 'usa' or country.lower() == 'america' or country.lower() == 'us'):
            country = 'US'
            config.set('USER INFO', 'postal', str(input("Enter your zip code: ")))
        region = input("Enter your state/region: ")
        while(region == ''): 
            print("ERROR: You must enter a state/region.")
            region = input("Enter your state/region: ")

        city = input("Enter your city: ")
        while(city == ''): 
            print("ERROR: You must enter a city.")
            city = input("Enter your city: ")

        config.set('USER INFO', 'city', str(city))
        config.set('USER INFO', 'country', str(country))
        config.set('USER INFO', 'region', str(region))
        config.set('RESTART DATA', 'locManual', 'True')

        with open('user.prefs', 'w') as configfile:
                config.write(configfile)
        startup.StartUp.checkWeatherData(config)

    def printHelp():
        print( "\n\thelp: see all commands\n\n\tquit: exit program\n\n\tsetlocation: set or change your location\n" )

import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# NOTE: Compiles temps and dates into json file -- seems to work
# NOTE: either make new function or rewrite to work with this one for weather conditions and precip
def compileData(allTemps,allConds,allPrecip,currCond,currTemp,currFeels):
    data = {}
    dateChange = 0
    i = 0
    with open('weatherData.json', 'r+') as f:
        json_data = json.load(f)

    while i < 40:
        if (i == 0):
            if(json_data['weather_data']['currentDate'] == str(datetime.now().date())):
                if(json_data['weather_data']['todayHigh'] < allTemps[i].text.replace('°','')):
                    json_data['weather_data']['todayHigh'] = allTemps[i].text.replace('°','')
                if(json_data['weather_data']['todayLow'] > allTemps[i+1].text.replace('°','')):
                    json_data['weather_data']['todayLow'] = allTemps[i+1].text.replace('°','')

            json_data['weather_data']['currentTemp'] = currTemp.text.replace('°','')
            json_data['weather_data']['currentFeelsLike'] = currFeels.text.replace('°','')
            json_data['weather_data']['currentCondition'] = currCond.text

            if(int(json_data['weather_data']['currentTemp']) > int(json_data['weather_data']['todayHigh'])):
                json_data['weather_data']['todayHigh'] = json_data['weather_data']['currentTemp']

            if(int(json_data['weather_data']['currentTemp']) < int(json_data['weather_data']['todayLow'])):
                json_data['weather_data']['todayLow'] = json_data['weather_data']['currentTemp']

            json_data['weather_data']['currentDate'] = str(datetime.now().date())
            json_data['weather_data']['lastChecked'] = str(datetime.now().time())
            json_data['weather_data']['todayRainChance'] =  allPrecip[i//4].text[4:len(allPrecip[i//4].text)].replace('%','')
            with open('weatherData.json', 'w') as f:
                json.dump(json_data, f, indent=2)
        ##if allTemps[i].text == '--' or allTemps[i+1].text == '--':
          ##  i+=4
        else:
            json_data['weather_data']['nextDays']['day' + str(dateChange)]['date'] = str(datetime.now().date()+timedelta(days=dateChange))
            if(allTemps[i].text > allTemps[i+1].text):
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['high'] = allTemps[i].text.replace('°','')
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['low'] = allTemps[i+1].text.replace('°','')
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['condition'] = allConds[i//4].text
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['precipChance'] =  allPrecip[i//4].text[4:len(allPrecip[i//4].text)].replace('%','')
            elif(allTemps[i].text < allTemps[i+1].text):
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['high'] = allTemps[i+1].text.replace('°','')
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['low'] = allTemps[i].text.replace('°','')
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['condition'] = allConds[i//4].text
                json_data['weather_data']['nextDays']['day' + str(dateChange)]['precipChance'] = allPrecip[i//4].text[4:len(allPrecip[i//4].text)].replace('%','')
            with open('weatherData.json', 'w') as f:
                json.dump(json_data, f, indent=2)
        data[(datetime.now()+timedelta(days=dateChange)).day] = {allTemps[i].text, allTemps[i+1].text}
        i+=4
        dateChange+=1

    return data

# NOTE: should be complete -- debug if needed after data compilation
# Runs faster than lastresort and theoretically is more reliable. Only usable by those in a US city
def collectWeatherData(config):

    if(config.get('USER INFO', 'country') == 'US'):
        URL = "https://weather.com/weather/tenday/l/"+ config.get('USER INFO', 'postal')

        todayURL = "https://weather.com/weather/today/l/"+config.get('USER INFO', 'postal')

    else:
        return lastResort(config)
    try:
        time.sleep(2)
        page = requests.get(URL, timeout = 3.0)
        time.sleep(2)
        pageToday = requests.get(todayURL, timeout = 3.0)

        soup = BeautifulSoup(page.content, 'html.parser')
        todaySoup = BeautifulSoup(pageToday.content, 'html.parser')

        checkPage = soup.find('div' , {'class' : 'NotFound--notFound--zWK1W'})
        checkPageToday = todaySoup.find('div' , {'class' : 'NotFound--notFound--zWK1W'})
        if(not (checkPage is None and checkPageToday is None)):
            return lastResort(config)

    except:
        return lastResort(config)
    allTemps = soup.find_all('span', attrs={'data-testid': 'TemperatureValue'})
    allConds = soup.find_all('span', attrs={'class': 'DetailsSummary--extendedData--307Ax'})
    allPrecip = soup.find_all('div', attrs={'class': 'DetailsSummary--precip--1a98O'})

    currCond = todaySoup.find('div', attrs={'class': 'CurrentConditions--phraseValue--mZC_p'})
    currTemp = todaySoup.find('span', attrs={'class': 'CurrentConditions--tempValue--MHmYY'})
    currFeels = todaySoup.find('span', attrs={'class': 'TodayDetailsCard--feelsLikeTempValue--2icPt'})
    return compileData(allTemps, allConds, allPrecip, currCond, currTemp, currFeels)


# NOTE: should be complete -- debug if needed after data compilation
def lastResort(config):
    region = config.get('USER INFO', 'region')
    region = region.replace(" ",'+')
    city = config.get('USER INFO', 'city')
    city = city.replace(" ",'+')
    country = config.get('USER INFO', 'country')
    country = country.replace(" ",'+')
    URL = 'https://www.google.com/search?q='+city+'+'+region +'+' + country + '+10+day+forecast+weather.com+US'
    try:
        # NOTE: this is to prevent google from blocking the request
        time.sleep(2)
        page = requests.get(URL, timeout = 3.0)
    except:
        return None
    soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all('a', href=True):
        if(a['href'].find('weather.com/weather/tenday') != -1):
            URL = a['href']
            break
    URL = URL.replace('/url?q=', '')
    URL = URL.split('&sa=U')[0]
    URL = URL.replace('%2B', '+')
    URL = URL.replace('%3F', '?')
    URL = URL.replace('%3D', '=')
    try:
        time.sleep(2)
        weather = requests.get(URL, timeout = 1.0)
        time.sleep(2)
        weatherToday = requests.get(URL.replace('tenday','today'), timeout = 1.0)

    except:
        return None
    soupWeather = BeautifulSoup(weather.content, 'html.parser')
    todaySoup = BeautifulSoup(weatherToday.content, 'html.parser')

    allTemps = soupWeather.find_all('span', attrs={'data-testid': 'TemperatureValue'})
    allConds = soupWeather.find_all('span', attrs={'class': 'DetailsSummary--extendedData--307Ax'})
    allPrecip = soupWeather.find_all('div', attrs={'class': 'DetailsSummary--precip--1a98O'})


    currCond = todaySoup.find('div', attrs={'class': 'CurrentConditions--phraseValue--mZC_p'})
    currTemp = todaySoup.find('span', attrs={'class': 'CurrentConditions--tempValue--MHmYY'})
    currFeels = todaySoup.find('span', attrs={'class': 'TodayDetailsCard--feelsLikeTempValue--2icPt'})

    return compileData(allTemps,allConds,allPrecip,currCond,currTemp,currFeels)


    
    
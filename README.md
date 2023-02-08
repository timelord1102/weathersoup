# weathersoup
A weather data scraper using beautiful soup written in Python

A work in progress

Project Goal:
  Create a weather scraper without using Selenium or API to be used in a larger feature-rich terminal-based calender program
 
What's Complete:
  Weather is scraped from weather.com and compiled/stored in a json file. 
  Location is automatically retired via IP and can be manually set as well if needed
  Two methods to get locations weather.com URL: a) Direct (faster) if in US b) Indirect (slower) via explcit google search and link fetch

To do:
  Seperate program into its own consolodated callable module for use in other projects
  Add commands to retrieve data from json file
  Further bug testing

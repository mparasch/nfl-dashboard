# nfl-dashboard
This project is meant to be an intro for me to learn Dash and Plotly using webscraped NFL data.

## Description
Each file in this project has a a specific function.
* ```ESPN_data_scrape.py```  collects data from ESPN's data for [Offense](https://www.espn.in/nfl/stats/team/_/stat/total), [Defense](https://www.espn.com/nfl/stats/team/_/view/defense), and [Standings](https://www.espn.com/nfl/standings/_/group/league).
* ```pro_reference_scrape.py``` scrapes data from [pro-football-reference](https://www.pro-football-reference.com/teams/GNB).
* ```NFL_Dashboard.py``` launches the Dash and Plotly dashboard that visualizes the data from both sources.

## Visuals
#### Section 1 - Drop down menus for Team 1 and Team 2 that allows user to select desired matchup. Provides a scoring estimate based on the 3 game rolling mean.
![Section 1 of the dashboard](/images/Section1.JPG)
#### Section 2 - Drop down menu that allows you to select which metric appears on the line plot for each team. (r_ preface means that it is a rolling mean)
![Section 2 of the dashboard](/images/Section2.JPG)
#### Section 3 - Fully customizable and animated scatterplot. All metrics displayed and filters can be customized by the user.
![Section 3 of the dashboard](/images/Section3.JPG)

## Installation
### Requirements 
* Python 3
* Libraries:
  * pandas
  * re
  * plotly
  * dash
  * urllib.request

Make sure to install the current versions for all libraries listed above using ```pip install <library or module name>```
### Getting Started
If you download the files from this project to your local drive and have the dependencies all installed, you can simply run ```NFL_Dashboard.py``` and the dashboard will run on your local drive at ```http://127.0.0.1:8050/```.\
The data in the library at the time of this being uploaded is for the 2020-2021 season. If you want a different season data you will need to manipulate the web scraping scripts to match the 2021 season and re-run them to overwrite the existing CSV files in the ```/data/...``` folder.

## Project Status
Not actively updating this project, but I may revisit for next season. Enhacements that I would like to create:
* Replace the rolling mean estimate with machine learning model to predict team score.
* Create way to insert the team logos from the ```/logos/...``` folder as different teams are selected.


# NFL Dashboard with webscraping
## Overview
The **NFL Dashboard** is a data-driven application that provides detailed analysis of NFL team performance. The data is scraped from various sources like **ESPN** and **Pro Football Reference**, processed, and visualized in a dashboard. The data pipeline consists of multiple Python scripts that handle the extraction, transformation, and loading (ETL) of data. The main file that ties everything together is **NFL_Dashboard.py**. This script orchestrates the data collection, processing, and visualization tasks. Below is an overview of the components involved in the pipeline.

---

## Description
Each file in this project has a a specific function.
* ```ESPN_data_scrape.py```  collects data from ESPN's data for [Offense](https://www.espn.in/nfl/stats/team/_/stat/total), [Defense](https://www.espn.com/nfl/stats/team/_/view/defense), and [Standings](https://www.espn.com/nfl/standings/_/group/league).
* ```pro_reference_scrape.py``` scrapes data from [pro-football-reference](https://www.pro-football-reference.com/teams/GNB).
* ```NFL_Dashboard.py``` launches the Dash and Plotly dashboard that visualizes the data from both sources.

---

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

---

## Dashboard Screenshots
#### Section 1 - Drop down menus for Team 1 and Team 2 that allows user to select desired matchup. Provides a scoring estimate based on the 3 game rolling mean.
![Section 1 of the dashboard](/images/Section1.JPG)
#### Section 2 - Drop down menu that allows you to select which metric appears on the line plot for each team. (r_ preface means that it is a rolling mean)
![Section 2 of the dashboard](/images/Section2.JPG)
#### Section 3 - Fully customizable and animated scatterplot. All metrics displayed and filters can be customized by the user.
![Section 3 of the dashboard](/images/Section3.JPG)

---

## Data Processing Pipeline

The data pipeline processes the scraped data into a clean and usable format for the NFL Dashboard.

### 1. **Scraping Data from ESPN**:
- **Offensive Stats**: Total yards, passing and rushing yards, points scored, etc.
- **Defensive Stats**: Defensive yards allowed, sacks, interceptions, etc.
- **Standings**: Team win/loss records, home/away records, division rankings.

### 2. **Scraping Data from Pro Football Reference**:
- **Game-by-Game Stats**: Points scored, yards, turnovers, and other performance metrics for each team in the season.

### 3. **Data Merging**:
- The data from both ESPN (offensive, defensive, standings) and Pro Football Reference (game stats) are merged into a single dataframe based on team names and week number.
- Additional metadata (such as conference and division) from the `NFL_Appendix.xlsx` file is joined with the merged data.

### 4. **Data Transformation and Calculation**:
- The data is cleaned by:
  - Renaming columns for consistency.
  - Dropping unnecessary columns.
  - Filling in missing values for specific metrics (e.g., turnovers).
- Additional metrics are calculated, such as:
  - `pts_diff`: Point differential (Team score - Opponent score).
  - Rolling averages for performance metrics like scores and total yards (`r3_team_score`, `r3_opp_score`, `r3_pts_diff`, `r3_off_TotYd`, `r3_def_TotYd`).

---

## Data Structure

The final dataset contains the following columns:

### Columns:
- `Team`: Name of the team.
- `Team_abbrv`: Abbreviation of the team (e.g., 'NYG' for New York Giants).
- `Week`: The week number of the NFL season.
- `Day`: The day of the week the game was played.
- `Date`: The date the game was played.
- `Time`: The time the game was played.
- `W/L`: Win or Loss (1 = Win, 0 = Loss).
- `OT`: Whether the game went into overtime.
- `Record`: Win-loss record of the team.
- `Opponent`: The opposing team.
- `Team_score`: The score of the team.
- `Opp_score`: The score of the opponent.
- `off_1stD`: Offensive first downs.
- `off_TotYd`: Offensive total yards.
- `off_PassY`: Passing yards.
- `off_RushY`: Rushing yards.
- `off_TO`: Offensive turnovers.
- `def_1stD`: Defensive first downs.
- `def_TotYd`: Defensive total yards allowed.
- `def_PassY`: Defensive passing yards allowed.
- `def_RushY`: Defensive rushing yards allowed.
- `def_TO`: Defensive turnovers.
- `pts_diff`: Point differential (team score - opponent score).
- `r3_team_score`: Rolling average of team score over the last 3 games.
- `r3_opp_score`: Rolling average of opponent score over the last 3 games.
- `r3_pts_diff`: Rolling average of point differential over the last 3 games.
- `r3_off_TotYd`: Rolling average of offensive total yards over the last 3 games.
- `r3_def_TotYd`: Rolling average of defensive total yards allowed over the last 3 games.
- `Conference`: The team's conference.
- `Division`: The team's division.

---

## Project Status
Not actively updating this project, but I may revisit for next season. Enhacements that I would like to create:
* Replace the rolling mean estimate with machine learning model to predict team score.
* Create way to insert the team logos from the ```/logos/...``` folder as different teams are selected.

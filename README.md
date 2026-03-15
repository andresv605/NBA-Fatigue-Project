Title: 
NBA Team Performance vs Schedule Fatigue
Project Description:
This project analyzes how NBA team performance is affected by schedule fatigue. Game data is collected using the BALLDONTLIE API and stored in CSV files. The data is then processed to calculate fatigue-related metrics such as rest days, back-to-back games, point differential, and win/loss results.

Data Collection:
A Python script collects NBA game data from the BALLDONTLIE API and appends the results to a dataset over time.

Analysis:
The collected data is analyzed using Python and Jupyter Notebook to compare team performance in different scheduling situations, such as back-to-back games and games played with more rest.

Tools Used:
Python
Pandas
Requests
Seaborn / Matplotlib
Jupyter Notebook
Visual Studio Code
GitHub

Project Structure:
data/
  raw/
  processed/
src/
  collect_games.py
  build_team_games.py
  build_features.py
notebooks/
  analysis_visuals.ipynb

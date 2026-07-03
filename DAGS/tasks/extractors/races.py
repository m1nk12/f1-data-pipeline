import pandas as pd
import requests
from clients.jolpica_client import JolpicaClient

client = JolpicaClient()

def fetch_race(season) -> pd.DataFrame:
    """
    Fetches data for all races in a given season.

    Args:
        season (int): The year of the F1 season.
    Returns:
        dataframe: A list of dictionaries, each containing information for a race in a season.
              Returns an empty list if no constructors are found for the season.
    """

    data = client.get_races(season)
    races_data = data['MRData']['RaceTable']['Races']

    records = []

    for race in races_data:
       records.append({
            'season': race.get('season'),
            'round': race.get('round'),
            'name': race.get('raceName'),
            'date': race.get('date'),
            'time': race.get('time')
       })
    res_df = pd.DataFrame(records)
    return res_df
    
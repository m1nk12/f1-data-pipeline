import requests
import pandas as pd
from clients.jolpica_client import JolpicaClient

client = JolpicaClient()

def fetch_constructor(season) -> pd.DataFrame:
    """
    Fetches data for all constructors in a given season.
    
    Args:
        season (int): The year of the F1 season.
    Returns:
        dataframe: A Dataframe containing information for a constructor.
              Returns an empty list if no constructors are found for the season.
    """
    
    data = client.get_constructors()
    records = []
    constructors_data = data['MRData']['ConstructorTable']['Constructors']

    for constructor in constructors_data:
        records.append({
        'constructorId': constructor.get('constructorId'),
        'name': constructor.get('name'),
        'nationality': constructor.get('nationality')
        })
    res_df = pd.DataFrame(records)
    return res_df

import fastf1
import requests
import pandas as pd
from clients.jolpica_client import JolpicaClient

client = JolpicaClient()

def fetch_driver(season):
    """
    Fetches data for all drivers in a given season.

    Args:
        season (int): The year of the F1 season.
    Returns:
        dataframe: A list of dictionaries, each containing information for a driver.
              Returns an empty list if no drivers are found for the season.
    """
    
    response = client.get_drivers(season)
    drivers = response['MRData']['DriverTable']['Drivers']

    records = []

    for driver in drivers:

        records.append(
            {
                "driver_id": driver["driverId"],
                "given_name": driver["givenName"],
                "family_name": driver["familyName"],
                "code": driver.get("code"),
                "nationality": driver["nationality"],
                "dob": driver["dateOfBirth"],
            }
        )

    return pd.DataFrame(records)
    

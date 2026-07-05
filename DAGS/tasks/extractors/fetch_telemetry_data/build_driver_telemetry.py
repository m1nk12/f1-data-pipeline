import pandas as pd

def build_driver_telemetry(laps, driver, season, round, session):
    """
    Builds telemetry data for a specific driver in a given session.

    Args:
        laps (DataFrame): The laps DataFrame containing lap data for the session.
        driver (str): The driver's code (e.g., "HAM" for Lewis Hamilton).
        season (int): The year of the F1 season.
        round (int): The round number of the race.
        session (str): session type
    Returns:
        DataFrame: A DataFrame containing telemetry data for the specified driver.
    """

    records = []
    driver_laps = laps.pick_drivers(driver)

    for _, lap in driver_laps.iterlaps():
        try:
            telemetry = lap.get_car_data().add_distance()
        except Exception:
            continue
    
    telemetry['season'] = season
    telemetry['round'] = round
    telemetry['session'] = session
    telemetry['driver'] = driver
    telemetry['lap_number'] = lap["LapNumber"]

    records.append(telemetry)

    if(len(records) == 0):
        return pd.DataFrame()
    else:
        return pd.concat(records, ignore_index = True)
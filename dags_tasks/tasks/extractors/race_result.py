from dags_tasks.client.jolpica_client import JolpicaClient
import pandas as pd

client = JolpicaClient()


def fetch_race_result_data(season: int, round: int) -> pd.DataFrame:
    """
    Fetch race results for an entire season.

    Parameters
    ----------
    season : int
        Formula 1 season.

    Returns
    -------
    pd.DataFrame
        One row per driver per race.
    """

    data = client.get_results(season,round)

    races = data["MRData"]["RaceTable"]["Races"]

    records = []


    race_name = races[0]["raceName"]
    race_date = races[0]["date"]

    for result in races[0]["Results"]:

        driver = result["Driver"]
        constructor = result["Constructor"]

        time = result.get("Time", {})
        fastest_lap = result.get("FastestLap", {})
        fastest_lap_time = fastest_lap.get("Time", {})

        records.append(
            {
                "season": season,
                "round": round,
                "race_name": race_name,
                "race_date": race_date,

                "driver_id": driver.get("driverId"),
                "driver_code": driver.get("code"),
                "driver_number": driver.get("permanentNumber"),
                "driver_name": f"{driver.get('givenName')} {driver.get('familyName')}",

                "constructor_id": constructor.get("constructorId"),
                "constructor_name": constructor.get("name"),

                "grid": result["grid"],
                "position": str(result["position"]),
                "points": float(result["points"]),
                "laps": int(result["laps"]),

                "status": result.get("status"),
                "race_time": time.get("time"),

                "fastest_lap_rank": fastest_lap.get("rank"),
                "fastest_lap_number": fastest_lap.get("lap"),
                "fastest_lap_time": fastest_lap_time.get("time"),
            }
        )

    return pd.DataFrame(records)
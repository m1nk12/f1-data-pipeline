from client.fastf1_client import FastF1Client
from build_driver_telemetry import build_driver_telemetry
from storage.write_parquet import write_parquet
from storage.minio_client import upload_file
import tempfile
import os

client = FastF1Client()

def save_driver_telemetry(df, season, round, session, driver):
    """
    create parquet file and save it to minIO bucket
    """

    with tempfile.TemporaryDirectory() as tmp:
        file_name = f"{driver}.parquet"

        local_path = os.path.join(
            tmp,
            file_name
        )


        #Write parquet file
        write_parquet(
            df, 
            local_path
        )

        #path on minIO
        object_name = (
            f"telemetry/"
            f"season={season}/"
            f"round={round}/"
            f"session={session}/"
            f"{driver}.parquet"
        )

        #upload to MinIO
        upload_file(
            bucket="bronze",
            object_name=object_name,
            file_path=local_path
        )


def fetch_telemetry(season: int, round: int, session: str = "R"):
    """
    Fetches telemetry data for a given season, round, and session.

    Args:
        season (int): The year of the F1 season.
        round (int): The round number of the race.
        session (str): The session type. Defaults to "R" for Race.  
                       Other options include "Q" for Qualifying, "S" for Sprint
    Returns:
        dataframe: A DataFrame containing telemetry data for the specified session.
    """
    session = client.get_session(season, round, session)

    laps = session.laps

    for driver in laps['Driver'].unique():
        telemetry_df = build_driver_telemetry(
            laps,
            driver,
            season,
            round,
            session
        )

        if(telemetry_df.empty):
            continue
    save_driver_telemetry(telemetry_df, season, round, session, driver)

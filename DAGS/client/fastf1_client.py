from pathlib import Path

import fastf1


class FastF1Client:

    def __init__(self, cache_dir="/opt/airflow/cache"):
        self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        fastf1.Cache.enable_cache(str(self.cache_dir))

    def get_session(
        self,
        season: int,
        round: int,
        session: str = "R",
    ):
        """
        Load a race session.

        Parameters
        ----------
        session:
            R  -> Race
            Q  -> Qualifying
            S  -> Sprint
            FP1 FP2 FP3
        """

        session_obj = fastf1.get_session(
            season,
            round,
            session,
        )

        session_obj.load(
            laps=True,
            telemetry=True,
            weather=False,
            messages=False
        )

        return session_obj
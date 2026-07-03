from .baseclient import BaseClient


class JolpicaClient(BaseClient):

    BASE_URL = "https://api.jolpi.ca/ergast/f1"

    def __init__(self):
        super().__init__(base_url=self.BASE_URL)

    def get_drivers(self, season: int):
        """
        Get all drivers for a season.
        """
        return self.get(f"{season}/drivers.json")

    def get_constructors(self, season: int):
        """
        Get constructors for a season.
        """
        return self.get(f"{season}/constructors.json")

    def get_races(self, season: int):
        """
        Get races for a season.
        """
        return self.get(f"{season}/races.json")

    def get_results(self, season: int):
        """
        Get race results.
        """
        return self.get(f"{season}/results.json")

    def get_qualifying(self, season: int, round: int):
        """
        Get qualifying results.
        """
        return self.get(f"{season}/{round}/qualifying.json")

    def get_sprint_results(self, season: int, round: int):
        """
        Get sprint results.
        """
        return self.get(f"{season}/{round}/sprint.json")

    def get_pit_stops(self, season: int, round: int):
        """
        Get pit stop data.
        """
        return self.get(f"{season}/{round}/pitstops.json")

    def get_lap_times(self, season: int, round: int):
        """
        Get lap times.
        """
        return self.get(f"{season}/{round}/laps.json")
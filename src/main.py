import json
import os
from datetime import datetime, timedelta

class RaceResultProcessor:
    def __init__(self, data_dir='data', results_dir='results'):
        self.data_dir = data_dir
        self.results_dir = results_dir
        self.drivers = self.load_drivers()
        self.points_table = {i: 61 - i for i in range(1, 61)}
        self.missing_drivers = []

    def load_drivers(self):
        return{
    "Jake Luther": "pro",
    "Bobby Flack": "pro",
    "Aaron Meyers": "pro",
    "Darren Ruthford": "pro",
    "Scott Rister": "pro",
    "Justin Hall7": "pro",
    "Nick Terrell": "pro",
    "Thomas Clawson": "pro",
    "Bradley Alvis": "pro",
    "Jesse Olsen": "pro",
    "Christopher Daniel3": "pro",
    "Mike Braun": "pro",
    "Patrick Cantrell": "pro",
    "Nathan Sides": "pro",
    "Scott Kimbrow": "pro",
    "Andrew Gajdarik": "pro",
    "Aubrey Cundall": "pro",
    "Jordan D Cozzi": "pro",
    "Adam Wok Hei": "pro",
    "William Alcala": "pro",
    "Skyler Gragg": "am",
    "Matthew Wykoff": "pro",
    "Daniel Ciuro": "am",
    "Kevin Madyda": "pro",
    "Darryl Wineinger": "am",
    "Tyler Sage Anderson": "pro",
    "Will Coffey": "pro",
    "Daniel R Hall": "pro",
    "Mitch Buenaventura": "pro",
    "Tony Caicedo": "am",
    "Bob LinDell": "am",
    "Landon Orr": "am",
    "Matthew Markley": "am",
    "Kelvin Collado": "am",
    "Richard Costanza": "am",
    "Shane Brown3": "am",
    "Douglas Jerum": "am",
    "Charles Roats": "am",
    "Kevin Hayes3": "am",
    "Devin M Adams": "am",
    "Derek Fotre": "am",
    "Joseph Evers": "am",
    "Thomas Pereira": "am",
    "Michael Doyon": "am",
    "Chris Krause": "am",
    "Charles Cappelli": "am",
    "Jarod Pettit": "am",
    "Carsten Path": "am",
    "Keith Gwinnup": "am",
    "Fen Acinni": "am",
    "Patricio Montivero": "am",
    "Mauricio Marquez-Ramos": "am",
    "Clarence Rosa": "am",
    "Chris Wells2": "am",
    "Christopher Pierro": "am",
    "Jeff Leaf": "am",
    "Lee Kane": "am",
    "Kevin Hayes III": "am",
    "Logan Brink": "pro",
    "Hector Collazo3": "pro",
    "Keith Roycroft": "am",
    "Christian Gritsko": "pro",
    "Parker Merrill": "am",
    "Chris Genore": "am",
    "Mark Agee": "am",
    "Patrick Ripley": "am"
}

    def did_driver_finish_race(self, driver_data):
        return driver_data.get('reason_out') == 'Running'

    def process_race_results(self, filename):
        race_type = self.get_race_type(filename)
        data = self.load_json_data(filename)

        positions = {'pro': {}, 'am': {}}
        for driver in data['session_results'][0]['results']:
            driver_name = driver['display_name']
            if driver_name not in self.drivers:
                self.missing_drivers.append(driver_name)
                continue

            division = self.drivers[driver_name]
            finished = self.did_driver_finish_race(driver)
            points = self.calculate_points(driver['finish_position'], race_type, finished)
            positions[division][driver_name] = points

        self.write_results_file(positions, filename, data['track']['track_name'])

    def calculate_points(self, position, race_type, finished):
        base_points = self.points_table[position + 1] if finished else 0
        return base_points * 2 if race_type == "endurance" else base_points

    def load_json_data(self, filename):
        with open(filename) as f:
            return json.load(f)

    def get_race_type(self, filename):
        data = self.load_json_data(filename)
        start_time = data.get("start_time", "").replace("Z", "")
        end_time = data.get("end_time", "").replace("Z", "")

        if start_time and end_time:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            race_length = end_time - start_time
            return "endurance" if race_length > timedelta(hours=2) else "sprint"
        return "sprint"

    def write_results_file(self, positions, filename, track_name):
        session_id = filename.split('-')[-1].split('.')[0]
        track_name = track_name.replace(" ", "-")
        output_filename = f"{self.results_dir}/{session_id}-{track_name}.txt"

        with open(output_filename, 'w') as file:
            for division in ['pro', 'am']:
                file.write(f"{division.title()} Division\n")
                sorted_positions = sorted(positions[division].items(), key=lambda x: x[1], reverse=True)
                for i, (driver, points) in enumerate(sorted_positions, 1):
                    status = " - DNF" if points == 0 else ""
                    file.write(f"{i}. {driver} - {points} points{status}\n")
                file.write("\n")

    def get_data_filenames(self):
        filenames = os.listdir(self.data_dir)
        return [os.path.join(self.data_dir, filename) for filename in filenames]

    def run(self):
        filenames = self.get_data_filenames()
        for filename in filenames:
            self.process_race_results(filename)
        print("Missing Drivers:", self.missing_drivers)

if __name__ == "__main__":
    processor = RaceResultProcessor()
    processor.run()

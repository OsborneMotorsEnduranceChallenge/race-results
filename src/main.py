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
        # Initialize the cumulative points tracker
        self.cumulative_points = {'pro': {}, 'am': {}}

    def load_drivers(self):
        with open('driver-data/drivers.json') as f:
            drivers_data = json.load(f)
        return drivers_data

    def did_driver_finish_race(self, driver_data):
        return driver_data.get('reason_out') == 'Running'

    def process_race_results(self, filename):
        race_type = self.get_race_type(filename)
        data = self.load_json_data(filename)

        positions = {'pro': {}, 'am': {}}
        for driver in data['session_results'][0]['results']:
            driver_name = driver['display_name']
            incidents = driver['incidents'] # Extract incidents count

            if driver_name not in self.drivers:
                self.missing_drivers.append(driver_name)
                continue

            division = self.drivers[driver_name]
            finished = self.did_driver_finish_race(driver)
            points = self.calculate_points(driver['finish_position'], race_type, finished, incidents) # Pass incidents to calculate_points
            positions[division][driver_name] = points

            # Update cumulative points
            if driver_name not in self.cumulative_points[division]:
                self.cumulative_points[division][driver_name] = 0
            self.cumulative_points[division][driver_name] += points

        self.write_results_file(positions, filename, data['track']['track_name'])
        
    def calculate_points(self, position, race_type, finished, incidents):
        # Calculate base points; points are 0 if the driver did not finish
        base_points = self.points_table.get(position + 1, 0) if finished else 0
        
        # Double points for endurance races
        if race_type == "endurance":
            base_points *= 2
        
        # Add safety bonus if incidents are fewer than 8
        if incidents < 8:
            safety_bonus = 2 if race_type == "endurance" else 1
        else:
            safety_bonus = 0
        
        # Total points are the sum of base points and any safety bonus
        return base_points + safety_bonus

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

    def write_total_standings(self):
        with open(f"{self.results_dir}/standings.txt", 'w') as file:
            file.write("Total Standings:\n")
            for division in ['pro', 'am']:
                file.write(f"{division.title()} Division\n")
                sorted_positions = sorted(self.cumulative_points[division].items(), key=lambda x: x[1], reverse=True)
                for i, (driver, points) in enumerate(sorted_positions, 1):
                    file.write(f"{i}. {driver} - {points} points\n")
                file.write("\n")

    def run(self):
        filenames = self.get_data_filenames()
        for filename in filenames:
            self.process_race_results(filename)
        print("Missing Drivers:", self.missing_drivers)
        # Write total standings to a file
        self.write_total_standings()

if __name__ == "__main__":
    processor = RaceResultProcessor()
    processor.run()
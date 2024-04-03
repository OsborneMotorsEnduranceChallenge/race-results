import json
import os
from datetime import datetime, timedelta

missing_drivers = []
points_table = {i: 61 - i for i in range(1, 61)}
drivers = {
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

def process_race_results(filename, race_type):
    # Load the JSON data from the file
    with open(filename) as f:
        data = json.load(f)

    pro_positions = {}
    am_positions = {}

    # Iterate over the results
    for driver in data['session_results'][0]['results']:
        # Get the driver's name and position
        driver_name = driver['display_name']
        position = driver['finish_position']

        # Check if the driver_name is in the drivers dict
        if driver_name not in drivers:
            missing_drivers.append(driver_name)
        # Check the driver's division and store their position
        division = drivers.get(driver_name)
        if division == "pro":
            if did_driver_finish_race(driver):
                if race_type == "endurance":
                    pro_positions[driver_name] = points_table[position + 1] * 2
                else:
                    pro_positions[driver_name] = points_table[position + 1]
            else:
                pro_positions[driver_name] = 0
        elif division == "am":
            if did_driver_finish_race(driver):
                if race_type == "endurance":
                    am_positions[driver_name] = points_table[position + 1] * 2
                else:
                    am_positions[driver_name] = points_table[position + 1]
            else:
                am_positions[driver_name] = 0

    # Sort the positions
    pro_positions = sorted(pro_positions.items(), key=lambda x: x[1], reverse=True)
    am_positions = sorted(am_positions.items(), key=lambda x: x[1], reverse=True)

    # Get the session ID from the filename
    session_id = filename.split('-')[-1].split('.')[0]

    # Get the track name
    track_name = data['track']['track_name'].replace(" ", "-")

    # Create the output filename
    output_filename = f"results/{session_id}-{track_name}.txt"

    # Print out the positions of each driver in their respective division
    with open(output_filename, 'w') as file:
        file.write("Pro Division\n")
        for i, (driver, points) in enumerate(pro_positions, 1):
            if points == 0:
                file.write(f"{i}. {driver} - {points} points - DNF\n")
            else:
                file.write(f"{i}. {driver} - {points} points\n")

        file.write("\nAmateur Division\n")
        for i, (driver, points) in enumerate(am_positions, 1):
            if points == 0:
                file.write(f"{i}. {driver} - {points} points - DNF\n")
            else:
                file.write(f"{i}. {driver} - {points} points\n")

def get_data_filenames():
    data_dir = 'data'
    filenames = os.listdir(data_dir)
    return [os.path.join(data_dir, filename) for filename in filenames]

def did_driver_finish_race(driver_data):
    reason_out = driver_data.get('reason_out')
    if reason_out == 'Running':
        return True
    else:
        return False

def get_race_type(filename):
    with open(filename) as f:
        data = json.load(f)

    race_type = None
    try:
        start_time = data.get("start_time").replace("Z", "")
        end_time = data.get("end_time").replace("Z", "")
        if start_time and end_time:
            # Convert the timestamps to datetime objects
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            race_length = end_time - start_time
            if race_length > timedelta(hours=2):
                race_type = "endurance"
            else:
                race_type = "sprint"
    except (json.JSONDecodeError, ValueError):
        pass
    return race_type

def main():
    filenames = get_data_filenames()
    for filename in filenames:
        race_type = get_race_type(filename)
        process_race_results(filename, race_type)
        print(race_type)

if __name__ == "__main__":
    main()
    print("Missing Drivers:")
    for driver in missing_drivers:
        print(driver)
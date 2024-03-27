import pandas as pd
import json
from iracingdataapi.client import irDataClient
import os

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
    "Skyler Gragg": "pro",
    "Matthew Wykoff": "pro",
    "Daniel Ciuro": "pro",
    "Kevin Madyda": "pro",
    "Darryl Wineinger": "pro",
    "Tyler Sage Anderson": "pro",
    "Will Coffey": "pro",
    "Daniel R Hall": "am",
    "Mitch Buenaventura": "am",
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
    "Jeff Leaf": "am"
}

def process_race_results(filename):
    # Load the JSON data from the file
    with open(filename) as f:
        data = json.load(f)

    pro_positions = {}
    am_positions = {}

    # Iterate over the results
    for result in data['session_results'][0]['results']:
        # Get the driver's name and position
        driver_name = result['display_name']
        position = result['finish_position']

        # Check the driver's division and store their position
        division = drivers.get(driver_name)
        if division == "pro":
            pro_positions[driver_name] = position
        elif division == "am":
            am_positions[driver_name] = position

    # Sort the positions
    pro_positions = sorted(pro_positions.items(), key=lambda x: x[1])
    am_positions = sorted(am_positions.items(), key=lambda x: x[1])

    # Get the session ID from the filename
    session_id = filename.split('-')[-1].split('.')[0]

    # Get the track name
    track_name = data['track']['track_name'].replace(" ", "-")

    # Create the output filename
    output_filename = f"results/{session_id}-{track_name}.txt"

    # Print out the positions of each driver in their respective division
    with open(output_filename, 'w') as file:
        file.write("Pro Division\n")
        for i, (driver, position) in enumerate(pro_positions, 1):
            file.write(f"{i}. {driver}\n")

        file.write("\nAmateur Division\n")
        for i, (driver, position) in enumerate(am_positions, 1):
            file.write(f"{i}. {driver}\n")

def get_data_filenames():
    data_dir = 'data'
    filenames = os.listdir(data_dir)
    return [os.path.join(data_dir, filename) for filename in filenames]

def main():
    filenames = get_data_filenames()
    for filename in filenames:
        process_race_results(filename)

if __name__ == "__main__":
    main()
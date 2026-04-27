Chicago Traffic Camera Analysis

CS 341 – Project 2
Author: Alejandro Camacho

Overview

This project is a Python-based command-line application that analyzes traffic camera data from Chicago using a SQLite database.

The program allows users to explore:

Red light and speed camera locations
Traffic violations over time
Trends by year, month, and location
Visualizations of violations and camera locations
🛠️ Technologies Used
Python 3
SQLite (sqlite3)
Matplotlib (for data visualization)

---------------------------------------------------------------

Project Structure
.
├── main.py
├── chicago-traffic-cameras.db
├── chicago.png
└── README.md

---------------------------------------------------------------
How to Run
1. Install Dependencies

Make sure you have Python installed. Then install matplotlib:

pip install matplotlib
2. Run the Program
python main.py
3. Required Files

Make sure these files are in the same directory:

chicago-traffic-cameras.db
chicago.png

---------------------------------------------------------------

Features
1. Intersection Lookup

Search for intersections using wildcards (%, _).

2. Camera Lookup

Find all red light and speed cameras at a specific intersection.

3. Violation Percentage

View the percentage of red light vs speed violations for a given date.

4. Cameras per Intersection

Displays how many cameras exist at each intersection.

5. Violations by Year

Analyze total violations at each intersection for a selected year.

6. Violations by Camera
View yearly violations for a specific camera
Option to generate a graph

7. Monthly Violations
Shows violations per month for a camera
Optional visualization

8. Compare Violations

Compare red light vs speed violations across an entire year.

#
# header comment! Overview, name, etc.
# Alejandro Camacho
# HW 2 CS 341 
import sqlite3
import matplotlib.pyplot as plt

##################################################################  
#
# print_stats
#
# Given a connection to the database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbCursor):
    print("General Statistics:")
    
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")
    row = dbCursor.fetchone()
    print("  Number of Red Light Cameras:", f"{row[0]:,}")

    dbCursor.execute("SELECT count(Camera_ID) from SpeedCameras")
    row = dbCursor.fetchone()
    print("  Number of Speed Cameras:", f"{row[0]:,}")

    dbCursor.execute("SELECT COUNT(Num_Violations) from RedViolations")
    row = dbCursor.fetchone()
    print("  Number of Red Light Camera Violation Entries:", f"{row[0]:,}")

    dbCursor.execute("SELECT COUNT(Num_Violations) from SpeedViolations")
    row = dbCursor.fetchone()
    print("  Number of Speed Camera Violation Entries:", f"{row[0]:,}")

    dbCursor.execute("""
            SELECT MIN(Violation_Date), MAX(Violation_Date)
            FROM RedViolations
        """)
    row = dbCursor.fetchone()
    print(f"  Range of Dates in the Database: {row[0]} to {row[1]}")

    dbCursor.execute("SELECT SUM(Num_Violations) FROM RedViolations")
    row = dbCursor.fetchone()
    print("  Total Number of Red Light Camera Violations:", f"{row[0]:,}")

    dbCursor.execute("SELECT SUM(Num_Violations) FROM SpeedViolations")
    row = dbCursor.fetchone()
    print("  Total Number of Speed Camera Violations:", f"{row[0]:,}")
    
##################################################################  
#
# main
dbConn = sqlite3.connect("chicago-traffic-cameras.db")
dbCursor = dbConn.cursor()

print("Project 2: Chicago Traffic Camera Analysis")
print("CS 341, Spring 2026")
print()
print("This application allows you to analyze various")
print("aspects of the Chicago traffic camera database.")
print()
print_stats(dbCursor)
print()

print("Select a menu option: ")
print("  1. Find an intersection by name")
print("  2. Find all cameras at an intersection")
print("  3. Percentage of violations for a specific date")
print("  4. Number of cameras at each intersection")
print("  5. Number of violations at each intersection, given a year")
print("  6. Number of violations by year, given a camera ID")
print("  7. Number of violations by month, given a camera ID and year")
print("  8. Compare the number of red light and speed violations, given a year")
print("  9. Find cameras located on a street")
print("or x to exit the program.")
userInput = input()





print("Exiting program.")
#
# done
#
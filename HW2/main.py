#
# header comment! Overview, name, etc.
# Alejandro Camacho
# HW 2 CS 341 
import sqlite3
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta

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
    print(f"  Range of Dates in the Database: {row[0]} - {row[1]}")

    dbCursor.execute("SELECT SUM(Num_Violations) FROM RedViolations")
    row = dbCursor.fetchone()
    print("  Total Number of Red Light Camera Violations:", f"{row[0]:,}")

    dbCursor.execute("SELECT SUM(Num_Violations) FROM SpeedViolations")
    row = dbCursor.fetchone()
    print("  Total Number of Speed Camera Violations:", f"{row[0]:,}")
    
##################################################################  
#

##################################################################
#
# intersectionLookup
#
# Allows user to lookup an intersection by name
#
def intersectionLookup(dbCursor):
    intersectionName = input("Enter the name of the intersection to find (wildcards _ and % allowed): ")

    dbCursor.execute(
        "SELECT Intersection_ID, Intersection from Intersections WHERE Intersection LIKE ? ORDER BY Intersection ASC", 
        (intersectionName,)
    )

    results = dbCursor.fetchall()
    if not results:
        print()
        print("No intersections matching that name were found.")
        return
    
    print()
    for row in results:
        print(f"{row[0]} : {row[1]}")
    print()
##################################################################
#

##################################################################
#
# cameraLookup
#
# Allows user to lookup all that cameras at a given intersection
#
def cameraLookup(dbCursor):
    cameraName = input("Enter the name of the intersection (no wildcards allowed): ")
    print()
    print()

    dbCursor.execute("""
        SELECT RedCameras.Camera_ID, RedCameras.Address
        FROM RedCameras
        JOIN Intersections
           ON Intersections.Intersection_ID = RedCameras.Intersection_ID
        WHERE Intersections.Intersection = ?
        ORDER BY Camera_ID
        """, (cameraName,))
    
    red_results = dbCursor.fetchall()

    if red_results:
        print("Red Light Cameras:")
        print()
        for row in red_results:
            print(f"   {row[0]} : {row[1]}")
        print()
    else:
        print("No red light cameras found at that intersection.")
        print()
    
    dbCursor.execute("""
        SELECT SpeedCameras.Camera_ID, SpeedCameras.Address
        FROM SpeedCameras
        JOIN Intersections
           ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
        WHERE Intersections.Intersection = ?
        ORDER BY Camera_ID
        """, (cameraName,))
    
    speed_results = dbCursor.fetchall()

    if speed_results:
        print("Speed Cameras:")
        print()
        for row in speed_results:
            print(f"   {row[0]} : {row[1]}")
    else:
        if red_results:
            print("No speed cameras found at that intersection.")
        else:
            print("No speed cameras found at that intersection.")
            
    print()
##################################################################
#

##################################################################
#
# violationPercent
#
# Allows user to find the percentage of violations for a certain date
#
def violationPercent(dbCursor):
    dateWanted = input("Enter the date that you would like to look at (format should be YYYY-MM-DD): ")
    print()

    dbCursor.execute("SELECT SUM(Num_Violations) FROM RedViolations WHERE Violation_Date = ?", (dateWanted,))
    redViolations = dbCursor.fetchone()[0]
    redViolations = 0 if redViolations is None else redViolations


    dbCursor.execute("SELECT SUM(Num_Violations) FROM SpeedViolations WHERE Violation_Date = ?", (dateWanted,))
    speedViolations = dbCursor.fetchone()[0]
    speedViolations = 0 if speedViolations is None else speedViolations

    totalViolations = redViolations + speedViolations

    if totalViolations == 0:
        print("No violations on record for that date.")
        print()
        return
    
    redPercent = (redViolations / totalViolations) * 100
    speedPercent = (speedViolations / totalViolations) * 100

    print(f"Number of Red Light Violations: {redViolations:,} ({redPercent:.3f}%)")
    print(f"Number of Speed Violations: {speedViolations:,} ({speedPercent:.3f}%)")
    print(f"Total Number of Violations: {totalViolations:,}")
    print()
##################################################################
#

##################################################################
#
# numCameras
#
# Allows user to find  the number of cameras at a certain intersection
#
def numCameras(dbCursor):
    print()

    dbCursor.execute("""
        SELECT Intersections.Intersection, Intersections.Intersection_ID, COUNT(RedCameras.Camera_ID) AS totalCameras
        FROM Intersections
        JOIN RedCameras
        ON RedCameras.Intersection_ID = Intersections.Intersection_ID
        GROUP BY Intersections.Intersection_ID
        ORDER BY totalCameras DESC""")
    
    redRows = dbCursor.fetchall()
    
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras")
    redTotal = dbCursor.fetchone()[0]

    
    print("Number of Red Light Cameras at Each Intersection")
    for intersect, id, total in redRows:
        percent = (total / redTotal) * 100
        print(f"  {intersect} ({id}) : {total} ({percent:.3f}%)")

    print()

    dbCursor.execute("""
        SELECT Intersections.Intersection, Intersections.Intersection_ID, COUNT(SpeedCameras.Camera_ID) AS totalCameras
        FROM Intersections
        JOIN SpeedCameras
        ON SpeedCameras.Intersection_ID = Intersections.Intersection_ID
        GROUP BY Intersections.Intersection_ID
        ORDER BY totalCameras DESC""")
    
    speedRows = dbCursor.fetchall()
    
    dbCursor.execute("SELECT COUNT(*) FROM SpeedCameras")
    speedTotal = dbCursor.fetchone()[0]


    print("Number of Speed Cameras at Each Intersection")
    for intersect, id, total in speedRows:
        percent = (total / speedTotal) * 100
        print(f"  {intersect} ({id}) : {total} ({percent:.3f}%)")
    
    print()

##################################################################
#

##################################################################
#
# violationsYear
#
# Allows user to find number of violations at an intersection by a year
#
def violationsYear(dbCursor): 
    yearInput = input("Enter the year that you would like to analyze: ")
    print()

    dbCursor.execute("""
        SELECT Intersections.Intersection,
        Intersections.Intersection_ID,
        SUM(RedViolations.Num_Violations)
        FROM Intersections
        JOIN RedCameras
        ON RedCameras.Intersection_ID = Intersections.Intersection_ID
        JOIN RedViolations
        ON RedViolations.Camera_ID = RedCameras.Camera_ID
        WHERE strftime('%Y', RedViolations.Violation_Date) = ?
        GROUP BY Intersections.Intersection_ID
        ORDER BY SUM(RedViolations.Num_Violations) DESC
                     """, (yearInput,))
    redRows = dbCursor.fetchall()

    dbCursor.execute("SELECT SUM(Num_Violations) FROM RedViolations WHERE strftime('%Y', Violation_Date) = ?", (yearInput,))
    redTotal = dbCursor.fetchone()[0]
    redTotal = 0 if redTotal is None else redTotal

    print(f"Number of Red Light Violations at Each Intersection for {yearInput}")
    if redTotal == 0:
        print("No red light violations on record for that year.")
    else:
        for intersect, id, total in redRows:
            percent = (total / redTotal) * 100
            print(f"  {intersect} ({id}) : {total:,} ({percent:.3f}%)")
        print(f"Total Red Light Violations in {yearInput} : {redTotal:,}")
    print()
    
    dbCursor.execute("""
        SELECT Intersections.Intersection,
        Intersections.Intersection_ID,
        SUM(SpeedViolations.Num_Violations)
        FROM Intersections
        JOIN SpeedCameras
        ON SpeedCameras.Intersection_ID = Intersections.Intersection_ID
        JOIN SpeedViolations
        ON SpeedViolations.Camera_ID = SpeedCameras.Camera_ID
        WHERE strftime('%Y', SpeedViolations.Violation_Date) = ?
        GROUP BY Intersections.Intersection_ID
        ORDER BY SUM(SpeedViolations.Num_Violations) DESC
                     """, (yearInput,))
    speedRows = dbCursor.fetchall()

    dbCursor.execute("SELECT SUM(Num_Violations) FROM SpeedViolations WHERE strftime('%Y', Violation_Date) = ?", (yearInput,))
    speedTotal = dbCursor.fetchone()[0]
    speedTotal = 0 if speedTotal is None else speedTotal

    print(f"Number of Speed Violations at Each Intersection for {yearInput}")
    if speedTotal == 0:
        print("No speed violations on record for that year.")
    else:
        for intersect, id, total in speedRows:
            percent = (total/speedTotal) * 100
            print(f"  {intersect} ({id}) : {total:,} ({percent:.3f}%)")
        print(f"Total Speed Violations in {yearInput} : {speedTotal:,}")
    print()


##################################################################
#

##################################################################
#
# violationsCamera
#
# Allows user to find number of violations at an intersection by a year
#
def violationsCamera(dbCursor):
    print()
    cameraID = input("Enter a camera ID: ")
    print()

    dbCursor.execute("""
        SELECT 
        strftime('%Y', Violation_Date) AS Year,
        SUM(Num_Violations) AS Total
        FROM RedViolations
        WHERE Camera_ID = ?
        GROUP BY Year
        
        UNION ALL
        
                     
        SELECT 
        strftime('%Y', Violation_Date) AS Year,
        SUM(Num_Violations) AS Total
        FROM SpeedViolations
        WHERE Camera_ID = ?
        GROUP BY Year
        ORDER BY Year ASC""", (cameraID, cameraID))
    
    rows = dbCursor.fetchall()

    if not rows:
        print("No cameras matching that ID were found in the database.")
        print()
        return

    print(f"Yearly Violations for Camera {cameraID}")
    for year, totals in rows:
        print(f"{year} : {totals:,}")
    print()

    plotInput = input("Plot? (y/n) ")

    if plotInput.lower() != 'y':
        print()
        return
    
    years = [int(y) for (y,t) in rows]
    totals = [t for (y,t) in rows]
    plt.plot(years, totals)
    plt.title(f"Yearly Violations for Camera {cameraID}")
    plt.xlabel("Year")
    plt.ylabel("Number of Violations")

    plt.show()
    print()
    return

##################################################################
#

##################################################################
#
# violationsMonth
#
# Allows user to find number of violations by month given the camera ID and year
#
def violationsMonth(dbCursor):
    print()
    
    cameraID = input("Enter a camera ID: ")
    print()

    dbCursor.execute("""
        SELECT 1 FROM RedCameras WHERE Camera_ID = ?
        UNION
        SELECT 1 FROM SpeedCameras WHERE Camera_ID = ?;
    """, (cameraID, cameraID))

    exists = dbCursor.fetchone()

    if not exists:
        print("No cameras matching that ID were found in the database.")
        print()
        return

    yearInput = input("Enter a year: ")
    print()
    
    print(f"Monthly Violations for Camera {cameraID} in {yearInput}")

    dbCursor.execute("""
        SELECT strftime('%m', Violation_Date) AS Month,
               SUM(Num_Violations) AS Total
        FROM RedViolations
        WHERE Camera_ID = ?
          AND strftime('%Y', Violation_Date) = ?
        GROUP BY Month

        UNION ALL

        SELECT strftime('%m', Violation_Date) AS Month,
               SUM(Num_Violations) AS Total
        FROM SpeedViolations
        WHERE Camera_ID = ?
          AND strftime('%Y', Violation_Date) = ?
        GROUP BY Month

        ORDER BY Month ASC;
    """, (cameraID, yearInput, cameraID, yearInput))
    
    rows = dbCursor.fetchall()

    for month, total in rows:
        print(f"{month}/{yearInput} : {total:,}")
    
    print()
    
    plotInput = input("Plot? (y/n) ")
    print()

    if plotInput.lower() != 'y':
        return

    if not rows:
        return

    months = [int(m) for (m, t) in rows]
    totals = [t for (m, t) in rows]

    plt.plot(months, totals)
    plt.title(f"Monthly Violations for Camera {cameraID} in {yearInput}")
    plt.xlabel("Month")
    plt.ylabel("Number of Violations")
    plt.show()


##################################################################
#


##################################################################
#
# compareViolations
#
# Allows user to compare the number of red light and speed violations with input of a year
#
from datetime import datetime, date, timedelta

def compareViolations(dbCursor):
    print("Enter a year: ")
    year = input()

    def first_last_5(table):
        sql = f"""
            SELECT date(Violation_Date) AS Day, SUM(Num_Violations) AS Total
            FROM {table}
            WHERE strftime('%Y', Violation_Date) = ?
            GROUP BY Day
            ORDER BY Day {{order}}
            LIMIT 5
        """
        dbCursor.execute(sql.format(order="ASC"), (year,))
        first = dbCursor.fetchall()

        dbCursor.execute(sql.format(order="DESC"), (year,))
        last = list(reversed(dbCursor.fetchall()))

        return first + last

    def daily_map(table):
        dbCursor.execute(f"""
            SELECT date(Violation_Date) AS Day, SUM(Num_Violations) AS Total
            FROM {table}
            WHERE strftime('%Y', Violation_Date) = ?
            GROUP BY Day
            ORDER BY Day ASC
        """, (year,))
        return {
            datetime.strptime(d, "%Y-%m-%d").date(): total
            for d, total in dbCursor.fetchall()
        }

    red = first_last_5("RedViolations")
    speed = first_last_5("SpeedViolations")

    if not red and not speed:
        print("Red Light Violations:\nSpeed Violations:")
    else:
        print("Red Light Violations:")
        for d, t in red:
            print(f"{d} {t}")

        print("Speed Violations:")
        for d, t in speed:
            print(f"{d} {t}")

    print()

    if input("Plot? (y/n) ").lower() != "y":
        print()
        return

    red_map = daily_map("RedViolations")
    speed_map = daily_map("SpeedViolations")

    y = int(year)
    start = date(y, 1, 1)
    end = date(y, 12, 31)

    num_days = (end - start).days + 1

    x_vals = list(range(num_days))
    red_totals = []
    speed_totals = []

    for i in range(num_days):
        cur_day = start + timedelta(days=i)
        red_totals.append(red_map.get(cur_day, 0))
        speed_totals.append(speed_map.get(cur_day, 0))

    plt.figure()
    plt.plot(x_vals, red_totals, label="Red Light", color='red')
    plt.plot(x_vals, speed_totals, label="Speed", color='orange')

    plt.xticks([0, 50, 100, 150, 200, 250, 300, 350])

    plt.title(f"Violations Each Day of {year}")
    plt.xlabel("Day")
    plt.ylabel("Number of Violations")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print()
##################################################################
#

##################################################################
#
# compareViolations
#
# Allows a user to find the cameras at a street
#
def camerasAtStreet(dbCursor):
    print("Enter a street name: ")
    streetName = input()
    fortmattedInput = f"%{streetName}%"

    print()

    dbCursor.execute("""
        SELECT 
        Camera_ID,
        Address,
        Latitude,
        Longitude
        FROM RedCameras
        WHERE Address LIKE ?
        ORDER BY Camera_ID ASC
                     """,(fortmattedInput,))
    
    redCameras = dbCursor.fetchall()
    
    dbCursor.execute("""
        SELECT 
        Camera_ID,
        Address,
        Latitude,
        Longitude
        FROM SpeedCameras
        WHERE Address LIKE ?
        ORDER BY Camera_ID ASC
                     """,(fortmattedInput,))
    
    speedCameras = dbCursor.fetchall()

    if not redCameras and not speedCameras:
        print("There are no cameras located on that street.")
        print()
        return
    else:
        print(f"List of Cameras Located on Street: {streetName}")
        print ("  Red Light Cameras:")
        for id, address, lat, long in redCameras:
            print(f"     {id} : {address} {lat, long}")

        print("  Speed Cameras:")
        for id, address, lat, long in speedCameras:
            print(f"     {id} : {address} {lat, long}")

    print()

    print("Plot? (y/n) ")
    plotInput = input()
    print()

    if plotInput.lower() != 'y':
        return
    
    x, y, labels = [], [], []

    for id, address, lat, long in redCameras + speedCameras:
        if lat is None or long is None:
            continue
        x.append(long)
        y.append(lat)
        labels.append(str(id))

    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    plt.imshow(image, extent=xydims)

    plt.title(f"Cameras on {streetName}")
    plt.plot(x, y, "o", color="red")

    for xi, yi, lab in zip(x, y, labels):
        plt.annotate(
            lab,
            (xi, yi),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
            fontsize=8
        )

    plt.tight_layout()
    plt.show()
    print()
    

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

while True:
    print("""Select a menu option:\n  1. Find an intersection by name
  2. Find all cameras at an intersection
  3. Percentage of violations for a specific date
  4. Number of cameras at each intersection
  5. Number of violations at each intersection, given a year
  6. Number of violations by year, given a camera ID
  7. Number of violations by month, given a camera ID and year
  8. Compare the number of red light and speed violations, given a year
  9. Find cameras located on a street
or x to exit the program.""")
    
    print("Your choice --> ")
    userInput = input().strip()

    if userInput == '1':
        intersectionLookup(dbCursor)
    elif userInput == '2':
        cameraLookup(dbCursor)
    elif userInput == '3':
        violationPercent(dbCursor)
    elif userInput == '4':
        numCameras(dbCursor)
    elif userInput == '5':
        violationsYear(dbCursor)
    elif userInput == '6':
        violationsCamera(dbCursor)
    elif userInput == '7':
        violationsMonth(dbCursor)
    elif userInput == '8':
        compareViolations(dbCursor)
    elif userInput == '9':
        camerasAtStreet(dbCursor)
    elif userInput == 'x':
        break
    else:
        print("Error, unknown command, try again...\n")
print("Exiting program.")
#
# done
#
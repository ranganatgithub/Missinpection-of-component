Project Steps
1. System Overview
The system performs the following functions:

Continuously monitors the screen using OpenCV to detect barcode colors.
Analyzes the scanned image and determines validity (green = valid, red = invalid).
If invalid, triggers an alert via Tkinter popup and an Arduino buzzer.
Requires the line leader to scan their ID to resolve the issue.
Stores all data in an SQL database for tracking.
Automatically resumes production after resolution.


2. Required Technologies
Python Libraries: OpenCV, Tkinter, Serial, SQLite/MySQL
Hardware: Arduino with a buzzer and RFID/ID scanner
Machine Learning: Image processing for color detection

import cv2, numpy as np, tkinter as tk, serial, sqlite3
from datetime import datetime
from tkinter import messagebox

# Function to monitor screen and detect barcode colors
def monitor_screen():
    cap = cv2.VideoCapture(0)
    red_lower, red_upper = np.array([0, 120, 70]), np.array([10, 255, 255])
    green_lower, green_upper = np.array([40, 40, 40]), np.array([80, 255, 255])
    while True:
        ret, frame = cap.read()
        if not ret: break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red_mask, green_mask = cv2.inRange(hsv, red_lower, red_upper), cv2.inRange(hsv, green_lower, green_upper)
        if cv2.countNonZero(red_mask) > 1000: return "RED"
        elif cv2.countNonZero(green_mask) > 1000: return "GREEN"
        cv2.imshow("Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release(), cv2.destroyAllWindows()

# Function to show Tkinter alert and trigger Arduino buzzer
def show_alert():
    root = tk.Tk(); root.withdraw()
    messagebox.showerror("Error", "Invalid Component Detected! Line Stopped.")
    arduino = serial.Serial('COM3', 9600); arduino.write(b'1'); arduino.close()
    request_leader_scan(); root.destroy()

# Function to scan leader ID and store in database
def request_leader_scan():
    operator_id = input("Scan your ID to resume operation: ")
    store_data(operator_id, "RED")
    print("ID accepted. Resuming production.")

# Function to store data in SQL database
def store_data(operator_id, status):
    conn = sqlite3.connect('production_log.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS log 
                      (timestamp TEXT, operator_id TEXT, status TEXT)''')
    cursor.execute("INSERT INTO log VALUES (?, ?, ?)", 
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operator_id, status))
    conn.commit(), conn.close()

# Main function to run the monitoring system
def main():
    print("Starting Component Monitoring System...")
    while True:
        if monitor_screen() == "RED": show_alert()
        else: print("Component is valid, continuing production.")

if __name__ == "__main__":
    main()



Here's the complete code in a concise format that fits on one page:

python
Copy
Edit
import cv2, numpy as np, tkinter as tk, serial, sqlite3
from datetime import datetime
from tkinter import messagebox

# Function to monitor screen and detect barcode colors
def monitor_screen():
    cap = cv2.VideoCapture(0)
    red_lower, red_upper = np.array([0, 120, 70]), np.array([10, 255, 255])
    green_lower, green_upper = np.array([40, 40, 40]), np.array([80, 255, 255])
    while True:
        ret, frame = cap.read()
        if not ret: break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red_mask, green_mask = cv2.inRange(hsv, red_lower, red_upper), cv2.inRange(hsv, green_lower, green_upper)
        if cv2.countNonZero(red_mask) > 1000: return "RED"
        elif cv2.countNonZero(green_mask) > 1000: return "GREEN"
        cv2.imshow("Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release(), cv2.destroyAllWindows()

# Function to show Tkinter alert and trigger Arduino buzzer
def show_alert():
    root = tk.Tk(); root.withdraw()
    messagebox.showerror("Error", "Invalid Component Detected! Line Stopped.")
    arduino = serial.Serial('COM3', 9600); arduino.write(b'1'); arduino.close()
    request_leader_scan(); root.destroy()

# Function to scan leader ID and store in database
def request_leader_scan():
    operator_id = input("Scan your ID to resume operation: ")
    store_data(operator_id, "RED")
    print("ID accepted. Resuming production.")

# Function to store data in SQL database
def store_data(operator_id, status):
    conn = sqlite3.connect('production_log.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS log 
                      (timestamp TEXT, operator_id TEXT, status TEXT)''')
    cursor.execute("INSERT INTO log VALUES (?, ?, ?)", 
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operator_id, status))
    conn.commit(), conn.close()

# Main function to run the monitoring system
def main():
    print("Starting Component Monitoring System...")
    while True:
        if monitor_screen() == "RED": show_alert()
        else: print("Component is valid, continuing production.")

if __name__ == "__main__":
    main()


#Arduino Code (Upload separately to the board)
int buzzer = 9;
void setup() { pinMode(buzzer, OUTPUT); Serial.begin(9600); }
void loop() {
  if (Serial.available() > 0 && Serial.read() == '1') {
    digitalWrite(buzzer, HIGH); delay(3000); digitalWrite(buzzer, LOW);
  }
}

import time
from Motor import *
from Infrared_Obstacle_Avoidance import *
from Ultrasonic import *
from Led import *
import RPi.GPIO as GPIO

# Initialize modules
motor = Motor()
ultrasonic = Ultrasonic()
led = Led()
infrared = Infrared_Obstacle_Avoidance()

# GPIO Pins for lane detection
LEFT_LANE = 14
RIGHT_LANE = 15
INTERSECTION = 23  # Pin to detect intersections

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_LANE, GPIO.IN)
GPIO.setup(RIGHT_LANE, GPIO.IN)
GPIO.setup(INTERSECTION, GPIO.IN)

# Functions
def lane_following():
    """Keep the car within the lane."""
    if GPIO.input(LEFT_LANE) == 1 and GPIO.input(RIGHT_LANE) == 1:
        motor.setMotorModel(1000, 1000, 1000, 1000)  # Move forward
    elif GPIO.input(LEFT_LANE) == 1:
        motor.setMotorModel(800, 800, 1000, 1000)  # Adjust to the right
    elif GPIO.input(RIGHT_LANE) == 1:
        motor.setMotorModel(1000, 1000, 800, 800)  # Adjust to the left
    else:
        motor.setMotorModel(0, 0, 0, 0)  # Stop if off-lane

def detect_object():
    """Detect object and perform lane change."""
    distance = ultrasonic.get_distance()
    if distance < 20:  # Object detected within 20 cm
        lane_change()

def lane_change():
    """Switch lanes to avoid an object."""
    motor.setMotorModel(-1500, -1500, 1500, 1500)  # Turn left
    time.sleep(1.5)  # Adjust based on real-world turning angle
    motor.setMotorModel(1000, 1000, 1000, 1000)  # Move forward
    time.sleep(2)  # Move ahead in the new lane
    return_to_lane()

def return_to_lane():
    """Rejoin the original lane."""
    motor.setMotorModel(1500, 1500, -1500, -1500)  # Turn right
    time.sleep(1.5)
    motor.setMotorModel(1000, 1000, 1000, 1000)  # Move forward

def intersection_control():
    """Stop at intersection, scan for obstacles, and proceed if clear."""
    if GPIO.input(INTERSECTION) == 1:  # Intersection detected
        motor.setMotorModel(0, 0, 0, 0)  # Stop
        print("Intersection detected. Scanning...")
        time.sleep(2)
        if ultrasonic.get_distance() > 20:  # No object detected
            print("Intersection clear. Proceeding...")
            motor.setMotorModel(1000, 1000, 1000, 1000)
        else:
            print("Object detected at intersection. Waiting...")
            time.sleep(2)

# Main Program
if __name__ == "__main__":
    print("Starting car operation...")
    try:
        while True:
            lane_following()
            detect_object()
            intersection_control()
    except KeyboardInterrupt:
        print("Stopping car...")
        motor.setMotorModel(0, 0, 0, 0)  # Stop motors on exit
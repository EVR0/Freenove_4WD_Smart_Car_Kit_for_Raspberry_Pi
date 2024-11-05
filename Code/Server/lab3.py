import time
import Motor
import Ultrasonic
import Buzzer
import Led
import RPi.GPIO as GPIO
from Infrared_Obstacle_Avoidance import *

Us = Ultrasonic.Ultrasonic()
Motor = Motor.Motor()
Buzzer = Buzzer.Buzzer()
Led = Led.Led()


IR_LEFT = 17    
IR_MIDDLE = 27   
IR_RIGHT = 22    

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_LEFT, GPIO.IN)
    GPIO.setup(IR_MIDDLE, GPIO.IN)
    GPIO.setup(IR_RIGHT, GPIO.IN)


def follow_line():
    if not GPIO.input(IR_LEFT) and GPIO.input(IR_MIDDLE) and not GPIO.input(IR_RIGHT):
        
        Motor.setMotorModel(2000, 2000, 2000, 2000)
        Led.ledMode('2')  
    elif not GPIO.input(IR_LEFT) and not GPIO.input(IR_MIDDLE) and GPIO.input(IR_RIGHT):
       
        Motor.setMotorModel(2000, 2000, 1500, 1500)
        Led.ledMode('3')  
    elif GPIO.input(IR_LEFT) and not GPIO.input(IR_MIDDLE) and not GPIO.input(IR_RIGHT):
        
        Motor.setMotorModel(1500, 1500, 2000, 2000)
        Led.ledMode('4') 
    elif not GPIO.input(IR_LEFT) and not GPIO.input(IR_MIDDLE) and not GPIO.input(IR_RIGHT):
        
        Motor.setMotorModel(2000, 2000, 1500, 1500)
        Led.ledMode('3')  
    else:
        
        Motor.setMotorModel(0, 0, 0, 0)
        Led.ledMode('1') 


def avoid_obstacle():
    Motor.setMotorModel(0, 0, 0, 0)
    Buzzer.run("1")  
    time.sleep(1)
    
   
    Motor.setMotorModel(2000, -2000, 2000, -2000)  
    time.sleep(0.5)
    Motor.setMotorModel(2000, 2000, 2000, 2000)  
    time.sleep(1)
    
   
    while GPIO.input(IR_MIDDLE) == True:
        Motor.setMotorModel(1500, 1500, 1500, 1500)
    Motor.setMotorModel(0, 0, 0, 0)  
    Buzzer.run("0")  


def main():
    setup()
    try:
        while True:
            distance = Us.get_distance()
            
            if distance <= 20:
                
                Led.ledMode('5')  
                avoid_obstacle()
            else:
                
                follow_line()
                
            time.sleep(0.1)  
            
    except KeyboardInterrupt:
        Motor.setMotorModel(0, 0, 0, 0)
        Buzzer.run("0")
        Led.ledMode('1')
        GPIO.cleanup()
        print("\nEnd of program")

if __name__ == "__main__":
    main()

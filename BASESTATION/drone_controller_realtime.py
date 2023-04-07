# This file is the drone controller, the goal of this script is to control the drone through its
import os
import cv2
import log_helpers
from djitellopy import tello
import time

##############################


##############################

def pre_flight_checks(drone):
    if drone.get_battery() < 30:
        print("Battery Too Low For Flight: " + str(drone.get_battery()))
        exit()
    else:
        print("Ready for Flight with battery life: " + str(drone.get_battery()))

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def image_capture(drone, lat, lon):
    img = drone.get_frame_read().frame
    cv2.waitKey(1)
    
    name = log_helpers.save(img, lat, lon)

    status = cv2.imwrite(name,img)
    
def surveillance(drone, lat, lon):
    rotate = 0
    offset1 = 1
    offset2 = 2
    while rotate < 8:
        image_capture(drone, lat, lon)
        if rotate % 2 == 0:  
            drone.rotate_clockwise(45+offset1)
        else:
            drone.rotate_clockwise(45+offset2)
        rotate += 1
    
""" def execute_flight_path(drone):
    image_capture(drone)
    drone.takeoff()
    time.sleep(3)
    # surveillance(drone)
    #go_xyz_speed(x, y, z, speed)
    drone.go_xyz_speed(0,0,50,40)
    surveillance(drone)
    #up and right by 200 cm
    drone.go_xyz_speed(50,0,0,40)
    surveillance(drone)
    drone.go_xyz_speed(-50,0,0,40)
    drone.land() """
    
""" def execute_flight_path(drone):
    image_capture(drone)
     """
    
""" def startup_script():
    print("Connecting to tello")
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    pre_flight_checks(drone)
    
    
   

if __name__ == "__main__":
    # initialize the system configurations and store it
    
    
    
    
    
    execute_flight_path(drone)
    
    
    
    
     """
    
   
# This file is the drone controller, the goal of this script is to control the drone through its
import cv2
import log_helpers

##############################


##############################

def pre_flight_checks(drone):
    if drone.get_battery() < 30:
        print("Battery Too Low For Flight: " + str(drone.get_battery()))
        exit()
    else:
        print("Ready for Flight with battery life: " + str(drone.get_battery()))

def image_capture(drone, lat, lon):
    img = drone.get_frame_read().frame
    cv2.waitKey(1)
    
    name = log_helpers.save(lat, lon)

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
    

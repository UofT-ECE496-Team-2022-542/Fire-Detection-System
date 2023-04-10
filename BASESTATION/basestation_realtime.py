from image_classifier import init_model, forward_pass
from log_helpers import get_image_filepaths, log_request, save
from datetime import datetime
import argparse
import os
from gps import get_point_at_distance

import drone_controller_realtime as drone_controller
from djitellopy import tello
import cv2
import time


#---------- GLOBAL VARIABLES ----------
# The address of the Backend's "log" route
BACKEND_IP_ADDRESS = '127.0.0.1' # Local Host
# BACKEND_IP_ADDRESS = ''# IP Address of server ipconfig/all
BACKEND_PORT = 5001 # Port
BACKEND_LOG_ADDRESS = 'http://' + BACKEND_IP_ADDRESS + ':' + str(BACKEND_PORT) + '/log'
#BACKEND_LOG_ADDRESS = 'http://icarusfiredetectionsystem.pythonanywhere.com/log'
# The directory where images are stored
IMAGE_DIR = None
# The image classifier model
#MODEL = init_model('MODELS/demo_8.pth')
MODEL = init_model('MODELS/ResNet18.pth')
# The ID of this instance of the drone
DRONE_ID = 0
# Current Lat/Lon of Drone
LAT = 0
LON = 0

#---------- FUNCTIONS ----------
# Executes log_request for each image in the specified folder
def log_request_folder(dir_path, print_progress=False, proper_filename=True):
    for image_filepath in get_image_filepaths(dir_path, proper_filename):
        # Retrieve metadata from filename only if proper filenames in dir_path
        filepath, lat, lon = None, None, None
        if proper_filename:
            filepath = image_filepath[0]
            lat = image_filepath[2]
            lon = image_filepath[3]
        else: 
            filepath = image_filepath
            lat = 42
            lon = 70

        # Generate additional metadata
        prediction = forward_pass(MODEL, filepath)
        # time_captured = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_captured = image_filepath[1]

        # Execute the log request
        log_request(
            url=BACKEND_LOG_ADDRESS,
            drone_id=DRONE_ID,
            time_captured=time_captured,
            lat=lat,
            lon=lon,
            prediction=prediction,
            image_filepath=filepath,
            print_progress=print_progress
        )
        os.remove(image_filepath[0])
    return

def transfer_images():
    int1 = time.time()
    os.system('networksetup -setairportnetwork en0 "UofT" ')  
    time.sleep(20)
    log_request_folder(dir_path='drone_images')
    int2 = time.time()
    print(int2 - int1)
    os.system('networksetup -setairportnetwork en0 "TELLO-994E04" ')
    #change to drone wifi
    time.sleep(0.5)
    
def transfer_images_local():
    int1 = time.time()
    #os.system('networksetup -setairportnetwork en0 "Fighters" ')  
    #time.sleep(2)
    log_request_folder(dir_path='drone_images')
    int2 = time.time()
    print(int2 - int1)
    #os.system('networksetup -setairportnetwork en0 "TELLO-994E04" ')
    #change to drone wifi
    #time.sleep(0.5)
    
# Enable this code when showing online host and no flight
def execute_flight_path(drone):
    while True:
        drone_controller.image_capture(drone, LAT, LON)
        #transfer_images()
        transfer_images_local()
        
# Enable this code when showing online but with flying
""" def execute_flight_path(drone):
    drone.takeoff()
    drone.go_xyz_speed(0,0,20,40)
    drone_controller.surveillance(drone, LAT, LON)
    transfer_images()
    drone.land() """
    
# Enable this when showing localhost but with flying
""" def execute_flight_path(drone):
    drone.takeoff()
    drone.go_xyz_speed(0,0,20,40)
    rotate = 0
    offset1 = 1
    offset2 = 2
    while rotate < 8:
        drone_controller.image_capture(drone, LAT, LON)
        transfer_images_local()
        if rotate % 2 == 0:  
            drone.rotate_clockwise(45+offset1)
        else:
            drone.rotate_clockwise(45+offset2)
        rotate += 1
    drone.land() """
    
    
    

#---------- MAIN ----------
if __name__ == '__main__':  
    parser = argparse.ArgumentParser()  
    parser.add_argument(  
        "--id",  
        type=int,  
        required=True,  
        help="A positive integer to serve as the ID for this drone"
    )  
    parser.add_argument(  
        "--test",  
        type=str,  
        required=False,  
        help="The test mode to start the program in. Available options: test_inputs"
    )  
    args = parser.parse_args()
    DRONE_ID = args.id

    # TEST MODES
    if args.test=='test_inputs':
        log_request_folder(dir_path='../TESTING/test_images', print_progress=True,  proper_filename=False)

    # REGULAR OPERATION
    else:
        os.system('networksetup -setairportnetwork en0 "UofT" ') 
        time.sleep(20)
        lat,lon = os.popen('curl ipinfo.io/loc').read().split(',')
        LAT = lat
        LON = lon
        os.system('networksetup -setairportnetwork en0 "TELLO-994E04" ')  
        time.sleep(2)
        print("Connecting to tello")
        drone = tello.Tello()
        drone.connect()
        
        drone.streamon()
        drone_controller.pre_flight_checks(drone)
        execute_flight_path(drone)
        
        drone.streamoff()
        exit()
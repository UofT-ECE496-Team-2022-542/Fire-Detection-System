from image_classifier import init_model, forward_pass
from log_helpers import get_image_filepaths, log_request
from datetime import datetime
import argparse
import os


#---------- GLOBAL VARIABLES ----------
# The address of the Backend's "log" route
BACKEND_LOG_ADDRESS = 'http://icarusfiredetectionsystem.pythonanywhere.com/log'
# The directory where images are stored
IMAGE_DIR = None
# The image classifier model
MODEL = init_model('MODELS/ResNet18.pth')
# The ID of this instance of the drone
DRONE_ID = 0

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
        time_captured = ''
        if proper_filename:
            time_captured = image_filepath[1]
        else:
            time_captured = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

        if proper_filename:
            os.remove(image_filepath[0])
    return

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
        log_request_folder(dir_path='drone_images')
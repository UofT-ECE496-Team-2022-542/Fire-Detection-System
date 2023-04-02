import os
import requests
import base64
import datetime

# Retrieves timestamp, lat, lon from image filename
def retrieve(image_name):
    name, ext = os.path.splitext(image_name)
    if ext != '.jpg':
        print("Invalid file. Was expecting a .jpg file.")
        return
    date, lat, lon = name.split(',')
    return date, lat, lon

#Saves images taken by the drone as 
def save(image, lat, lon):    
    time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')[:-3]
    name = f"./drone_images/{time},{lat},{lon}.jpg"
    return name

# Return a list of all filepaths in the given directory
def get_image_filepaths(dir_path, proper_filename=True):
    filepaths = []
    for filename in os.listdir(dir_path):
        f = os.path.join(dir_path, filename)
        if os.path.isfile(f):
            if proper_filename:
                date, lat, lon = retrieve(filename)
                filepaths.append([f, date, lat, lon])
            else:
                filepaths.append(f)
    return filepaths

#Performs a post request to backend for an image to be logged
def log_request(url, drone_id, time_captured, lat, lon, prediction, image_filepath, print_progress=False):
    #Convert image_filepath to blob
    with open(image_filepath, "rb") as image_file:
        image_blob = base64.b64encode(image_file.read()).decode('utf-8')
    #Create json for log request
    log_request = {
        "drone_id": drone_id,
        "time_captured": time_captured,
        "lat": lat,
        "lon": lon,
        "prediction": prediction,
        "image": image_blob,
    }
    if print_progress: print('Sending image to be logged...')
    log_response = requests.post(url, json=log_request)
    if print_progress: print('Response: {}'.format(log_response.text))
    return
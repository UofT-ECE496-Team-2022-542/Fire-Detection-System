# importing the os library  
import os  
# scanning the available Wi-Fi networks  
try:
    os.system('networksetup -setairportnetwork en0 "TELLO-994E04" ')  
except:
    print("Did not conenct")
# providing the Wi-Fi name as input  
# connecting to the provided Wi-Fi network  
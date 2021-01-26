import os
import platform
baudrate = 76800
theme = "light"
samplePerSecond = 20
plotStatus = 0
percentage = 0

config = {
		"host":"192.168.1.33",
		"port":5000,
}

links = {
  "olcum": "olcum",
  "yenikayit": "yenikayit",
  "people": ""
}
rec_folder = os.path.join("static","recs")
if(platform.system() == "Windows"):
  com_port = "COM7"
else:
  com_port = "/dev/ttyACM0"
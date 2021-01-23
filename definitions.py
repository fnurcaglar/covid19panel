import os
import platform
baudrate = 76800
theme = "light"
samplePerSecond = 20
plotStatus = 0
percentage = 0

config = {
		"host":"127.0.0.1",
		"port":5000,
}

links = {
  "measure": "measure",
#   "ayarlar": "ayarlar",
  "newperson": "newperson",
  "people": ""
}
rec_folder = os.path.join("static","recs")
if(platform.system() == "Windows"):
  com_port = "COM7"
else:
  com_port = "/dev/ttyACM0"
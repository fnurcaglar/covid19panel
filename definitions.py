import os
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
  "measure": "measure",
#   "ayarlar": "ayarlar",
  "newperson": "newperson",
  "people": ""
}
rec_folder = os.path.join("static","recs")
com_port = "/dev/ttyACM0"
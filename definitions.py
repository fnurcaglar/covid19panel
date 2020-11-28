import os
baudrate = 76800
theme = "light"
samplePerSecond = 20
plotStatus = 0
percentage = 0

config = {
		"host":"0.0.0.0",
		"port":5000,
		# "ip":"192.168.1.104:5000"
		"ip":"127.0.0.1:5000"
}

links = {
  "measure": "measure",
#   "ayarlar": "ayarlar",
  "newperson": "newperson",
  "people": ""
}
rec_folder = os.path.join("static","recs")
com_port = "COM21"
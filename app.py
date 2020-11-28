# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 17:19:03 2020
Edited on Thu Sep 3 01:32:13 2020

@author: Fatih Erdem
"""

from imports import *
from definitions import *

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "secret!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avokadio.db'
db = SQLAlchemy(app)
sio = SocketIO(app, logger = False)
migrate = Migrate(app, db)

class users(db.Model):
	id 			= db.Column(db.Integer, unique=True, primary_key=True)
	userno 		= db.Column(db.String(10)) #TODO: change to integer
	name 		= db.Column(db.String(10))
	phone 		= db.Column(db.Integer)
	gender 		= db.Column(db.String(10))
	height 		= db.Column(db.Integer)
	weight		= db.Column(db.Integer)
	leftpnif	= db.Column(db.Integer) 
	rightpnif	= db.Column(db.Integer) 
	globalpnif	= db.Column(db.Integer)
	birthyear	= db.Column(db.Integer)
	note		= db.Column(db.Integer)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def saveToExcel(sheet,data):
	data_split = data.split(',')
	row_num = int(data_split[1])
	sheet.cell(row=row_num+2, column=1).value = data_split[0]
	for i in range(1,9):
		sheet.cell(row=row_num+2, column=i+1).value = float(data_split[i])

@app.route("/settings")
def settings():
	return render_template("settings.html", ip=config["ip"] ,config=config, theme=theme, url=links["settings"])

@app.route("/measure", methods=['POST', 'GET'])
def measure():
	if request.method == 'POST':
		now = datetime.now().strftime("%y%m%d-%H%M%S")
		no = request.form.get('userno')
		userno = no.split()[0]
		user = users.query.filter_by(userno=userno).first()
		return render_template("plot.html", ip=config["ip"] ,config=config, theme=theme, url=links["measure"], user=user, users=users.query.all(), plotStatus=plotStatus, percentage=percentage, alerts=[0,0])
	else:
		return render_template("plot.html", ip=config["ip"] ,config=config, theme=theme, url=links["measure"],users=users.query.all() , plotStatus=plotStatus, percentage=percentage, alerts=[0,0])

@app.route("/")
def people():
	print(rec_folder)

	return render_template("users.html", ip=config["ip"] ,config=config,users=users.query.all(), theme=theme, url=links["people"])

@app.route("/people/<userno>")
def kullanici(userno):
	addr = os.path.join(rec_folder,userno,"excel")
	fileaddresses = glob(addr+"//*")
	filenames = []
	for file in fileaddresses:
		file = file.replace(addr,"")
		print(file)
		file = file[1:(len(file)-5)]
		print(file)
		name = datetime.strptime(file, '%y%m%d-%H%M%S')	
		file = name.strftime('%y%m%d-%H%M%S')
		filenames.append(file)
	numberofrecords = len(fileaddresses)
	user = users.query.filter_by(userno=userno).first()
	return render_template("user.html", ip=config["ip"] ,config=config, theme=theme, url=links["measure"], user=user, names=filenames, addresses=fileaddresses, number=numberofrecords)

@app.route("/newperson")
def kayit():
	return render_template("newperson.html", ip=config["ip"] ,config=config, theme=theme, url=links["newperson"])

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	global user_list
	if request.method == 'POST':
		userno = request.form['userno']
		name = request.form['name']
		phone = request.form['phone']
		gender = request.form['gender']
		height = request.form['height']
		weight = request.form['weight']
		leftpnif = request.form['leftpnif']
		rightpnif = request.form['rightpnif']
		globalpnif = request.form['globalpnif']
		birthyear = request.form['birthyear']
		note = request.form['note']
		new_user = users(userno=userno, name=name, phone=phone, gender=gender, height=height, weight=int(float(weight)*10), leftpnif=leftpnif, rightpnif=rightpnif, globalpnif=globalpnif, birthyear=birthyear, note=note)
		db.session.add(new_user)
		db.session.commit()
		user_rec_folder =os.path.join(rec_folder,userno)
		os.makedirs(user_rec_folder,exist_ok= True)
		user_rec_excel_folder 	= os.path.join(user_rec_folder,"excel")
		user_rec_csv_folder 	= os.path.join(user_rec_folder,"csv")
		os.makedirs(user_rec_excel_folder,exist_ok= True)
		os.makedirs(user_rec_csv_folder,exist_ok= True)
		new = name
	return render_template("newperson.html", ip=config["ip"] ,config=config, theme=theme, new=new)

@app.route('/measure/<userno>')
def newrec(userno):
	now = datetime.now().strftime("%y%m%d-%H%M%S")
	user = users.query.filter_by(userno=userno).first()
	return render_template("plot.html", ip=config["ip"] ,config=config, theme=theme, url=links["measure"], user=user, users=users.query.all(), plotStatus=plotStatus, percentage=percentage, alerts=[0,0])

@sio.on("deleteUser")
def deleteUser(userno):
	db.session.query(users).filter(users.userno==userno).delete()
	db.session.commit()
	return render_template("users.html", ip=config["ip"] ,config=config, theme=theme, url=links["people"], users= users.query.all())

@sio.on("startMeasure")
def startMeasure(userno,measureTime):
	global samplePerSecond
	print(measureTime)
	totalSample = int(measureTime)*samplePerSecond
	#TODO: check if folders exists
	initAvoSerial(com_port, 57600)
	sio.emit("startMeasure", [1, 0])
	now = datetime.now().strftime("%y%m%d-%H%M%S")
	user_rec_excel_folder = os.path.join(rec_folder,userno,"excel")
	user_rec_csv_folder = os.path.join(rec_folder,userno,"csv")
	user_rec_excel_file = os.path.join(user_rec_excel_folder,now + ".xlsx")
	user_rec_csv_file = os.path.join(user_rec_csv_folder,now+".csv")
	f = open(user_rec_csv_file, "a")
	newPath = shutil.copy('user_records.xlsx', user_rec_excel_file)
	workbook = load_workbook(filename=user_rec_excel_file)
	print (workbook.sheetnames)
	sheet = workbook["records"]
	f.write("time,number,nh3,co,no2,c3h8,c4h10,ch4,h2,c2h5oh\n")
	startMeasureBy(totalSample)
	data = readData()
	while (data != "STARTED"):
		startMeasureBy(totalSample)
		data = readData()
	for d in range(totalSample):
		data = readData()
		id_no = data.split(',')[1] 
		if is_integer(id_no): #is_integer fonksiyonu string içinde int varsa True dönüyor.
			if (int(id_no) == d):
				print(data)
				f.write(data+'\n')
				saveToExcel(sheet,data)
				sio.emit("startMeasure", [1, int(100*(d+1)/(totalSample))])
			else:
				print("DATA READ ERROR! TRY AGAIN")
	f.close()
	workbook.save(filename=user_rec_excel_file)
	sio.emit("startMeasure", [0, 100])
	#TODO: basari ile tamamlandi diye arayuze ekleyecegiz.	
	closeAvoSerial()
	sio.emit("alert", [1,1])
	sio.emit("startMeasure", [0, 0])

@sio.on("changeDuration")
def changeDuration(data):
	global measureTime
	measureTime = int(data)
	print(measureTime)

@sio.on("connect")
def connect():
	print("Connected")

@sio.on("disconnect")
def disconnect():
	print("Disconnected")

@sio.on("changeTheme")
def changeTheme():
	global theme
	if theme == "dark":
		theme = "light"
	elif theme == "light":
		theme = "dark"
	sio.emit("changeTheme", theme)

if __name__ == "__main__":
	app.debug = True
	print("                           dP                      dP oo          \n                           88                      88             \n.d8888b. dP   .dP .d8888b. 88  .dP  .d8888b. .d888b88 dP .d8888b. \n88'  `88 88   d8' 88'  `88 88888    88'  `88 88'  `88 88 88'  `88 \n88.  .88 88 .88'  88.  .88 88  `8b. 88.  .88 88.  .88 88 88.  .88 \n`88888P8 8888P'   `88888P' dP   `YP `88888P8 `88888P8 dP `88888P' \n")
	sio.run(app, host=config["host"], port=config["port"])
import subprocess
import sys

try:
    from flask import Flask, render_template, request, flash, url_for, redirect
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'flask'])
finally:
    from flask import Flask, render_template, request, flash, url_for, redirect

try:
    from flask_socketio import SocketIO
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'flask_socketio'])
finally:
    from flask_socketio import SocketIO

try:
    from flask_sqlalchemy import SQLAlchemy
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'flask_sqlalchemy'])
finally:
    from flask_sqlalchemy import SQLAlchemy

try:
    from flask_migrate import Migrate
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'Flask-Migrate'])
finally:
    from flask_migrate import Migrate

try:
    import serial
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'serial'])
finally:
    import serial

try:
    from glob import glob
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'glob'])
finally:
    from glob import glob

try:
    import threading
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'threading'])
finally:
    import threading

try:
    import locale
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'locale'])
finally:
    import locale

try:
    import io
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'io'])
finally:
    import io

try:
    from openpyxl import Workbook, load_workbook
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'openpyxl'])
finally:
    from openpyxl import Workbook, load_workbook

import shutil
import serial.tools.list_ports
import math
import random
from datetime import datetime
import os
from avoserial import *
import time
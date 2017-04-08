from flask import Flask, render_template, request
from werkzeug import secure_filename
from format_phonegap import format_data
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import codecs
import requests
import _thread

app = Flask("app")

	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f2 = request.files['file2']
		if f.filename == "allt.xml" and f2.filename == "lm-data.xml":
		    f.save(secure_filename(f.filename))
		    _thread.start_new_thread(format_data, ())
		    return 'Filen har laddats upp korrekt, om ca 10min kommer appen att vara uppdaterad'
		return 'Filen kunde inte laddas upp! Se till att filnamnen är "allt.xml"<br>och "lm-data.xml"'


@app.route("/")
def home():
	with open("index.html", "r") as f:
		page_content = f.read()
	return page_content
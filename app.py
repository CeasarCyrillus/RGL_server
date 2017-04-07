from flask import Flask, render_template, request
from werkzeug import secure_filename
from format_phonegap import format_data
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import codecs
import os
import requests

app = Flask("app")

	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route("/")
def home():
	with open("index.html", "r") as f:
		page_content = f.read()
	return page_content

#if __name__ == "__main__":
app.run(debug=True)
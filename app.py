from flask import Flask
from format_phonegap import format_data
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import codecs
import os
import requests

app = Flask("app")

@app.route("/")
def home():
    return "Hello World!"

#if __name__ == "__main__":
app.run("0.0.0.0")
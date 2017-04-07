from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import codecs
import os
import requests

with open("config.txt", "r") as f:
	data = f.readlines();
	config_lakemedelsform = data[0].replace("\n", "").replace("\r", "");
	config_allt_xml = data[1].replace("\n", "").replace("\r", "");

lx_lakemedelsform = {}

for event, elem in ET.iterparse(config_lakemedelsform):
	tag = elem.tag[34:]
	if tag == "enumeration":
		lx_lakemedelsform[elem.attrib["value"]] = elem.find("*")[0].text

f = codecs.open("lm-data.xml", "r", "utf-8")
text = list(set(f.read().split("</def:lmprodukt>")))
f.close()


f = codecs.open(config_allt_xml, "r", "utf-8")
allt = f.read()
f.close()

f = codecs.open("temp_data.txt", "w", "utf-8")
alla_preperat = []
for i in range(len(text)):
	print(i+1, "/", len(text), flush=True),
	soup = BeautifulSoup(str(text[i]), "html.parser")
	if soup is not None:
		name = soup.find("def:produktnamn")
		if name is not None:
			name = name.text.replace("®", "")
			form = soup.find("def:lakemedelsform")
			form = lx_lakemedelsform[form.text]
			eans = soup.find_all("def:streckkod")
			new_eans = []
			for ean in eans:
				ean_f = ean.text[1:]
				if len(ean_f) == 13:
					new_eans.append(ean_f)
			if name.lower() in allt.lower():
				if new_eans:
					f.write(name + ";" + form + "#" + str(new_eans)[1:-1].replace("'", "") + "#\n")
			else:
				if eans:
					for ean in eans:
						ean_f = ean.text[1:]
						if len(ean_f) == 13:
							prepp = name + ";" + form + ";-;-;-;-;-;"+ean_f+";-;\n"
							alla_preperat.append(prepp)

f.close()

f = codecs.open(config_allt_xml, "r", "utf-8")
text = f.read()
f.close()


soup = BeautifulSoup(text, "html.parser")
infodispens = soup.find_all("infodispens")
dispenser = {}
for info in infodispens:
	soup = BeautifulSoup(str(info), "html.parser")
	dispensid = soup.find("dispensid").text
	dispens = soup.find("dispens").text.replace("\n", "")
	dispenser[dispensid] = dispens

soup = BeautifulSoup(text, "html.parser")
infoforbud = soup.find_all("infoforbud")
forbuds = {}
for info in infoforbud:
	soup = BeautifulSoup(str(info), "html.parser")
	forbudid = soup.find("forbudid").text
	forbud = soup.find("forbud").text.replace("\n", "")
	forbuds[forbudid] = forbud

soup = BeautifulSoup(text, "html.parser")
infoovrigt = soup.find_all("infoovrigt")
ovrigts = {}
for info in infoovrigt:
	soup = BeautifulSoup(str(info), "html.parser")
	ovrigtid = soup.find("ovrigtid").text
	ovrigt = soup.find("ovrigt").text.replace("\n", "")
	ovrigts[ovrigtid] = ovrigt

soup = BeautifulSoup(text, "html.parser")
infoklass = soup.find_all("dopingklasser")
klasser = {}
for info in infoklass:
	soup = BeautifulSoup(str(info), "html.parser")
	klassid = soup.find("klassid").text
	klass = soup.find("dopingklass").text.replace("\n", "")
	klasser[klassid] = klass

ic_and_ooc = {"2":"Varierar", "1":"Ja", "3":"Nej"}

f = codecs.open("temp_data.txt", "r", "utf-8")
text = f.read().replace("\r", "")
f.close()
text = text.split("\n")[:-1]

data_from_temp_data = {}
for name in text:
	lista = name.split("#")[:-1]
	name = lista[0]
	ean = lista[1]
	data_from_temp_data[name] = ean


f = codecs.open(config_allt_xml, "r", "utf-8")
text = f.read()
f.close()

soup = BeautifulSoup(text, "html.parser")
lakemedel = {}
total = soup.find_all("lakemedel")
i = 1
ean_amount = 0
max_up = 0
for info in total:
	soup = BeautifulSoup(str(info), "html.parser")
	name = soup.find("produktnamn").text.replace("\n", "").replace("\r", "")
	form = soup.find("beredningsform").text.replace("\n", "").replace("\r", "")
	ic = soup.find("ic").text.replace("\n", "").replace("\r", "")
	ooc = soup.find("ooc").text.replace("\n", "").replace("\r", "")
	forbudid = soup.find("forbudid")
	dispensid = soup.find("dispensid")
	ovrigtid = soup.find("ovrigtid")
	klassid = soup.find("klassid")
	prep = name + ";" + form
	

	if forbudid is not None:
		forbud = forbuds[forbudid.text].replace("\n", "").replace("\r", "")
	else:
		forbud = "-"
	if dispensid is not None:
		dispens = dispenser[dispensid.text].replace("\n", "").replace("\r", "")
	else:
		dispens = "-"
	if ovrigtid is not None:
		ovrigt = ovrigts[ovrigtid.text].replace("\n", "").replace("\r", "")
	else:
		ovrigt = "-"
	if klassid is not None:
		klass = klasser[klassid.text].replace("\n", "").replace("\r", "")
	else:
		klass = "-"
	

	try:
		eans = data_from_temp_data[prep].replace(" ", "").replace("\n", "").replace("\r", "")
		eansEx = True
	except KeyError:
		ean = "-"
		eansEx = False
	if eansEx:
		for ean in eans.split(","):
			ean_amount += 1
			prep = name + ";" + form + ";" + ic_and_ooc[ic] + ";" + ic_and_ooc[ooc] + ";" + forbud + ";" + dispens + ";" + ovrigt + ";" + ean + ";" + klass + ";;";
			alla_preperat.append(prep)
	else:
		prep = name + ";" + form + ";" + ic_and_ooc[ic] + ";" + ic_and_ooc[ooc] + ";" + forbud + ";" + dispens + ";" + ovrigt + ";" + ean + ";" + klass + ";;";
		alla_preperat.append(prep)
	i += 1
	print(i, "/", len(total), flush=True),

alla_preperat = list(set(alla_preperat))
print("Antal preperat:", len(alla_preperat))
print("Hittade", ean_amount, "Streckkoder")
with open("databas.txt", "w") as f:
	for pr in alla_preperat:
		f.write(pr)
with open('databas_phonegap.txt', 'rb') as f:
	r = requests.post('http://fecabook.hol.es/static2/upload.php', files={'databas.txt': f})
print("Klar!")
input("")
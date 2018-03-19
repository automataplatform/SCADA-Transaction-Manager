#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import OpenOPC
from urllib.parse import urlparse, parse_qs

opc = OpenOPC.client()
opc.connect('Kepware.KEPServerEnterprise.V5')
PORT_NUMBER = 8080
tags=['Inlet_Nitrogen','Inlet_Methane','Inlet_CO2','Inlet_Ethane','Inlet_C5','Inlet_Propane','Inlet_IButane','Inlet_NButane','Inlet_Vapour_Pressure','Inlet_BTU','Inlet_Gas_SG','Inlet_Compressibility','Inlet_Gallons_MSCF','Inlet_Molecular_Weight','Residue_Nitrogen','Residue_Methane','Residue_CO2','Residue_Ethane','Residue_C5','Residue_Propane','Residue_IButane','Residue_NButane','Residue_Vapour_Pressure','Residue_BTU','Residue_Gas_SG','Residue_Compressibility','Residue_Gallons_MSCF','Residue_Molecular_Weight']
target_tags=[]
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		#GET query content
		query_components = parse_qs(urlparse(self.path).query)
		data = query_components["data"]
		if(data):
			self.wfile.write(json.dumps({"name":opc.read(data), "port":"7766", "data":"adad"}).encode())
		else:
			for tag in tags:
				target_tags.append(opc.read(tag))
			self.wfile.write(json.dumps({"name":target_tags, "port":"7766", "data":"adad"}).encode())
		# Send the html message
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
	

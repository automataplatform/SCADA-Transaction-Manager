#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import OpenOPC
from urllib.parse import urlparse, parse_qs

opc = OpenOPC.client()
opc.connect('Kepware.KEPServerEX.V6')
PORT_NUMBER = 8080
tags=["Inlet_BTU","Inlet_C5","Inlet_CO2","Inlet_Compressibility","Inlet_Ethane","Inlet_Gallons_MSCF","Inlet_Gas_SG","Inlet_IButane","Inlet_Methane","Inlet_Molecular_Weight","Inlet_NButane","Inlet_Nitrogen","Inlet_Propane","Inlet_Vapour_Pressure","Residue_BTU","Residue_C5","Residue_CO2","Residue_Compressibility","Residue_Ethane","Residue_Gallons_MSCF","Residue_Gas_SG","Residue_IButane","Residue_Methane","Residue_Molecular_Weight","Residue_NButane","Residue_Nitrogen","Residue_Propane","Residue_Vapour_Pressure","Tag1","Tag2",]
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
		
		#if(query_components["data"]):
		#	data = query_components["data"]
		#	self.wfile.write(json.dumps({"name":opc.read(data), "port":"7766", "data":"adad"}).encode())
		#else:
		for tag in tags:
			tempArr=[]
			tempArr.append(tag)
			tempArr.append(opc.read("Channel1.Device1."+tag))
			target_tags.append(tempArr)
		self.wfile.write(json.dumps({"data":target_tags}).encode())
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
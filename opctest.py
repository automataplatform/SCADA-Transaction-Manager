#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import OpenOPC
from urllib.parse import urlparse, parse_qs

opc = OpenOPC.client()
opc.connect('Matrikon.OPC.Simulation')
PORT_NUMBER = 8080
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
		# Send the html message
		self.wfile.write(json.dumps({"name":opc[data],"port":"7766","data":"adad"}).encode())
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
	

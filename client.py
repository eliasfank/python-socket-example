import socket
import sys
import os
import time

def usage():
	###Function that shows to the user how to call the program
	print("Usage:")
	print("python "+__file__+" <host> <port> <file path>")
	sys.exit()
	
def sendFile(host, port, fp):
	###Function that manages the sending of the file to the server
	m = s.recv(1024)
	if (m=="READY"):
		print("Sending file to "+host+":"+str(port))
		try:
			f = open(fp, 'rb')
			d = f.read(4096)
			s.send(d)
			while d != "":
				time.sleep(0.1)
				d = f.read(4096)
				s.send(d)
			#Signal the server that the file has reached the end
			s.send("--END--")
			f.close()
			l = s.recv(1024)
			#If the file has been uploaded successfully
			#Get the total value from the products of the uploaded file
			if (l=="SUCCES"): 
				print("Succesfully uploaded file.")
				totalValue = s.recv(1024)
				print("Total products value: "+totalValue)
				sys.exit()
			else:
				print("Failed to upload file. Try again?")
			s.close()
		except Exception as msg:
			print("Error message: "+str(msg))
			return False
		return True
	elif (m=="ERROR"):
		print("Error: An unexpected error has occoured at the server side. Try again?")
		return False
	else:
		print("Error: Didn't expect this message: "+m)
		return False

###Try to get all paramms from the command line
###If not, show to te user the usage information
try:
	host = sys.argv[1]
	port = int(sys.argv[2])
	filePath = sys.argv[3]
except:
	usage()
################################################

#Create a socket that use IPV4 and TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#If the file exists
#Start the connection with the server
if (os.path.exists(filePath)):
	try:
		s.connect((host, int(port)))
		print("Connected to server!")
	except socket.error as sem:
		print("ERROR: Couldn't connect.")
		print(sem)
		sys.exit()

	##Send a message that signals the start of the file upload
	s.send("GETFILE")
	sendFile(host, port, filePath)

else:
	print("File does not exists.")
	sys.exit()
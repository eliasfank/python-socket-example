import socket
import thread
import sys
import os
import uuid
HOST = ''              
PORT = 50005  # Port for the server recieve connections

def calcValue(fileName):
    ###Function that calculate the total value from products 
    ##in the recieved file
	totalValue = 0
	file = open(fileName, "r")
	lines = file.readlines()
	for l in lines:
		parts = l.split(",")
		totalValue+=float(parts[1])*float(parts[2])
	return totalValue

def get(con):
    ###generate a unique name to the file
    fileName = "RecievedFiles/"+str(uuid.uuid4()) 
    try:
        ###Save the file on the server directory
        #######################################################
        file = open(fileName, 'wb')
        con.send("READY")
        print("Downloading file...")
        while True:
            d = con.recv(4096)
            if (d=="--END--"):
                file.close()
                break
            #print(d)
            file.write(d)
        con.send("SUCCES")
        print("Succesfully downloaded file as "+fileName)
        #######################################################

        ###Calculate the total value from the products and send
        ##the value to the client##############################
        valorTotal = calcValue(fileName)
        con.send(str(valorTotal))
        #######################################################

        ###After it all, close the connection with the client
        con.close()

    except Exception as msg:
        con.send("ERROR")
        #File Error.
        print("Error message: "+str(msg))
        return

def conectado(con, cliente):
    ###Function that starts a new thread for the connection
    print 'Conectado por', cliente
    msg = con.recv(1024)
    if (msg=="GETFILE"):
        print("Connection started with "+str(cliente))
        get(con)
    else:
        con.close()
    thread.exit()

###Create a socket that use IPV4 and TCP protocol
###Bind the port for this process conections
###Set the maximun number of queued connections
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
try:
    tcp.bind(orig)
    print("Bind succesfull!")
except socket.error as SBE:
    print("Bind failed!")
    print(SBE)
    sys.exit()
tcp.listen(5)

print("TCP start.")
print("Listening...")

###Server accept connections until a keyboard interrupt
###If there is a keyboard interrupt, release the port
try:
    while True:
        con, cliente = tcp.accept()
        thread.start_new_thread(conectado, tuple([con, cliente]))
except KeyboardInterrupt:
    print("")
    print("Stop listening and TCP closed.")
    tcp.close()
    sys.exit()




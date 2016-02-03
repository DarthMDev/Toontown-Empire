# TODO: Add correct paths + add astron cluster files! ~FordTheWriter
import os
data = []
with open('C:\path\math\path\qa.prc', 'r+') as config:
	data = config.readlines()
	line = data[7].split()
	x = line[1]
	y = x.split("-")
	ver = y[2]
	ver = ver.split(".")
	if str(ver[2]) == "9":
		ver[1] = int(ver[1]) + 1
		ver[2] = 0
	if str(ver[1]) == "9":
		ver[0] = int(ver[0]) + 1
		ver[1] = 0
	else:
		ver[2] = int(ver[2]) + 1
		data[7] = "server-version TTE-Alpha-"+ str(ver[0]) + "." + str(ver[1]) + "." + str(ver[2]) + "\n"
		
		
os.remove('C:\path\math\path\qa.prc')

with open('C:\path\math\path\qa.prc', "a+") as newfile:
	newfile.writelines(data)
			
	print(ver)

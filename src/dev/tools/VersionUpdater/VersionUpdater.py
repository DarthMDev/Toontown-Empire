import os
data = []
#TODO: Add the correct path and make it edit the cluster files. ~FordTheWriter
with open('C:\Users\mar_h_000\Desktop\qa.prc', 'r+') as config:
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
		
		
os.remove('C:\Users\mar_h_000\Desktop\qa.prc')

with open('C:\Users\mar_h_000\Desktop\qa.prc', "a+") as newfile:
	newfile.writelines(data)
			
	print(ver)

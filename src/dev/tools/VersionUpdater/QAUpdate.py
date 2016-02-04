import os

MainPathRequest = raw_input("Enter Path Here For QA [Must not use frontslashes, Instead use the /.]: ")
QAPath = MainPathRequest + "qa.prc"


data = []
with open(QAPath, 'r+') as config:
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
 			
os.remove(QAPath)
 
with open(QAPath, "a+") as newfile:
 	newfile.writelines(data)
 	print(ver)
        
del data
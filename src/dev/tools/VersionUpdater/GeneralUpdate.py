import os

MainPathRequest = raw_input("Enter Path Here For General Config [Must not use frontslashes, Instead use the /.]: ")
VersionRequest = raw_input("Enter the version you want it to be: ")
Version = VersionRequest
GeneralPath = MainPathRequest + "general.prc"


data = []
with open(GeneralPath, 'r+') as config:
 	data = config.readlines()
 	line = data[6].split()  
        x = line[1]
 	data[6] = "build-version "+ Version + "\n"
 			
os.remove(GeneralPath)
 

with open(GeneralPath, "a+") as newfile:
 	newfile.writelines(data)
        print(Version)
        
del data
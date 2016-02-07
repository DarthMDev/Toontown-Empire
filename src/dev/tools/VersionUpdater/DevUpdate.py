import os

MainPathRequest = raw_input("Enter Path Here For Dev [Must not use frontslashes, Instead use the /.]: ")
DevPath = MainPathRequest + "dev.prc"
VersionRequest = raw_input("Enter the version you want it to be: ")
Version = VersionRequest

data = []
with open(DevPath, 'r+') as config:
 	data = config.readlines()
 	line = data[22].split()  
        x = line[1]
 	data[22] = "build-version "+ Version + "\n"
 			
os.remove(DevPath)
 

with open(DevPath, "a+") as newfile:
 	newfile.writelines(data)
        print(Version)
        
del data
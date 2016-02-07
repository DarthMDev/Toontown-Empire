import os

MainPathRequest = raw_input("Enter Path Here For QA [Must not use frontslashes, Instead use the /.]: ")
VersionRequest = raw_input("Enter the version you want it to be: ")
Version = VersionRequest
QAPath = MainPathRequest + "qa.prc"


data = []
with open(QAPath, 'r+') as config:
 	data = config.readlines()
 	line = data[8].split()  
        x = line[1]
 	data[8] = "build-version "+ Version + "\n"
 			
os.remove(QAPath)
 

with open(QAPath, "a+") as newfile:
 	newfile.writelines(data)
        print(Version)
        
del data
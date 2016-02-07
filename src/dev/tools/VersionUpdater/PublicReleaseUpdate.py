import os

MainPathRequest = raw_input("Enter Path Here For Public Client [Must not use frontslashes, Instead use the /.]: ")
PublicPath = MainPathRequest + "public_client.prc"
VersionRequest = raw_input("Enter the version you want it to be: ")
Version = VersionRequest


data = []
with open(PublicPath, 'r+') as config:
 	data = config.readlines()
 	line = data[32].split()  
        x = line[1]
 	data[32] = "build-version "+ Version + "\n"
 			
os.remove(PublicPath)
 

with open(PublicPath, "a+") as newfile:
 	newfile.writelines(data)
        print(Version)
        
del data
# import ftplib, os, shutil
# import random

# Folder_Name = "Test"
# try:
#     os.mkdir(Folder_Name)
# except FileExistsError:
#     pass
# Download_Path = Folder_Name + "/"
# ftp = ftplib.FTP()
# ftp.connect("175.209.222.13", 21)
# ftp.login("acon3d", "acon3d")

# Which_File = "/ModelMakerAsset/FBX/" + "Window"
# ftp.cwd(Which_File)
# # A = random.choice(ftp.nlst())
# print(random.choice(ftp.nlst())[: random.choice(ftp.nlst()).index(".fbx")])

door_index = None
if 1 + 2 == 4:
    door_index = 1

if door_index is not None:
    print("A")
else:
    print("B")

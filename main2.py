import os

def list_files(directory, n=0):
    list = sorted(os.listdir(directory), key=lambda x: -os.path.isdir(directory + str(x) + "/"))
    for i in list:
        if os.path.isfile(directory + str(i)):
            print("  "*n + ("└── " if i == list[-1] else "├── ") + str(i))
        elif os.path.isdir(directory + str(i) + "/"):
            print("  "*n + ("└── " if i == list[-1] else "├── ") + str(i))
            list_files(directory + str(i) + "/", n+1)
            
list_files("[your PATH]")

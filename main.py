import os

def list_files(directory, n=0):
    for i in os.listdir(directory):
        if os.path.isfile(directory + str(i)):
            print("  "*n + str(i))
        elif os.path.isdir(directory + str(i) + "/"):
            print("  "*n + str(i))
            list_files(directory + str(i) + "/", n+1)




def list_files2(directory, list=None):
    if not list:
        list = []
        
    res = []
    
    for i in os.listdir(directory):
        try:
            if os.path.isfile(directory + str(i)):
                res.append(str(i) + f" ({str(os.path.getsize(directory + str(i)) / 1024**2)} MB)")
            elif os.path.isdir(directory + str(i)):
                res.append([str(i), list_files2(directory + str(i) + "/", list)])
        except PermissionError:
            continue
    list += res
    return list


def print_files(arr, path, file, indents=1):

    if indents == 1:
        print(path)
        arr = sorted(arr, key=lambda x: (-isinstance(x, list), x))
    
        
    for item in arr:
        if isinstance(item, list):
            print_files(item, path, file, indents + 1 if len(item) > 0 and not isinstance(item[0], list) else indents)
        else:
            try:
                file.write("   |" * (indents) + "---" + item + "\n")
            except UnicodeEncodeError:
                continue
            print("   " * (indents) + ("└── " if item == arr[-1] else "├── ") + item)


            
def search(arr, filter=None, files=[]):
    for item in arr:
        if isinstance(item, list):
            search(item, filter, files)
        else:
            if filter:
                if str(filter) in str(item):
                    files.append(item)
            else:
                if " MB)" in str(item):
                    files.append(item)
    return sorted(files)

        
            



def main():
    exit = False
    print("Welcome to Filelister!\nAdd the file path of a directory from the MS-Explorer!")
    while not exit:
        file = open("file_lister/files.txt", "w")
        path = str(input("path: ")).replace('"', "").replace("\\", "/") + "/"
        print("P -> print whole filesystem | F -> filter for certain files")
        userinput = str(input("Input: "))
        if userinput.upper() == "P":
            print_files(list_files2(path), path, file)
        elif userinput.upper() == "F":
            file = open("file_lister/files.txt", "w")
            if str(input("Filter for certain file extension? Y -> Yes / N -> show all files sorted by filename\nInput: ")).upper() == "Y":
                for i in search(list_files2(path), str(input("file extension /example: .pdf, .exe, .xls, .docx, etc/ : "))):
                    print(i)
                    file.write(i + "\n")
            else:
                for i in search(list_files2(path)):
                    print(i)
                    file.write(i + "\n")
        if str(input("Exit? Y -> Yes / N -> No\nInput: ")).upper() == "Y":
            exit = True
        file.close()
main()


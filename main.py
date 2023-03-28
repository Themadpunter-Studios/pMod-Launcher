import webbrowser
import json
import sys
import os
import wget
import zipfile
import shutil

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
def downloadVersionInstance(version, name):
    global versionsjson, gamesjson
    try:
        file = wget.download(versionsjson[version])
    except:
        return "ERROR || Version nonexistent"
    try:
        print("\n")
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(name)
        os.remove(file)
        gamesjson["games"][name] = {
            "gamedir": os.getcwd()+"/"+name+"/pMod-"+version
        }
        with open("games.json", "w") as write_file:
            json.dump(gamesjson, write_file)
        
        
    except:
        return "ERROR || Error in unzipping"
    return "INFO || SUCCESS"

try:
    os.remove("versions.json")
except:
    pass
wget.download("https://raw.githubusercontent.com/Themadpunter-Studios/pMod-data/main/versions.json")
with open("versions.json", "r") as read_file:
    versionsjson = json.load(read_file)

try:
    with open("games.json", "r") as read_file:
        gamesjson = json.load(read_file)
except:
    defaultData = {
    "games": {
        
    },
    "default": "v1.1.0"
}
    
    with open("games.json", "w") as write_file:
        json.dump(defaultData, write_file)
    with open("games.json", "r") as read_file:
        gamesjson = defaultData
    downloadVersionInstance("v1.1.0","v1.1.0")



instance = gamesjson["default"]   



def main():
    global instance, gamesjson, versionsjson
    clear()
    print("MAIN MENU")
    print("1) Play pMod")
    print("2) Switch Instance")
    print("3) Create Instance")
    print("4) Modify Instance")
    try:
        choice = int(input("pMod> "))
    except:
        choice = 0
    if choice == 1:
        webbrowser.open(gamesjson["games"][instance]["gamedir"]+"/build/index.html")
    elif choice == 2:
        clear()
        print("Enter instance name:")
        for instancename in gamesjson["games"].keys():
            print(instancename)
        instance = input("pMod> ")
        while not instance in gamesjson["games"].keys():
            print("Instance not in list. Try again.")
            instance = input("pMod> ")
        main()
    elif choice == 3:
        clear()
        print("Enter instance name: (Type nothing to cancel:)")
        instanceName = input("pMod> ")
        if instanceName == "":
            main()
        print("Enter instance version:")
        print("(VERSION LIST:)")
        for instancename in versionsjson.keys():
            print(instancename) 
        versionName = input("pMod> ")
        while not versionName in versionsjson.keys():
            print("Version not in list. Try again.")
            versionName = input("pMod> ")
        downloadVersionInstance(versionName, instanceName)
        print("\n\n")
        main()
    elif choice == 4:
        clear()
        print("How to mod instance?")
        print("1) Rename Instance")
        print("2) Delete Instance")
        print("3) Set as Default")
        print("4) Modding Info")
        try:
            choice = int(input("pMod> "))
        except:
            choice = 0
        if choice == 1:
            print("What to rename to?")
            mvto = input("pMod> ")
            os.rename(instance, mvto)
            gamesjson["games"][mvto] = gamesjson["games"][instance]
            gamesjson["games"][mvto]["gamedir"] = os.getcwd()+"/"+mvto
            if gamesjson["default"] == instance:
                gamesjson["default"] = mvto
            del gamesjson["games"][instance]
            instance = mvto
            with open("games.json", "w") as write_file:
                json.dump(gamesjson, write_file)
            main()
        elif choice == 2:
            if len(gamesjson["games"].keys()) < 2:
                print("Can't remove only instance")
                main()
            shutil.rmtree(instance)
            del gamesjson["games"][instance]
            if instance == gamesjson["default"]:
                instance = list(gamesjson["games"].keys())[0]
                gamesjson["default"] = list(gamesjson["games"].keys())[0]
            with open("games.json", "w") as write_file:
                json.dump(gamesjson, write_file)
            main()
        elif choice == 3:
            gamesjson["default"] = instance
            with open("games.json", "w") as write_file:
                json.dump(gamesjson, write_file)
            main()
        elif choice == 4:
            print("""
How to Mod
1. Open the .sb3 file in https://shredmod.is-an.app
2. Apply your changes.
3. Go to https://shredmod.github.io/packager/.
4. Compile your new .sb3 file.
5. Replace the builds in the build directory.
            """)
            while True:
                pass
        main()
        
print("\nWelcome to pMod Launcher!")
main()
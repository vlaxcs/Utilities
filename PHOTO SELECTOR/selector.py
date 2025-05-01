import shutil
import os

config = {
    "id_path": None,
    "photo_format": None,
    "source_path": None,
    "destination_path": None,
    "classify": None,
    "classifier": {
        "classifier_path": None
    }
}

def setConfig():
    global config
    with open(os.path.join(os.path.dirname(__file__), "config.dpr")) as f:
        attr = []
        for line in f.readlines():
            if line.startswith(">"):
                attr.append(line.split(">")[1].strip())

    try:
        config["id_path"] = os.path.join(os.path.dirname(__file__), "id.in")
        config["photo_format"] = attr[0].upper()
        config["source_path"] = os.path.normpath(attr[1])
        config["destination_path"] = os.path.normpath(attr[2])
        config["classify"] = False if attr[3].lower() != "da" else True
        if config["classify"]:
            config["classifier"]["classifier_path"] = os.path.join(os.path.dirname(__file__), "classify.in")
        
    except:
        print("Invalid configuration file.")
        exit(0)

photo_groups = dict()

def setDict(filename):
    global photo_group
    with open(filename, "r") as f:
        photo_group = {line.split('-')[0].strip(): line.split('-')[1].strip() for line in f.readlines()} 
    
    return photo_group


def copy_files(id_path, photo_format, src, dest, classify = False):
    if not os.path.exists(src):
        print(f"Source path '{src}' does not exist.")
        return
    
    if not os.path.exists(dest):
        print(f"Destination path '{dest}' does not exist.")
        os.makedirs(dest)
        print(f"Creted '{dest}'.")


    if not os.path.exists(id_path):
        print(f"Cannot fetch from {id_path}. Invalid route.")
        return

    files = []
    with open(id_path) as f:
        files = [{
            "name": f"IMG_{'0' * (4 - len(id.split('-')[0].strip()))}{id.split('-')[0].strip()}.{photo_format}",
            "classified": True if classify and id.count('-') == 1 else False,
            "class": id.split('-')[1].strip() if classify and id.count('-') == 1 else None
        } for id in f.readlines()]

    if classify:
        global photo_groups
        for group in photo_groups:
            try:
                tempdest = os.path.join(dest, photo_groups[group])
                os.makedirs(tempdest, exist_ok=True)
                print(f"Created {tempdest}.")
            except:
                print(f"Cannot create file {tempdest}. It might already exists.")
            
    for file in files:
        tempdest = os.path.join(dest, photo_groups[file["class"]]) if classify and file["class"] is not None else dest
        full_file_name = os.path.join(src, file["name"])
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, tempdest)
            print(f"Copied: {file["name"]} -> {tempdest}")
        else:
            print(f"File not found: {full_file_name}")

# photo_format to upper

if __name__ == "__main__":
    setConfig()

    id_path = config["id_path"]
    photo_format = config["photo_format"]
    src = config["source_path"]
    dest = config["destination_path"]
    classify = config["classify"]
    if (classify):
        classifier_path = config["classifier"]["classifier_path"]
        photo_groups = setDict(classifier_path)

    copy_files(id_path, photo_format, src, dest, classify)
    exit(0)
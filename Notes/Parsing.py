
import os
import json
import xml.etree.ElementTree as ET

from copy import deepcopy
from Logger import logger

class Parsing:
    def __init__(self):
        self.loaded = None
        self.file_path = None
        self.loading_static_paths()


    def loading_static_paths(self):
        file_dir_name = os.path.dirname(__file__)
        self.static_folder = os.path.abspath(
            os.path.join(
                file_dir_name, "static"
            )
        )
    @classmethod
    def file_exists(cls, file_path):
        if os.path.exists(file_path):
            return True
        else:
            raise FileNotFoundError(
                f"File {file_path} not found"
            )

    def json_parsing(self, file_name):
        self.file_path = f"{self.static_folder}/{file_name}"

        def load_and_print_json_file_content(
            file_path: str = None
        ):
            with open(file_path or self.file_path, "r") as json_file_r:
                self.loaded = json.load(json_file_r) # dict/list
                logger.debug(self.loaded)

        def save_json_data():
            changed_data = deepcopy(self.loaded)
            changed_data["properties"].append(
                {"name": "sadness", "level": 15}
            )
            replaced_path = self.file_path.replace(".json", "changed.json")
            with open(replaced_path, "w") as json_file_w:
                json.dump(changed_data, json_file_w, indent=4)
            load_and_print_json_file_content(replaced_path)
            os.remove(replaced_path)

        if self.file_exists(self.file_path):
            load_and_print_json_file_content()
            save_json_data()


if __name__ == '__main__':
    parsing = Parsing()
    parsing.json_parsing("simple.json")
    print("*" * 60)

# parse parsuje po nazwie pliku


# przykład: przejrzyj elementy <item> i wypisz atrybuty/tekst
def xml_parsing():
    tree = ET.parse("data.xml")
    root = tree.getroot()
    for item in root.findall(".//item"):
        print("attr id:", item.get("id"))
        print("text:", (item.text or "").strip())


    from urllib.request import urlopen
    # Pobieranie z URL (standardowe)
    with urlopen("https://example.com/data.xml") as r:
        xml_bytes = r.read()
    root = ET.fromstring(xml_bytes)


    # streaming, przy dużych plikach
    for event, elem in ET.iterparse("big.xml", events=("end",)):
        if elem.tag == "record":
            # przetwórz record
            print(elem.findtext("title"))
            # usuń, żeby zwolnić pamięć
            elem.clear()


    # jak masz już tekst to po prostu ładujesz
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <server>
            <host>localhost</host>
            <port>8080</port>
        </server>
        <users>
            <user name="admin">active</user>
            <user name="guest">inactive</user>
        </users>
    </config>
    """

    """
        Mapuje sie na cos takiego
    config
     ├── server
     │    ├── host  → "localhost"
     │    └── port  → "8080"
     └── users
          ├── user (name="admin") → "active"
          └── user (name="guest") → "inactive"
    
    Po sparsowaniu dostaje roota - czyli obiekt klasy Element
        Kążdy element ma
        .tag - nazwa elementu
        .text - tekst miedzy znacznikami
        .attrib - słownik atrybutów
        .find / .findall () - wyszukiwanie pojedyncze, albo wszystkcih dzieci
        
    Wyszukiwanie elementów  - ściężki XPath
        "server" 
            - dziecko o nazwie server 
            - element -> <server>.. </server>.
        "./server/port" 
            - element port wewnętrz dziecka
            <server><port>...</por></server>
        ".//user"
            -dowolny user w całym drzewie - wszystkie <user>
        
        ".//user[@name='admin']"
            -tylko user który ma dany atrybut name 
            
    Dodawanie / modyfikacja
    """
    root = ET.fromstring(xml_data)
    print(root.find(".//Interval").text)

    new_user = ET.Element("user", name="new")
    new_user.text = "pending"
    root.find("users").append(new_user)

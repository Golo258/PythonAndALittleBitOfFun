import os
import json
import yaml  # pyyaml

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
        json_file_path = f"{self.static_folder}/{file_name}"

        def load_and_print_json_file_content(
                file_path: str = None
        ):
            with open(file_path or json_file_path, "r") as json_file_r:
                self.loaded = json.load(json_file_r)  # dict/list
                logger.debug(self.loaded)

        def load_from_string():
            string_var = '{"a": 1, "b":3}'
            json_data = json.loads(string_var)
            logger.debug(json_data)

        def from_dict_to_string(cls):
            text = json.dumps(cls.loaded, indent=2)
            assert isinstance(text, str)
            logger.debug(text)

        def save_json_data():
            changed_data = deepcopy(self.loaded)
            changed_data["properties"].append(
                {"name": "sadness", "level": 15}
            )
            replaced_path = json_file_path.replace(".json", "changed.json")
            with open(replaced_path, "w") as json_file_w:
                json.dump(changed_data, json_file_w, indent=4)
            load_and_print_json_file_content(replaced_path)
            os.remove(replaced_path)

        if self.file_exists(json_file_path):
            load_and_print_json_file_content()
            save_json_data()
            load_from_string()
            from_dict_to_string(self)

    def yaml_parsing(self, file_name):
        yaml_file_path = f"{self.static_folder}/{file_name}"
        if self.file_exists(yaml_file_path):
            def load_yaml_and_show_content(file_path: str = None):
                chosen_path = file_path or yaml_file_path
                with open(chosen_path, "r") as yaml_file_r:
                    yaml_data = yaml.safe_load(yaml_file_r)  # ->dict/ list
                logger.debug(f"\n-- File {chosen_path}\n-- Data: {yaml_data}")
                return yaml_data

            def save_changed_data(data):
                data["pokemon"]["personality"] = "friendly"
                changed = yaml_file_path.replace(".yaml", "_changed.yaml")
                with open(changed, "w") as yaml_file_w:
                    yaml.safe_dump(yaml_data, yaml_file_w, sort_keys=False)

                load_yaml_and_show_content(changed)
                os.remove(changed)

            yaml_data = load_yaml_and_show_content()
            save_changed_data(yaml_data)

            logger.debug(yaml_data)

    def ini_parsing(self, file_name):
        from configparser import ConfigParser
        ini_file_path = f"{self.static_folder}/{file_name}"
        config = ConfigParser()
        if self.file_exists(ini_file_path):
            with open(ini_file_path, "r") as ini_r:
                config.read_file(ini_r)
            ini_data = {
                section: dict(config[section])
                for section in config.sections()
            }
            logger.debug(ini_data)
            ini_data["Database"]["allowed_proxy"] = True
            with open(ini_file_path, "w") as ini_w:
                config.write(ini_w)

    def xml_parsing(self, file_name):
        import xml.etree.ElementTree as ET
        xml_file_path = f"{self.static_folder}/{file_name}"
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        for item in root.findall(".//book"):
            logger.info(f"author: {item.find("author").text}")
            logger.info(f"title: {item.find("title").text}")

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
        root = ET.fromstring(xml_data)
        logger.info(root.find(".//host").text)

        new_user = ET.Element("user", name="new")
        new_user.text = "pending"
        root.find("users").append(new_user)

        # saving change or new
        new_root = ET.Element("root")
        ET.SubElement(new_root, "item", attrib={"id": "1"}).text = "Hello"
        tree = ET.ElementTree(new_root)
        tree.write(f"{self.static_folder}/out.xml", encoding="utf-8", xml_declaration=True)

    def csv_parsing(self):
        import csv

        # Wczytanie
        with open(f"{self.static_folder}/simple.csv", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for key in row.keys():
                    print(row[key])

        # Zapis
        with open(f"{self.static_folder}/out.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["col1", "col2"])
            writer.writeheader()
            writer.writerow({"col1": 1, "col2": 2})

if __name__ == '__main__':
    parsing = Parsing()
    parsing.json_parsing("simple.json")
    print("*" * 60)
    parsing.yaml_parsing("simple.yaml")
    print("*" * 60)
    parsing.ini_parsing("simple.ini")
    print("*" * 60)
    parsing.xml_parsing("simple.xml")
    print("*" * 60)
    parsing.csv_parsing()


    # przykład: przejrzyj elementy <item> i wypisz atrybuty/tekst


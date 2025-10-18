
import xml.etree.ElementTree as ET


# parse parsuje po nazwie pliku

tree = ET.parse("data.xml")
root = tree.getroot()

# przykład: przejrzyj elementy <item> i wypisz atrybuty/tekst
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

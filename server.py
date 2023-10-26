import csv
import xml.etree.ElementTree as ET
import sqlite3
import uuid
from xmlrpc.server import SimpleXMLRPCServer

server = SimpleXMLRPCServer(('localhost', 8000))
server.register_introspection_functions()

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def write_to_xml(data, filename):
    root = ET.Element("persons")
    for item in data:
        person = ET.SubElement(root, "person")
        ET.SubElement(person, "id").text = item["id"]
        ET.SubElement(person, "first_name").text = item["first_name"]
        ET.SubElement(person, "last_name").text = item["last_name"]
        ET.SubElement(person, "gender").text = item["gender"]
        ET.SubElement(person, "ip_address").text = item["ip_address"]
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space = "\t", level=0)
    tree.write(filename)

def write_to_sqlite(data, database_file):
    conn = sqlite3.connect(database_file)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        ip_address TEXT
    )
    ''')

    for item in data:
        cur.execute("INSERT INTO persons (id, first_name, last_name, gender, ip_address) VALUES (?, ?, ?, ?, ?)", 
                    (item["id"], item["first_name"], item["last_name"], item["gender"], item["ip_address"]))

    conn.commit()
    cur.close()
    conn.close()

# Funções remotas que o cliente pode chamar
def get_all_persons():
    persons = []
    for person in root.findall('person'):
        person_data = {
            "id": person.find('id').text,
            "first_name": person.find('first_name').text,
            "last_name": person.find('last_name').text,
            "gender": person.find('gender').text,
            "ip_address": person.find('ip_address').text,
        }
        formatted_data = format_person_data(person_data)
        persons.append(formatted_data)
    return persons

def search_person_by_first_name(first_name):
    first_name = first_name.upper()
    persons = []
    for person in root.findall('person'):
        if person.find('first_name').text.upper() == first_name:
            person_data = {
                "id": person.find('id').text,
                "first_name": person.find('first_name').text,
                "last_name": person.find('last_name').text,
                "gender": person.find('gender').text,
                "ip_address": person.find('ip_address').text,
            }
            formatted_data = format_person_data(person_data)
            persons.append(formatted_data)
    return persons

def search_person_by_last_name(last_name):
    last_name = last_name.upper()
    persons = []
    for person in root.findall('person'):
        if person.find('last_name').text.upper() == last_name:
            person_data = {
                "id": person.find('id').text,
                "first_name": person.find('first_name').text,
                "last_name": person.find('last_name').text,
                "gender": person.find('gender').text,
                "ip_address": person.find('ip_address').text,
            }
            formatted_data = format_person_data(person_data)
            persons.append(formatted_data)
    return persons

def count_and_sort_persons_by_first_name():
    name_count = {}
    for person in root.findall('person'):
        first_name = person.find('first_name').text
        if first_name in name_count:
            name_count[first_name] += 1
        else:
            name_count[first_name] = 1

    sorted_results = sorted(name_count.items(), key=lambda x: x[1], reverse=True)

    result = [f"{name} - {count} person{'s' if count > 1 else ''}" for name, count in sorted_results]
    return result
def format_person_data(person):
    formatted_data = (
        f"Id: {person['id']},\n"
        f"First Name: {person['first_name']},\n"
        f"Last Name: {person['last_name']},\n"
        f"Gender: {person['gender']},\n"
        f"Ip Address: {person['ip_address']}\n"
        "-----------------------------------------------------"
    )
    return formatted_data

def add_person( first_name, last_name, gender, ip_address):
    try:
        while True:
            new_id = str(uuid.uuid4())
            
            if any(person.find('id').text == new_id for person in root.findall('person')):
                continue
    
            new_person = {
                "id": new_id,
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "ip_address": ip_address
            }

            new_person_element = ET.SubElement(root, "person")
            for key, value in new_person.items():
                ET.SubElement(new_person_element, key).text = value
            tree.write("output.xml")

            conn = sqlite3.connect(DATABASE_FILE)
            cur = conn.cursor()
            cur.execute("INSERT INTO persons (id, first_name, last_name, gender, ip_address) VALUES (?, ?, ?, ?, ?)",
                        (new_id, first_name, last_name, gender, ip_address))
            conn.commit()
            cur.close()
            conn.close()

            return "Data added successfully"
    except Exception as e:
        return str(e)
        
server.register_function(get_all_persons)
server.register_function(search_person_by_first_name)
server.register_function(search_person_by_last_name)
server.register_function(count_and_sort_persons_by_first_name)
server.register_function(add_person)

if __name__ == "__main__":
    try:
        data = read_csv("dataset.csv")
        write_to_xml(data, "output.xml")
        tree = ET.parse('output.xml')
        root = tree.getroot()
        DATABASE_FILE = "database.db"
        write_to_sqlite(data, DATABASE_FILE)
        print("Servidor RPC iniciado. Aguardando conexões...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor RPC encerrado.")

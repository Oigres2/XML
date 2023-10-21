import csv
import xml.etree.ElementTree as ET
import sqlite3

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

if __name__ == "__main__":
    data = read_csv("dataset.csv")
    write_to_xml(data, "output.xml")
    DATABASE_FILE = "database.db"
    write_to_sqlite(data, DATABASE_FILE)

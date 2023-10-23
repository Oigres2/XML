import xmlrpc.client
import os

server = xmlrpc.client.ServerProxy('http://localhost:8000')

def menu():

    while True:
        os.system('cls')
        print("\n--- Menu ---")
        print("1. Show all persons")
        print("2. Search by first name")
        print("3. Search by last name")
        print("4. Count Persons by name")
        print("5. Add new person")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            os.system('cls')
            persons = server.get_all_persons()
            for person in persons:
                print(person)
            input("Press 'Enter' to continue to menu")
        elif choice == "2":
            os.system('cls')
            first_name = input("Enter the first name to search: ").strip()
            persons = server.search_person_by_first_name(first_name)
            for person in persons:
                print(person)
            input("Press 'Enter' to continue to menu")
        elif choice == "3":
            os.system('cls')
            last_name = input("Enter the last name to search: ").strip()
            persons = server.search_person_by_last_name(last_name)
            for person in persons:
                print(person)
            input("Press 'Enter' to continue to menu")
        elif choice == "4":
            os.system('cls')
            persons = server.count_and_sort_persons_by_first_name()
            for person in persons:
                print(person)
            input("Press 'Enter' to continue to menu")
        elif choice == "5":
            os.system('cls')
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            gender = input("Enter Gender: ").strip()
            ip_address = input("Enter IP Address: ").strip()

            server.add_person(first_name, last_name, gender, ip_address)
            print("Data added successfully.")
            input("Press 'Enter' to continue to menu")
        elif choice == "6":
            os.system('cls')
            print("Exiting...")
            break
        else:
            print("Invalid option! Try again.")


if __name__ == "__main__":
    menu()

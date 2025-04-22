import csv
import datetime
import os

# Constants
current_time = str(datetime.datetime.today()).split()
save_time = str('-'.join(list(reversed(current_time[0].split('-')))) + ' @ ' + ':'.join(current_time[1].split(':')[:2]))
fieldnames = ['Timestamp', 'Task']
fieldnames2 = ['Timestamp', 'Task', 'DeletedOn']
data_file = 'data.csv'
history_file = 'history.csv'

class ToDoList:

    def __init__(self):
        self.items = []
        self.deleted_items = []

        if os.path.exists(data_file):
            with open(data_file, newline='') as f1:
                items = csv.DictReader(f1)
                self.items = list(items)

        if os.path.exists(history_file):
            with open(history_file, newline='') as f2:
                deleted_items = csv.DictReader(f2)
                self.deleted_items = list(deleted_items)

        print('''\n=== Welcome to To-Do List App ===''')

    def display_items(self):
        print("\n--- Your To-Do List ---\n")
        if not self.items:
            print("No items in your to-do list.")
            return
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item['Timestamp']} | {item['Task']}")

    def add_item(self):
        item = input("\nAdd Task: ")
        adding = {'Timestamp': save_time, 'Task': item}
        self.items.append(adding)
        print("The item has been added.")

    def remove_item(self):
        self.display_items()
        print("\nWhat do you want to remove from the items above?")
        try:
            deletion = int(input("Enter item number to remove: "))
            if deletion <= 0 or deletion > len(self.items):
                raise ValueError

            deleted_item = self.items.pop(deletion - 1)
            deleted_item.update({'DeletedOn': save_time})
            self.deleted_items.append(deleted_item)
            print("The item has been deleted.")
        except ValueError:
            print("Please enter a valid number.")

    def history(self):
        print("\n--- Your Deleted To-Do List ---\n")
        if not self.deleted_items:
            print("No deleted items.")
            return
        for i, item in enumerate(self.deleted_items, 1):
            print(f"{i}. Deleted On: {item['DeletedOn']} -> {item['Timestamp']} | {item['Task']}")

    def save_file(self):
        with open(data_file, 'w', encoding='UTF8', newline='') as f1:
            writer = csv.DictWriter(f1, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.items)

        with open(history_file, 'w', encoding='UTF8', newline='') as f2:
            writer = csv.DictWriter(f2, fieldnames=fieldnames2)
            writer.writeheader()
            writer.writerows(self.deleted_items)

        print("\nThank You! Your To-Do List has been saved.")

    @staticmethod
    def help_menu():
        print('''
--- MENU OPTIONS ---
Press '1' to See Items
Press '2' to Add Item
Press '3' to Remove Item
Press '4' to See Deleted Items
Press '5' or 'quit' to Quit the App (and save your data)
''')


# === Main Entry ===
if __name__ == "__main__":
    myApp = ToDoList()
    myApp.help_menu()

    while True:
        print("\nType 'help' to see the menu OR 'quit' to save your list and close the app,")
        user_input = input("-> What do you want to do?: ").strip().lower()

        if user_input == "help":
            myApp.help_menu()
        elif user_input == "1":
            myApp.display_items()
        elif user_input == "2":
            myApp.add_item()
        elif user_input == "3":
            myApp.remove_item()
        elif user_input == "4":
            myApp.history()
        elif user_input == "5" or user_input == "quit":
            myApp.save_file()
            break
        else:
            print("\nInvalid input. Try again.")

import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import csv
from plyer import notification
import os

# Helper function to get the current timestamp
def current_time():
    return str(datetime.datetime.now())

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("500x500")
        self.root.config(bg="#222222")

        # List to store tasks
        self.tasks = []

        # UI elements
        self.create_widgets()

        # Load tasks from CSV if it exists
        self.load_tasks()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="To-Do List App", font=("Arial", 24), fg="#FFD700", bg="#222222")
        self.title_label.pack(pady=20)

        self.search_box = tk.Entry(self.root, font=("Arial", 12), fg="#FFD700", bg="#222222")
        self.search_box.pack(pady=10)
        self.search_box.bind("<KeyRelease>", self.search_tasks)

        self.listbox = tk.Listbox(self.root, font=("Arial", 12), fg="#FFD700", bg="#111111", selectbackground="#FFD700", height=15, width=50)
        self.listbox.pack(pady=10)

        self.button_frame = tk.Frame(self.root, bg="#222222")
        self.button_frame.pack()

        self.add_task_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, bg="#444444", fg="#FFD700", font=("Arial", 12))
        self.add_task_button.grid(row=0, column=0, padx=10)

        self.toggle_theme_button = tk.Button(self.button_frame, text="Toggle Dark/Light Mode", command=self.toggle_theme, bg="#444444", fg="#FFD700", font=("Arial", 12))
        self.toggle_theme_button.grid(row=0, column=1, padx=10)

        self.export_button = tk.Button(self.button_frame, text="Export Tasks", command=self.export_tasks, bg="#444444", fg="#FFD700", font=("Arial", 12))
        self.export_button.grid(row=0, column=2, padx=10)

        self.import_button = tk.Button(self.button_frame, text="Import Tasks", command=self.import_tasks, bg="#444444", fg="#FFD700", font=("Arial", 12))
        self.import_button.grid(row=0, column=3, padx=10)

    def add_task(self):
        task = simpledialog.askstring("Add New Task", "Enter a task:", parent=self.root)
        if task:
            category = simpledialog.askstring("Category", "Enter Category (e.g., Work, Study):", parent=self.root)
            priority = simpledialog.askstring("Priority", "Set Priority (Low, Medium, High):", parent=self.root)
            due_date = simpledialog.askstring("Due Date", "Enter Due Date (DD-MM-YYYY):", parent=self.root)

            try:
                due_date_obj = datetime.datetime.strptime(due_date, "%d-%m-%Y")
            except ValueError:
                messagebox.showwarning("Invalid Date", "Please enter a valid date in DD-MM-YYYY format.")
                return

            if priority not in ["Low", "Medium", "High"]:
                messagebox.showwarning("Invalid Priority", "Priority must be Low, Medium, or High.")
                return

            self.tasks.append({
                'Timestamp': current_time(),
                'Task': task,
                'Category': category,
                'Priority': priority,
                'Due Date': due_date_obj
            })
            self.display_tasks()
            self.send_notification(task)

    def display_tasks(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            due = task.get('Due Date')
            if due and datetime.datetime.now() > due:
                self.listbox.insert(tk.END, f"• {task['Task']} | Category: {task['Category']} | Priority: {task['Priority']} | Due: {due.strftime('%d-%m-%Y')} (Overdue)")
            else:
                self.listbox.insert(tk.END, f"• {task['Task']} | Category: {task['Category']} | Priority: {task['Priority']} | Due: {due.strftime('%d-%m-%Y')}")

    def search_tasks(self, event):
        search_term = self.search_box.get().lower()
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            if search_term in task['Task'].lower():
                self.listbox.insert(tk.END, f"• {task['Task']} | Category: {task['Category']} | Priority: {task['Priority']} | Due: {task['Due Date'].strftime('%d-%m-%Y')}")

    def toggle_theme(self):
        if self.root.cget('bg') == "#222222":  # Dark Mode
            self.root.config(bg="#FFFFFF")
            self.listbox.config(bg="#FFFFFF", fg="#000000", selectbackground="#FFD700")
            self.button_frame.config(bg="#FFFFFF")
        else:  # Light Mode
            self.root.config(bg="#222222")
            self.listbox.config(bg="#111111", fg="#FFD700", selectbackground="#FFD700")
            self.button_frame.config(bg="#222222")

    def export_tasks(self):
        with open('tasks_export.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Timestamp", "Task", "Category", "Priority", "Due Date"])
            writer.writeheader()
            writer.writerows(self.tasks)
        messagebox.showinfo("Export", "Tasks exported successfully!")

    def import_tasks(self):
        if not os.path.exists('tasks_import.csv'):
            messagebox.showwarning("Import Error", "No tasks to import. Please make sure the file exists.")
            return
        with open('tasks_import.csv', newline='') as file:
            reader = csv.DictReader(file)
            self.tasks = list(reader)
        self.display_tasks()

    def send_notification(self, task):
        notification.notify(
            title="Task Reminder",
            message=task,
            timeout=10
        )

    def load_tasks(self):
        if os.path.exists('tasks_import.csv'):
            with open('tasks_import.csv', newline='') as file:
                reader = csv.DictReader(file)
                self.tasks = list(reader)
            self.display_tasks()


# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

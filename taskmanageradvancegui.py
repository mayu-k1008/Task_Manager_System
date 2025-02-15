import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime

tasks = []

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            global tasks
            tasks = json.load(file)
    except FileNotFoundError:
        pass

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def add_task():
    task = simpledialog.askstring("Input", "Enter task:")
    due_date = simpledialog.askstring("Input", "Enter due date (YYYY-MM-DD):")
    priority = simpledialog.askstring("Input", "Enter priority (High/Medium/Low):")
    category = simpledialog.askstring("Input", "Enter category:")
    if task:
        task_details = {"task": task, "completed": False, "due_date": due_date, "priority": priority, "category": category}
        tasks.append(task_details)
        save_tasks()
        refresh_tasks()

def delete_task():
    task_index = task_listbox.curselection()
    if task_index:
        tasks.pop(task_index[0])
        save_tasks()
        refresh_tasks()

def mark_task_completed():
    task_index = task_listbox.curselection()
    if task_index:
        tasks[task_index[0]]["completed"] = True
        save_tasks()
        refresh_tasks()

def refresh_tasks():
    for row in task_listbox.get_children():
        task_listbox.delete(row)
    for i, task in enumerate(tasks):
        status = "Completed" if task["completed"] else "Pending"
        due_date = task["due_date"] if task["due_date"] else "No due date"
        priority = task["priority"] if task["priority"] else "No priority"
        category = task["category"] if task["category"] else "No category"
        task_listbox.insert("", "end", iid=i, values=(task["task"], status, due_date, priority, category))

def search_tasks():
    keyword = simpledialog.askstring("Search", "Enter keyword to search:")
    if keyword:
        result_listbox.delete(*result_listbox.get_children())
        results = [task for task in tasks if keyword.lower() in task["task"].lower()]
        if results:
            for i, task in enumerate(results):
                status = "Completed" if task["completed"] else "Pending"
                due_date = task["due_date"] if task["due_date"] else "No due date"
                priority = task["priority"] if task["priority"] else "No priority"
                category = task["category"] if task["category"] else "No category"
                result_listbox.insert("", "end", iid=i, values=(task["task"], status, due_date, priority, category))
        else:
            messagebox.showinfo("Search Results", "No matching tasks found")

def show_help():
    help_message = """
    Available commands:
    - Add Task: Add a new task with optional due date, priority, and category
    - Delete Task: Delete a selected task
    - Mark Task Completed: Mark a selected task as completed
    - Search Tasks: Search for tasks by keyword
    """
    messagebox.showinfo("Help", help_message)

app = tk.Tk()
app.title("Task Manager")

style = ttk.Style()
style.theme_use('clam')

# Set custom colors and font
style.configure("Treeview", background="#FFFFFF", foreground="black", rowheight=25, fieldbackground="#D3D3D3", font=('Helvetica', 10))
style.map('Treeview', background=[('selected', '#4CAF50')], foreground=[('selected', 'white')])
style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), background="#4CAF50", foreground="white")
style.configure("TLabel", font=('Helvetica', 12))
style.configure("TButton", font=('Helvetica', 10), background="#4CAF50", foreground="white")
style.configure("TFrame", background="#D3D3D3")
style.configure("TLabelframe", background="#D3D3D3")
style.configure("TLabelframe.Label", font=('Helvetica', 12, 'bold'))

# Task List
task_frame = ttk.Labelframe(app, text="Tasks")
task_frame.pack(padx=10, pady=10, fill="both", expand=True)

task_listbox = ttk.Treeview(task_frame, columns=("Task", "Status", "Due Date", "Priority", "Category"), show="headings", height=10)
task_listbox.heading("Task", text="Task")
task_listbox.heading("Status", text="Status")
task_listbox.heading("Due Date", text="Due Date")
task_listbox.heading("Priority", text="Priority")
task_listbox.heading("Category", text="Category")
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

task_scrollbar = ttk.Scrollbar(task_frame, orient="vertical", command=task_listbox.yview)
task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox.config(yscrollcommand=task_scrollbar.set)

# Search Result List
result_frame = ttk.Labelframe(app, text="Search Results")
result_frame.pack(padx=10, pady=10, fill="both", expand=True)

result_listbox = ttk.Treeview(result_frame, columns=("Task", "Status", "Due Date", "Priority", "Category"), show="headings", height=10)
result_listbox.heading("Task", text="Task")
result_listbox.heading("Status", text="Status")
result_listbox.heading("Due Date", text="Due Date")
result_listbox.heading("Priority", text="Priority")
result_listbox.heading("Category", text="Category")
result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_listbox.yview)
result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_listbox.config(yscrollcommand=result_scrollbar.set)

# Buttons
button_frame = ttk.Frame(app)
button_frame.pack(pady=10)

add_button = ttk.Button(button_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=0, padx=10)

delete_button = ttk.Button(button_frame, text="Delete Task", command=delete_task)
delete_button.grid(row=0, column=1, padx=10)

complete_button = ttk.Button(button_frame, text="Mark Task Completed", command=mark_task_completed)
complete_button.grid(row=0, column=2, padx=10)

search_button = ttk.Button(button_frame, text="Search Tasks", command=search_tasks)
search_button.grid(row=0, column=3, padx=10)

help_button = ttk.Button(button_frame, text="Help", command=show_help)
help_button.grid(row=0, column=4, padx=10)

load_tasks()
refresh_tasks()
app.mainloop()

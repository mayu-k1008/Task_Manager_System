import tkinter as tk
from tkinter import messagebox

tasks = []

def add_task():
    task = task_entry.get()
    if task:
        tasks.append({"task": task, "completed": False})
        update_tasks()
        task_entry.delete(0, tk.END)

def delete_task(task_index):
    try:
        removed_task = tasks.pop(task_index)
        update_tasks()
        messagebox.showinfo("Deleted", f'Deleted task: {removed_task["task"]}')
    except IndexError:
        messagebox.showwarning("Error", "Invalid task number")

def mark_task_completed(task_index):
    try:
        tasks[task_index]["completed"] = True
        update_tasks()
        messagebox.showinfo("Completed", f'Marked task as completed: {tasks[task_index]["task"]}')
    except IndexError:
        messagebox.showwarning("Error", "Invalid task number")

def update_tasks():
    for widget in task_frame.winfo_children():
        widget.destroy()
    for i, task in enumerate(tasks):
        task_text = f'{i + 1}. {task["task"]} [{"Completed" if task["completed"] else "Pending"}]'
        task_label = tk.Label(task_frame, text=task_text, bg="#f0f4f7", fg="#333333", font=("Helvetica", 12), anchor="w", width=50)
        task_label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
        complete_button = tk.Button(task_frame, text="Complete", command=lambda i=i: mark_task_completed(i), bg="#d0e8f2", fg="#333333", font=("Helvetica", 10), padx=10, pady=5)
        complete_button.grid(row=i, column=1, padx=5, pady=5)
        delete_button = tk.Button(task_frame, text="Delete", command=lambda i=i: delete_task(i), bg="#f9c0c0", fg="#333333", font=("Helvetica", 10), padx=10, pady=5)
        delete_button.grid(row=i, column=2, padx=5, pady=5)

def view_tasks():
    view_window = tk.Toplevel(app)
    view_window.title("View Tasks")
    view_window.geometry("400x300")
    view_window.configure(bg="#f0f4f7")
    view_frame = tk.Frame(view_window, bg="#f0f4f7", padx=10, pady=10)
    view_frame.pack(pady=10, padx=10)
    
    if not tasks:
        tk.Label(view_frame, text="No tasks available", bg="#f0f4f7", fg="#333333", font=("Helvetica", 12), pady=10).pack()
    else:
        for i, task in enumerate(tasks):
            task_text = f'{i + 1}. {task["task"]} [{"Completed" if task["completed"] else "Pending"}]'
            tk.Label(view_frame, text=task_text, bg="#f0f4f7", fg="#333333", font=("Helvetica", 12), padx=10, pady=5, anchor="w", width=50).pack()

app = tk.Tk()
app.title("Task Manager")

header = tk.Label(app, text="Task Manager", font=("Helvetica", 24, "bold"), bg="#3f72af", fg="white", pady=10)
header.pack(fill=tk.X)

frame = tk.Frame(app, bg="#3f72af", pady=10, padx=10)
frame.pack(pady=10, padx=10)

task_entry = tk.Entry(frame, width=40, font=("Helvetica", 14))
task_entry.pack(side=tk.LEFT, padx=(0, 10))

add_button = tk.Button(frame, text="Add Task", command=add_task, bg="#3f72af", fg="white", font=("Helvetica", 12), padx=10)
add_button.pack(side=tk.LEFT)

task_frame = tk.Frame(app, bg="#f0f4f7", padx=10, pady=10)
task_frame.pack(pady=10, padx=10)

view_button = tk.Button(app, text="View Tasks", command=view_tasks, bg="#3f72af", fg="white", font=("Helvetica", 12), padx=10, pady=5)
view_button.pack(pady=10)

update_tasks()

app.mainloop()

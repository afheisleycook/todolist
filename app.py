import tkinter
from tkinter import simpledialog, messagebox
import sqlite3
import os

class ToDoApp(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List App")
        self.geometry("400x500")
        self.tasks = []
        self.db_file = "tasks.db"
        
        # Initialize database
        self.init_db()
        
        # Load tasks from database
        self.load_tasks()
        
        # Title Label
        self.lblTitle = tkinter.Label(master=self, text="My To-Do List", font=("Arial", 16, "bold"))
        self.lblTitle.pack(pady=10)
        
        # Listbox to display tasks
        self.task_listbox = tkinter.Listbox(master=self, height=15, width=45, font=("Arial", 10))
        self.task_listbox.pack(pady=10, padx=10)
        self.refresh_listbox()
        
        # Frame for buttons
        self.btn_frame = tkinter.Frame(master=self)
        self.btn_frame.pack(pady=10)
        
        # Add Task Button
        self.btn_add = tkinter.Button(master=self.btn_frame, text="Add Task", command=self.add_task, 
                                      bg="green", fg="white", font=("Arial", 10), width=12)
        self.btn_add.grid(row=0, column=0, padx=5)
        
        # Delete Task Button
        self.btn_delete = tkinter.Button(master=self.btn_frame, text="Delete Task", command=self.delete_task, 
                                         bg="red", fg="white", font=("Arial", 10), width=12)
        self.btn_delete.grid(row=0, column=1, padx=5)
        
        # Mark Complete Button
        self.btn_complete = tkinter.Button(master=self.btn_frame, text="Mark Complete", command=self.mark_complete, 
                                           bg="blue", fg="white", font=("Arial", 10), width=12)
        self.btn_complete.grid(row=1, column=0, padx=5, pady=5)
        
        # Clear All Button
        self.btn_clear = tkinter.Button(master=self.btn_frame, text="Clear All", command=self.clear_all, 
                                        bg="orange", fg="white", font=("Arial", 10), width=12)
        self.btn_clear.grid(row=1, column=1, padx=5, pady=5)
    
    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a new task:")
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.save_tasks()
            self.refresh_listbox()
            messagebox.showinfo("Success", "Task added successfully!")
    
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_index)
            self.save_tasks()
            self.refresh_listbox()
            messagebox.showinfo("Success", "Task deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select a task to delete!")
    
    def mark_complete(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"]
            self.save_tasks()
            self.refresh_listbox()
        except IndexError:
            messagebox.showerror("Error", "Please select a task to mark complete!")
    
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks = []
            self.save_tasks()
            self.refresh_listbox()
    
    def refresh_listbox(self):
        self.task_listbox.delete(0, tkinter.END)
        for idx, item in enumerate(self.tasks, 1):
            status = "✓" if item["completed"] else " "
            display_text = f"[{status}] {item['task']}"
            self.task_listbox.insert(tkinter.END, display_text)
    
    def save_tasks(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        for item in self.tasks:
            cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", 
                         (item["task"], item["completed"]))
        conn.commit()
        conn.close()
    
    def load_tasks(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, completed FROM tasks")
        rows = cursor.fetchall()
        self.tasks = [{"id": row[0], "task": row[1], "completed": bool(row[2])} for row in rows]
        conn.close()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()


todo = ToDoApp()
todo.mainloop()
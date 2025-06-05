import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import datetime
from typing import Optional, Callable
import json

class TaskList(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tasks = []
        self.setup_ui()

    def setup_ui(self):
        # Create the treeview
        self.tree = ttk.Treeview(self, columns=("Title", "Category", "Priority", "Due Date", "Status"),
                                show="headings", selectmode="browse")
        
        # Configure columns
        self.tree.heading("Title", text="Title")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Title", width=200)
        self.tree.column("Category", width=100)
        self.tree.column("Priority", width=80)
        self.tree.column("Due Date", width=100)
        self.tree.column("Status", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_task(self, task: dict):
        self.tasks.append(task)
        status = "✓" if task.get("completed", False) else "○"
        self.tree.insert("", "end", values=(
            task["title"],
            task.get("category", ""),
            task.get("priority", "Medium"),
            task.get("due_date", ""),
            status
        ))

    def clear_tasks(self):
        self.tasks.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

class MainWindow(ThemedTk):
    def __init__(self):
        super().__init__(theme="arc")  # Using a modern theme
        
        self.title("TaskMaster")
        self.geometry("800x600")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create header
        header = ttk.Frame(main_container)
        header.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(header, text="TaskMaster", font=("Helvetica", 24, "bold"))
        title_label.pack(side="left")
        
        # Create buttons frame
        buttons_frame = ttk.Frame(header)
        buttons_frame.pack(side="right")
        
        add_button = ttk.Button(buttons_frame, text="Add Task", command=self.add_task)
        add_button.pack(side="left", padx=5)
        
        edit_button = ttk.Button(buttons_frame, text="Edit Task", command=self.edit_task)
        edit_button.pack(side="left", padx=5)
        
        delete_button = ttk.Button(buttons_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side="left", padx=5)
        
        # Create task list
        self.task_list = TaskList(main_container)
        self.task_list.pack(fill="both", expand=True)
        
        # Create status bar
        self.status_bar = ttk.Label(main_container, text="Ready", relief="sunken", padding=5)
        self.status_bar.pack(fill="x", pady=(10, 0))

    def add_task(self):
        # This will be implemented in the task dialog
        pass

    def edit_task(self):
        # This will be implemented in the task dialog
        pass

    def delete_task(self):
        selected = self.task_list.tree.selection()
        if not selected:
            self.status_bar.config(text="No task selected")
            return
        
        # This will be implemented with database integration
        pass

    def update_status(self, message: str):
        self.status_bar.config(text=message) 
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import Optional, Dict, Callable

class TaskDialog(tk.Toplevel):
    def __init__(self, parent, task: Optional[Dict] = None, on_save: Callable = None):
        super().__init__(parent)
        
        self.task = task or {}
        self.on_save = on_save
        
        self.title("Add Task" if not task else "Edit Task")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        self.load_task_data()
        
        # Center the dialog
        self.center_window()
        
    def setup_ui(self):
        # Create main container
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(main_frame, text="Title:").pack(anchor="w", pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.pack(fill="x", pady=(0, 10))
        
        # Description
        ttk.Label(main_frame, text="Description:").pack(anchor="w", pady=(0, 5))
        self.description_text = tk.Text(main_frame, height=4, width=40)
        self.description_text.pack(fill="x", pady=(0, 10))
        
        # Category
        ttk.Label(main_frame, text="Category:").pack(anchor="w", pady=(0, 5))
        self.category_entry = ttk.Entry(main_frame, width=40)
        self.category_entry.pack(fill="x", pady=(0, 10))
        
        # Priority
        ttk.Label(main_frame, text="Priority:").pack(anchor="w", pady=(0, 5))
        self.priority_var = tk.StringVar(value="Medium")
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill="x", pady=(0, 10))
        
        priorities = ["Low", "Medium", "High"]
        for priority in priorities:
            ttk.Radiobutton(priority_frame, text=priority, value=priority,
                           variable=self.priority_var).pack(side="left", padx=5)
        
        # Due Date
        ttk.Label(main_frame, text="Due Date:").pack(anchor="w", pady=(0, 5))
        self.due_date_entry = ttk.Entry(main_frame, width=40)
        self.due_date_entry.pack(fill="x", pady=(0, 10))
        ttk.Label(main_frame, text="Format: YYYY-MM-DD").pack(anchor="w")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(button_frame, text="Save", command=self.save_task).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="right", padx=5)
        
    def load_task_data(self):
        if self.task:
            self.title_entry.insert(0, self.task.get("title", ""))
            self.description_text.insert("1.0", self.task.get("description", ""))
            self.category_entry.insert(0, self.task.get("category", ""))
            self.priority_var.set(self.task.get("priority", "Medium"))
            self.due_date_entry.insert(0, self.task.get("due_date", ""))
            
    def save_task(self):
        task_data = {
            "title": self.title_entry.get().strip(),
            "description": self.description_text.get("1.0", "end-1c").strip(),
            "category": self.category_entry.get().strip(),
            "priority": self.priority_var.get(),
            "due_date": self.due_date_entry.get().strip()
        }
        
        if not task_data["title"]:
            tk.messagebox.showerror("Error", "Title is required!")
            return
            
        if self.on_save:
            self.on_save(task_data)
        self.destroy()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}') 
import tkinter as tk
from tkinter import messagebox
from ui.main_window import MainWindow
from ui.task_dialog import TaskDialog
from database import Database

class TaskMaster:
    def __init__(self):
        self.db = Database()
        self.window = MainWindow()
        self.setup_handlers()
        self.load_tasks()
        
    def setup_handlers(self):
        self.window.add_task = self.show_add_task_dialog
        self.window.edit_task = self.show_edit_task_dialog
        self.window.delete_task = self.delete_selected_task
        
    def load_tasks(self):
        self.window.task_list.clear_tasks()
        tasks = self.db.get_all_tasks()
        for task in tasks:
            self.window.task_list.add_task(task)
            
    def show_add_task_dialog(self):
        dialog = TaskDialog(self.window, on_save=self.add_task)
        self.window.wait_window(dialog)
        
    def show_edit_task_dialog(self):
        selected = self.window.task_list.tree.selection()
        if not selected:
            self.window.update_status("No task selected")
            return
            
        task_id = selected[0]
        task = self.db.get_all_tasks()[int(task_id) - 1]  # Assuming IDs are sequential
        dialog = TaskDialog(self.window, task=task, on_save=lambda data: self.update_task(task_id, data))
        self.window.wait_window(dialog)
        
    def add_task(self, task_data):
        task_id = self.db.add_task(**task_data)
        if task_id:
            task_data["id"] = task_id
            self.window.task_list.add_task(task_data)
            self.window.update_status("Task added successfully")
        else:
            messagebox.showerror("Error", "Failed to add task")
            
    def update_task(self, task_id, task_data):
        if self.db.update_task(task_id, **task_data):
            self.load_tasks()  # Reload all tasks
            self.window.update_status("Task updated successfully")
        else:
            messagebox.showerror("Error", "Failed to update task")
            
    def delete_selected_task(self):
        selected = self.window.task_list.tree.selection()
        if not selected:
            self.window.update_status("No task selected")
            return
            
        task_id = selected[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            if self.db.delete_task(task_id):
                self.window.task_list.tree.delete(task_id)
                self.window.update_status("Task deleted successfully")
            else:
                messagebox.showerror("Error", "Failed to delete task")
                
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TaskMaster()
    app.run() 
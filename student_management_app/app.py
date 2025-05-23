import tkinter as tk
from tkinter import ttk, messagebox
import os

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - Login")
        self.root.geometry("800x600")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#f5f5f5')
        self.style.configure('Custom.TButton', 
                           background='#1a237e',
                           foreground='white',
                           padding=10)
        self.style.configure('Custom.TLabel',
                           background='#f5f5f5',
                           foreground='#333333',
                           font=('Helvetica', 10))
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create login frame
        self.login_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Login title
        ttk.Label(self.login_frame, 
                 text="Login",
                 font=('Helvetica', 20, 'bold'),
                 style='Custom.TLabel').pack(pady=20)
        
        # Username
        ttk.Label(self.login_frame,
                 text="Username:",
                 style='Custom.TLabel').pack(pady=5)
        self.username = ttk.Entry(self.login_frame, width=30)
        self.username.pack(pady=5)
        
        # Password
        ttk.Label(self.login_frame,
                 text="Password:",
                 style='Custom.TLabel').pack(pady=5)
        self.password = ttk.Entry(self.login_frame, width=30, show="*")
        self.password.pack(pady=5)
        
        # Login button
        login_btn = tk.Button(self.login_frame,
                            text="Login",
                            command=self.login,
                            bg='#1a237e',
                            fg='white',
                            font=('Helvetica', 10),
                            width=20,
                            height=2)
        login_btn.pack(pady=20)
        
        # Default credentials
        self.valid_credentials = {"admin": "admin123"}

    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        if username in self.valid_credentials and self.valid_credentials[username] == password:
            self.root.withdraw()  # Hide login window
            dashboard = tk.Toplevel()
            app = Dashboard(dashboard, username)
        else:
            messagebox.showerror("Error", "Invalid username or password")

class Dashboard:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Student Management System - Dashboard")
        self.root.geometry("1200x700")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Sidebar.TFrame', background='#1a237e')
        self.style.configure('Content.TFrame', background='#f5f5f5')
        self.style.configure('Custom.TButton',
                           background='#009688',
                           foreground='white',
                           padding=10)
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content area
        self.create_content_area()
        
        # Initialize student data
        self.students = [
            {"id": 1, "name": "John Doe", "age": 16, "grade": "10th"},
        ]
        
        # Populate student table
        self.update_student_table()

    def create_sidebar(self):
        sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Sidebar buttons
        buttons = ['Dashboard', 'Students', 'Reports', 'Settings']
        for btn_text in buttons:
            btn = tk.Button(sidebar,
                          text=btn_text,
                          bg='#1a237e',
                          fg='white',
                          font=('Helvetica', 10),
                          width=20,
                          height=2,
                          relief=tk.FLAT)
            btn.pack(pady=5)
        
        # Logout button at bottom
        tk.Button(sidebar,
                 text="Logout",
                 command=self.logout,
                 bg='#009688',
                 fg='white',
                 font=('Helvetica', 10),
                 width=20,
                 height=2,
                 relief=tk.FLAT).pack(side=tk.BOTTOM, pady=20)

    def create_content_area(self):
        content = ttk.Frame(self.main_container, style='Content.TFrame')
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Search frame
        search_frame = ttk.Frame(content, style='Content.TFrame')
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame,
                               textvariable=self.search_var,
                               width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame,
                             text="Search",
                             command=self.search_students,
                             bg='#009688',
                             fg='white',
                             font=('Helvetica', 10))
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = ttk.Frame(content, style='Content.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Create Treeview
        self.tree = ttk.Treeview(table_frame,
                                columns=('ID', 'Name', 'Age', 'Grade'),
                                show='headings')
        
        # Define headings
        for col in ('ID', 'Name', 'Age', 'Grade'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        btn_frame = ttk.Frame(content, style='Content.TFrame')
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Action buttons
        actions = [
            ('Add Student', self.add_student),
            ('Edit Student', self.edit_student),
            ('Delete Student', self.delete_student)
        ]
        
        for text, command in actions:
            btn = tk.Button(btn_frame,
                          text=text,
                          command=command,
                          bg='#009688',
                          fg='white',
                          font=('Helvetica', 10))
            btn.pack(side=tk.LEFT, padx=5)

    def update_student_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert students
        for student in self.students:
            self.tree.insert('', tk.END, values=(
                student['id'],
                student['name'],
                student['age'],
                student['grade']
            ))

    def add_student(self):
        # Create add student window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("300x300")
        
        # Entry variables
        name_var = tk.StringVar()
        age_var = tk.StringVar()
        grade_var = tk.StringVar()
        
        # Create entry fields
        ttk.Label(add_window, text="Name:").pack(pady=5)
        ttk.Entry(add_window, textvariable=name_var).pack(pady=5)
        
        ttk.Label(add_window, text="Age:").pack(pady=5)
        ttk.Entry(add_window, textvariable=age_var).pack(pady=5)
        
        ttk.Label(add_window, text="Grade:").pack(pady=5)
        ttk.Entry(add_window, textvariable=grade_var).pack(pady=5)
        
        def save():
            # Get new ID
            new_id = max([s['id'] for s in self.students], default=0) + 1
            
            # Create new student
            new_student = {
                'id': new_id,
                'name': name_var.get(),
                'age': int(age_var.get()),
                'grade': grade_var.get()
            }
            
            # Add to list and update table
            self.students.append(new_student)
            self.update_student_table()
            add_window.destroy()
        
        # Save button
        tk.Button(add_window,
                 text="Save",
                 command=save,
                 bg='#009688',
                 fg='white').pack(pady=20)

    def edit_student(self):
        # Get selected item
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        # Get student data
        student_id = self.tree.item(selected)['values'][0]
        student = next((s for s in self.students if s['id'] == student_id), None)
        
        if student:
            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Student")
            edit_window.geometry("300x300")
            
            # Entry variables
            name_var = tk.StringVar(value=student['name'])
            age_var = tk.StringVar(value=str(student['age']))
            grade_var = tk.StringVar(value=student['grade'])
            
            # Create entry fields
            ttk.Label(edit_window, text="Name:").pack(pady=5)
            ttk.Entry(edit_window, textvariable=name_var).pack(pady=5)
            
            ttk.Label(edit_window, text="Age:").pack(pady=5)
            ttk.Entry(edit_window, textvariable=age_var).pack(pady=5)
            
            ttk.Label(edit_window, text="Grade:").pack(pady=5)
            ttk.Entry(edit_window, textvariable=grade_var).pack(pady=5)
            
            def save():
                # Update student data
                student['name'] = name_var.get()
                student['age'] = int(age_var.get())
                student['grade'] = grade_var.get()
                
                # Update table
                self.update_student_table()
                edit_window.destroy()
            
            # Save button
            tk.Button(edit_window,
                     text="Save",
                     command=save,
                     bg='#009688',
                     fg='white').pack(pady=20)

    def delete_student(self):
        # Get selected item
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            # Get student ID and remove from list
            student_id = self.tree.item(selected)['values'][0]
            self.students = [s for s in self.students if s['id'] != student_id]
            
            # Update table
            self.update_student_table()

    def search_students(self):
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter and insert matching students
        for student in self.students:
            if (search_term in student['name'].lower() or
                search_term in str(student['age']).lower() or
                search_term in student['grade'].lower()):
                self.tree.insert('', tk.END, values=(
                    student['id'],
                    student['name'],
                    student['age'],
                    student['grade']
                ))

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

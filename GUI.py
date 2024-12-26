import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc

# Database connection function
def connect_to_db():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=AMR-HATEM;"
            "DATABASE=Hotel_DB;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
        return None

# Fetch table names
def fetch_table_names():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching tables: {str(e)}")
        return []

# Function to open table window and generate form
def open_table_window(table_name, right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()  # Clear the frame
    
    def insert_data():
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Create dynamic insert query
            columns_str = ', '.join(entries.keys())
            placeholders = ', '.join(['?'] * len(entries))
            values = [entry.get() for entry in entries.values()]

            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            cursor.execute(query, values)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Data successfully inserted into {table_name}.")
            show_data()  # Refresh data after inserting
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert data: {str(e)}")

    def show_data():
        try:
            for widget in data_frame.winfo_children():
                widget.destroy()  # Clear the data display area

            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

            # Table headers
            for col_index, col_name in enumerate(col_names):
                label = tk.Label(data_frame, text=col_name, font=("Arial", 10, "bold"), bg="lightgray", relief="ridge")
                label.grid(row=0, column=col_index, sticky="nsew", padx=1, pady=1)

            # Table rows
            for row_index, row in enumerate(rows):
                for col_index, value in enumerate(row):
                    label = tk.Label(data_frame, text=value, font=("Arial", 10), relief="ridge")
                    label.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=1, pady=1)

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

    # Fetch column names dynamically
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
        columns = [row[0] for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch columns: {str(e)}")
        return

    # Generate the form for data input
    tk.Label(right_frame, text=f"Add Data to {table_name}", font=("Arial", 14, "bold")).pack(pady=5)
    form_frame = tk.Frame(right_frame)
    form_frame.pack(pady=10)
    entries = {}

    for i, column in enumerate(columns):
        tk.Label(form_frame, text=column, font=("Arial", 10)).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(form_frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[column] = entry

    # Buttons
    button_frame = tk.Frame(right_frame)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Save", bg="blue", fg="white", command=insert_data).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Show Data", bg="blue", fg="white", command=show_data).grid(row=0, column=1, padx=5)

    # Data display frame
    data_frame = tk.Frame(right_frame)
    data_frame.pack(fill="both", expand=True)

# Main Application GUI
def main_gui():
    root = tk.Tk()
    root.title("Hotel Management Database")
    root.geometry("1000x600")

    # Left Frame: Table List
    left_frame = tk.Frame(root, bg="lightblue", width=250)
    left_frame.pack(side="left", fill="y")
    tk.Label(left_frame, text="Tables", font=("Arial", 14, "bold"), fg="white", bg="blue").pack(fill="x", pady=5)
    table_listbox = tk.Listbox(left_frame, font=("Arial", 12))
    table_listbox.pack(padx=10, pady=10, fill="y", expand=True)

    # Load tables into the listbox
    tables = fetch_table_names()
    for table in tables:
        table_listbox.insert(tk.END, table)

    # Right Frame: Dynamic form and data display
    right_frame = tk.Frame(root, bg="white")
    right_frame.pack(side="right", fill="both", expand=True)

    # On table selection, open the respective form
    def on_table_select(event):
        selected_table = table_listbox.get(table_listbox.curselection())
        open_table_window(selected_table, right_frame)

    table_listbox.bind("<<ListboxSelect>>", on_table_select)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    main_gui()
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# Constants
CSV_FILE = 'inventory.csv'

# Helper functions
def load_inventory():
    inventory = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                inventory.append(row)
    return inventory

def save_inventory(inventory):
    with open(CSV_FILE, 'w', newline='') as file:
        fieldnames = ['Item Name', 'Type', 'Serial Number', 'Location', 'Purchase Date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)

def add_item(item):
    inventory = load_inventory()
    inventory.append(item)
    save_inventory(inventory)

def delete_item(serial_number):
    inventory = load_inventory()
    inventory = [item for item in inventory if item['Serial Number'] != serial_number]
    save_inventory(inventory)

def search_inventory(query):
    inventory = load_inventory()
    return [item for item in inventory if query.lower() in item['Item Name'].lower() or query.lower() in item['Serial Number'].lower()]

# GUI setup
root = tk.Tk()
root.title("Inventory Tracker")

# GUI components
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
item_name_entry = tk.Entry(frame, width=30)
item_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
type_entry = tk.Entry(frame, width=30)
type_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Serial Number:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
serial_entry = tk.Entry(frame, width=30)
serial_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Location:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
location_entry = tk.Entry(frame, width=30)
location_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame, text="Purchase Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
purchase_date_entry = tk.Entry(frame, width=30)
purchase_date_entry.grid(row=4, column=1, padx=5, pady=5)

def add_inventory_item():
    item = {
        "Item Name": item_name_entry.get(),
        "Type": type_entry.get(),
        "Serial Number": serial_entry.get(),
        "Location": location_entry.get(),
        "Purchase Date": purchase_date_entry.get()
    }
    add_item(item)
    messagebox.showinfo("Success", "Item added to inventory.")
    clear_entries()
    load_table()

def delete_inventory_item():
    serial_number = serial_entry.get()
    delete_item(serial_number)
    messagebox.showinfo("Success", "Item deleted from inventory.")
    clear_entries()
    load_table()

def search_inventory_items():
    query = search_entry.get()
    results = search_inventory(query)
    load_table(results)

def clear_entries():
    item_name_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    serial_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    purchase_date_entry.delete(0, tk.END)

# Inventory table
tree = ttk.Treeview(root, columns=('Item Name', 'Type', 'Serial Number', 'Location', 'Purchase Date'), show='headings')
tree.heading('Item Name', text='Item Name')
tree.heading('Type', text='Type')
tree.heading('Serial Number', text='Serial Number')
tree.heading('Location', text='Location')
tree.heading('Purchase Date', text='Purchase Date')
tree.pack(pady=10)

def load_table(data=None):
    for row in tree.get_children():
        tree.delete(row)
    inventory = data if data else load_inventory()
    for item in inventory:
        tree.insert("", tk.END, values=(item['Item Name'], item['Type'], item['Serial Number'], item['Location'], item['Purchase Date']))

load_table()

# Buttons
tk.Button(root, text="Add Item", command=add_inventory_item).pack(pady=5)
tk.Button(root, text="Delete Item by Serial", command=delete_inventory_item).pack(pady=5)

# Search feature
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_inventory_items).pack(side=tk.LEFT)

root.mainloop()

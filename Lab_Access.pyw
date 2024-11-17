import subprocess
import pandas as pd
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import os

username = os.getlogin()

connection_triggered = False
connection_info = None

def update_connection_info(ip_address, port):
    global connection_triggered, connection_info

    if connection_info:
        connection_info.destroy()

    connection_info = Label(window, text=f"Connection ended\n\nName: '{clicked_name.get()}'  Host: '{ip_address}'  Port: '{str(port).strip()}'", fg="red")
    connection_info.place(x=0, y=115)
    connection_info.config(bg="lightgrey", font=("Helvetica", 9, "normal"))
    connection_triggered = True

def open_tera_term(ip_address, port):
    '''Run Tera Term.'''
    global connection_triggered, connection_info
    file_path = r"C:\Program Files (x86)\teraterm\ttermpro.exe"
    terra_term = [file_path, f"{ip_address}:{port}"]
    
    subprocess.run(terra_term)
    
    update_connection_info(ip_address, port)
    
    print(f"Command executed: {terra_term}")
  
def open_putty(ip_address, port):
    '''Run Tera Term.'''
    global connection_triggered, connection_info
    file_path = r"C:\Program Files\PuTTY\putty.exe"
    putty = [file_path, '-P', str(port), ip_address]
    
    subprocess.run(putty)
    
    update_connection_info(ip_address, port)
    
    print(f"Command executed: {putty}")

def load_data():
    '''Load backbone and access server data'''
    global df_backbone, df_access
    # Load Backbone data
    backbone_file = pd.read_csv(fr"C:\Users\{username}\path\to\Backbone_List.csv")
    df_backbone = pd.DataFrame(backbone_file)

    df_backbone["Port"] = df_backbone["Port"].fillna(0).astype(int)
    df_backbone["Host"] = df_backbone["Host"].fillna(0).astype(str)
    df_backbone["Name"] = df_backbone["Name"].fillna(0).astype(str)

    # Load Access Server data
    access_server_file = pd.read_csv(fr"C:\Users\{username}\path\to\Access_Server_List.csv")
    df_access = pd.DataFrame(access_server_file)

    df_access["Port"] = df_access["Port"].fillna(0).replace(0, 22)
    df_access["Host"] = df_access["Host"].fillna(0).astype(str)
    df_access["Name"] = df_access["Name"].fillna(0).astype(str)

load_data()

# Initialize main window
window = Tk()
window.title("Lab Access Tool")
window.config(padx=55, pady=70, bg='lightgray')

window.bind('<Return>', lambda event: (
    [connect_button.invoke() if 'connect_button' in globals() and connect_button_focus == True else None,
     add_button.invoke() if 'add_button' in globals() and add_button_focus == True else None,
     delete_button.invoke() if 'delete_button' in globals() and delete_button_focus == True else None]
))

window_width = 450
window_height = 250

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
style = ttk.Style(window)
style.theme_use("classic")
style.configure('W.TButton',
                font=('calibri', 10, 'normal'),
                foreground = 'black')
style.configure('TButton',
                font=('calibri', 10, 'normal', 'underline'))
style.configure('Custom.TButton',
                background='lightgrey',
                foreground='navy',
                font=('Arial', 10, 'bold'))
style.configure("TCombobox",
                foreground="black",
                background="#f0f0f0",
                font=("Arial", 12),
                padding=5)

# Style for the combobox dropdown menu
style.map("TCombobox",
          background=[('readonly', '#f0f0f0'), ('active', '#d0d0d0')],  # Background color on active state
          foreground=[('readonly', 'black'), ('active', 'blue')],  # Text color on active state
          fieldbackground=[('readonly', '#f0f0f0'), ('active', '#d0d0d0')])  # Background when it's active

style.map('TButton', foreground = [('active', '!disabled', 'darkblue')])

# Define StringVars
clicked_rack = StringVar(window) 
clicked_rack.set("Racks")

clicked_name = StringVar(window)
clicked_name.set("Name") 

# Determine which DataFrame to use based on the context
current_data = df_backbone

def update_hosts():
    '''Update the Host data'''
    selected_rack = clicked_rack.get()
    filtered_names = current_data[current_data["Rack"] == selected_rack]
    filtered_names = filtered_names.sort_values(by="Name")
    
    # Clear current host menu
    name_menu['values'] = []

    # Add new hosts to the menu
    valid_hosts = filtered_names[filtered_names["Name"].notna() & (filtered_names["Name"] != "0")]
    
    if valid_hosts.empty or (filtered_names["Name"] == "0").all():
        name_menu['values'] = ["No available hosts"]
    else:
        host_names = valid_hosts["Name"].tolist()
        name_menu['values'] = host_names

def connect_terra_term():
    '''Function for connecting using Tera Term(Backbone)'''
    selected_name = clicked_name.get()
    selected_row = current_data[current_data["Name"] == selected_name]
    
    if not selected_row.empty:
        host = selected_row["Host"].values[0]
        port = selected_row["Port"].values[0]
        open_tera_term(host, port)
    else:
        messagebox.showerror(title="Host not found", message="Host not selected or host not found")

def connect_putty():
    '''Function for connecting using Putty(Access server)'''
    selected_name = clicked_name.get()
    selected_row = current_data[current_data["Name"] == selected_name]
    
    if not selected_row.empty:
        host = selected_row["Host"].values[0]
        port = selected_row["Port"].values[0]

        # Check if port is NaN and handle it
        if pd.isna(port):
            connect_button.config(command=connect_putty)
        else:
            # Convert to integer if it's a float
            port = int(port) if isinstance(port, float) else port
        
            if port != 22:
                print(f"This will connect to Tera Term. Port: {port}")
                open_tera_term(host, port)
            else:
                print(f"This will connect to Putty. Port: {port}")
                open_putty(host, port)
    else:
        messagebox.showerror(title="Host not found", message="Host not selected or host not found")

def use_backbone():
    """Update dropdowns to show Backbone data."""
    global current_data, connect_button
    backbone_button.config(style='Custom.TButton')
    access_server_button.config(style='W.TButton')
    
    current_data = df_backbone
    
    clicked_rack.set("Racks")
    
    # Update combobox values for racks
    rack_list = list(set(df_backbone["Rack"]))
    rack_menu['values'] = sorted(rack_list, reverse=True)
    
    # Clear the host menu for Backbone
    clicked_name.set("Name")
    name_menu['values'] = []
    
    clicked_rack.trace_add("write", lambda *args: update_hosts())
    
    connect_button.config(command=connect_terra_term)

def use_access_server():
    """Update dropdowns to show Access Server data."""
    global current_data, connect_button
    access_server_button.config(style='Custom.TButton')
    backbone_button.config(style='W.TButton')
    
    current_data = df_access
    
    clicked_rack.set("Racks")
    
    # Update combobox values for racks
    rack_list = list(set(df_access["Rack"]))
    rack_menu['values'] = sorted(rack_list, reverse=True)
    
    # Clear the host menu for Access Server
    clicked_name.set("Name")
    name_menu['values'] = []
    
    clicked_rack.trace_add("write", lambda *args: update_hosts())
    
    connect_button.config(command=connect_putty)
    
def reload_data():
    '''Reloads the df_backbone and df_access data'''
    global df_backbone, df_access
    df_backbone = pd.read_csv(fr"C:\Users\{username}\path\to\Backbone_List.csv")
    df_backbone["Port"] = df_backbone["Port"].fillna(0).astype(int)
    df_backbone["Host"] = df_backbone["Host"].fillna(0).astype(str)
    df_backbone["Name"] = df_backbone["Name"].fillna(0).astype(str)

    df_access = pd.read_csv(fr"C:\Users\{username}\path\to\Access_Server_List.csv")
    df_access["Port"] = df_access["Port"].fillna(0).replace(0, 22)
    df_access["Host"] = df_access["Host"].fillna(0).astype(str)
    df_access["Name"] = df_access["Name"].fillna(0).astype(str)
    
def go_back_update():
    '''Go back to the main menu from the 'Add' menu'''
    global df_backbone, df_access
    radio_button_bb.grid_forget()
    radio_button_access.grid_forget()
    host_entry.grid_forget()
    port_entry.grid_forget()
    name_entry.grid_forget()
    add_button.grid_forget()
    rack_menu.grid_forget()
    host_label.destroy()
    port_label.destroy()
    name_label.destroy()
    refresh_button.destroy()
    back_button.destroy()
    
    window.geometry(f"{window_width}x{window_height}")
    window.config(padx=60, pady=70)
    
    reload_data()
    main_menu()
    
def go_back_delete():
    '''Go back to the main menu from the 'Delete' menu'''
    global df_backbone, df_access, connection_triggered
    rack_menu.grid_forget()
    name_menu.grid_forget()
    delete_button.destroy()
    delete_back_button.destroy()
    new_backbone_button.destroy()
    new_access_server_button.destroy()
    
    if connection_triggered == True:
        connection_info.place_forget()
    
    window.geometry(f"{window_width}x{window_height}")
    window.config(padx=60, pady=70)
    
    connection_triggered = False
    
    reload_data()
    main_menu()
    
def refresh():
    '''Refresh the update menu'''
    host_entry.delete(0, END)
    port_entry.delete(0, END)
    name_entry.delete(0, END)
    host_entry.focus()
    
    radio_var.set(0)
    
def open_popup():
    '''Create a new Toplevel window'''
    global popup
    popup = Toplevel(window)
    popup.title("Add or Delete")
    popup.config(pady=15)
    
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    
    window_x = window.winfo_x()
    window_y = window.winfo_y()
    
    popup_width = 270
    popup_height = 140
    
    popup_x = window_x + (window_width // 2) - (popup_width // 2)
    popup_y = window_y + (window_height // 2) - (popup_height // 2)
    
    popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
    
    Label(popup, text="Please choose an option: ").pack(pady=10)

    popup_add_button = Button(popup, text="Add", command=update_close_popup)
    popup_add_button.pack(padx=40, pady=20, side=LEFT)
    popup_add_button.config(width=7)
    popup_delete_button = Button(popup, text="Delete", command=delete_close_popup)
    popup_delete_button.pack(padx=40, pady=20, side=LEFT)
    popup_delete_button.config(width=7)

def update_close_popup():
    '''Close the popup after 'Add' clicked'''
    update_menu()
    popup.destroy()
    
def delete_close_popup():
    '''Close the popup after 'Delete' clicked'''
    delete_menu()
    popup.destroy()
    
def update_menu():
    '''Transition to the update menu'''
    global radio_button_bb, radio_button_access, host_entry, port_entry, back_button, name_entry, add_button, radio_var, refresh_button, host_label, port_label, name_label, add_button_focus, delete_button_focus, connect_button_focus, connection_triggered
    backbone_button.place_forget()
    access_server_button.place_forget()
    name_menu.grid_forget()
    update_button.grid_forget()
    connect_button.grid_forget()
    
    if connection_triggered == True:
        connection_info.place_forget()
    
    connection_triggered = False
    
    window.config(padx=60, pady=45)
    window.geometry(f"{window_width + 80}x{window_height + 10}")
    rack_menu.grid(column=0, row=2, padx=5, pady=5)
    
    radio_var = IntVar()
    
    radio_button_bb = Radiobutton(window, text="Backbone", variable=radio_var, value=1)
    radio_button_bb.grid(column=1, row=0, pady=20, columnspan=2)
    radio_button_bb.config(bg="lightgray")
    
    radio_button_access = Radiobutton(window, text="Access Server", variable=radio_var, value=2)
    radio_button_access.grid(column=3, row=0, pady=20, columnspan=2)
    radio_button_access.config(bg="lightgray")
    
    back_button = ttk.Button(window, text="Back", command=go_back_update)
    back_button.place(x=-50, y=-40)
    
    refresh_button = ttk.Button(window, text="Refresh", command=refresh)
    refresh_button.place(x=380, y=-40)
    
    connect_button_focus = False
    delete_button_focus = False
    add_button_focus = True
    
    add_button = ttk.Button(window, text="Add", command=add_to_csv)
    add_button.grid(column=2, row=3, pady=15, columnspan=2)
    add_button.focus_set()
    
    host_entry = ttk.Entry()
    host_entry.grid(column=1, row=2, columnspan=2)
    host_entry.config(width=20)
    host_entry.focus()
    
    port_entry = ttk.Entry()
    port_entry.grid(column=2, row=2, columnspan=2)
    port_entry.config(width=6)
    
    name_entry = ttk.Entry()
    name_entry.grid(column=3, row=2, columnspan=2, padx=40, pady=5)
    name_entry.config(width=20)
    
    host_label = Label()
    host_label.place(x=120, y=50)
    host_label.config(text="Host", bg="lightgray")
    
    port_label = Label()
    port_label.place(x=208, y=50)
    port_label.config(text="Port", bg="lightgray")
    
    name_label = Label()
    name_label.place(x=283, y=50)
    name_label.config(text="Name", bg="lightgray")
    
def confirm_popup():
    '''Yes or No confirm popup for deletion'''
    global name_value, host_value, port_value
    
    if clicked_rack.get() == "Racks":
        messagebox.showerror(title="Error", message="Please specify a valid Rack")
    elif clicked_name.get() == "No available hosts":
        messagebox.showerror(title="Error", message="No available hosts to delete")
    else:
    
        selected_name = clicked_name.get()

        # Find the corresponding row in the current DataFrame
        if current_data.equals(df_backbone):
            selected_row = df_backbone[df_backbone["Name"] == selected_name]
        else:
            selected_row = df_access[df_access["Name"] == selected_name]

        # Get host and port values
        host_value = selected_row["Host"].values[0]
        port_value = selected_row["Port"].values[0]
        name_value = selected_name  # Already got the name from the dropdown

        print(f"Host: '{host_value}', Port: '{port_value}', Name: '{name_value}'")  # Debugging output

        # Confirmation dialog
        response = messagebox.askyesnocancel(title="Confirmation", 
                                            message=f"Are you sure you want to delete '{name_value}'? \nHost: {host_value}\nPort: {round(port_value)}")

        if response is True:
            remove_from_csv()
        else:
            pass
    
def delete_row(file_path, index_to_remove):
    '''Function for deleting row in csv file'''
    # Load csv file
    try: 
        # Load the CSV file
        delete_df = pd.read_csv(file_path)
        
        # Check if the index is valid
        if index_to_remove in delete_df.index:
            # Drop the row at the specified index using .iloc
            delete_df = delete_df.drop(delete_df.index[index_to_remove])
            
            # Save the updated DataFrame back to the CSV file
            delete_df.to_csv(file_path, index=False)
            print(f"Row at index {index_to_remove} has been removed.")
        else:
            print("Invalid index. No row removed.")
    except Exception as e:
        print(f"Error: {e}")

def remove_from_csv():
    '''Remove the name from the csv file'''
    global df_backbone, df_access
    selected_name = clicked_name.get()
    selected_row_backbone = df_backbone[df_backbone["Name"] == selected_name]
    selected_row_access = df_access[df_access["Name"] == selected_name]
    
    if clicked_rack.get() == "Racks":
        messagebox.showerror("Error", message="Please specify a valid Rack")
        return
    
    if clicked_name.get() == "No available hosts":
        messagebox.showerror("Error", message="No available hosts to delete")
        return
    
    if current_data.equals(df_backbone):
        if selected_row_backbone.empty:
            index = int(selected_row_backbone.index[0])
            messagebox.showerror("Error", "Selected name not found in Backbone")
            return
        index = selected_row_backbone.index[0]
        delete_row(fr"C:\Users\{username}\path\to\Backbone_List.csv", index)
        messagebox.showinfo(title="Deleted", message=f"Removed '{name_value}' from data file \nHost: {host_value}\nPort: {port_value}")
        
    elif current_data.equals(df_access):
        if selected_row_access.empty:
            index = int(selected_row_access.index[0])
            messagebox.showerror("Error", "Selected name not found in Access Server")
            return
        index = selected_row_access.index[0]
        delete_row(fr"C:\Users\{username}\path\to\Access_Server_List.csv", index)
        messagebox.showinfo(title="Deleted", message=f"Removed '{name_value}' from data file \nHost: {host_value}\nPort: {round(port_value)}")
    
    if current_data.equals(df_backbone):
        load_data()
        use_backbone()
    elif current_data.equals(df_access):
        load_data()
        use_access_server()
    
    reload_data()
    update_hosts()
            
def delete_menu():
    '''The delete menu'''
    global delete_back_button, delete_button, new_access_server_button, new_backbone_button, delete_button_focus, connect_button_focus, add_button_focus
    update_button.grid_forget()
    connect_button.grid_forget()
    
    backbone_button.place_forget()
    access_server_button.place_forget()
    
    if connection_triggered == True:
        connection_info.place_forget()
    
    window.geometry(f"{window_width - 15}x{window_height}")
    window.config(padx=100, pady=95)
    
    new_backbone_button = ttk.Button(window, text="Backbone", style='Custom.TButton', command=lambda: (use_backbone(), new_backbone_button.config(style='Custom.TButton'), new_access_server_button.config(style='W.TButton')))
    new_backbone_button.place(x=20, y=-50)
    new_access_server_button = ttk.Button(window, text="Access Server", style='W.TButton', command=lambda: (use_access_server(), new_access_server_button.config(style='Custom.TButton'), new_backbone_button.config(style='W.TButton')))
    new_access_server_button.place(x=120, y=-50)
    
    delete_back_button = ttk.Button(window, text="Back", command=go_back_delete)
    delete_back_button.place(x=-90, y=-90)
    
    connect_button_focus = False
    add_button_focus = False
    delete_button_focus = True
    
    delete_button = ttk.Button(window, text="Delete", command=confirm_popup)
    delete_button.place(x=90, y=60)
    delete_button.focus_set()
    
    # The Backbone data will be displayed by default
    use_backbone()
    
def add_to_csv():
    """Print the selected value of the radio button."""
    selected_value = radio_var.get()  # Get the value of the selected radio button
    print(f"You've selected: {selected_value}")
    
    def check_numbers(input_value):
        return input_value.isdigit() and len(input_value) <= 4

    def is_full_width(value):
        return all(ord(char) >= 128 for char in value)
    
    rack_data = clicked_rack.get()
    host_data = host_entry.get()
    port_data = port_entry.get()
    name_data = name_entry.get()

    new_data = pd.DataFrame({
        "Rack": [rack_data],
        "Host": [host_data],
        "Port": [port_data],
        "Name": [name_data],
    })
    
    if clicked_rack.get() == "Racks":
        messagebox.showerror("Error", message="Please specify a valid Rack")
    elif len(host_entry.get()) == 0 or len(name_entry.get()) == 0:
        messagebox.showerror("Error", message="Host and Name must not be empty")
    elif any(char.isspace() for char in host_entry.get()) or any(char.isspace() for char in port_entry.get()):
        messagebox.showerror("Error", message="Host and Port must not contain any whitespaces")
    elif name_entry.get()[0].isspace() or name_entry.get()[-1].isspace():
        messagebox.showerror("Error", message="First and last character in Name must not be a whitespace")
    elif len(host_entry.get()) > 20 or len(name_entry.get()) > 20:
        messagebox.showerror("Error", message="You've exceeded the maximum value length (max 20 characters)")
    elif is_full_width(host_entry.get()) or is_full_width(port_entry.get()) and port_entry.get() != "":
        messagebox.showerror("Error", message="Host and Port must not contain full-width characters")
    elif radio_var.get() == 0 or radio_var.get() == None:
        messagebox.showerror("Error", message="Please select one of the options")
    elif radio_var.get() == 2 and len(port_entry.get()) == 0:  # Allow empty for Access Server
        
        if selected_value == 1:
            new_data.to_csv(fr"C:\Users\{username}\path\to\Backbone_List.csv", mode="a", header=not pd.io.common.file_exists(fr"C:\Users\{username}\path\to\Backbone_List.csv"))
            messagebox.showinfo(title="Added", message=f"Added '{name_data}' to Backbone file")
        elif selected_value == 2:
            new_data.to_csv(fr"C:\Users\{username}\path\to\Access_Server_List.csv", mode="a", header=not pd.io.common.file_exists(fr"C:\Users\{username}\path\to\Access_Server_List.csv"))
            messagebox.showinfo(title="Added", message=f"Added '{name_data}' to Access Server file")
        
        refresh()
    elif not check_numbers(port_entry.get()):
        messagebox.showerror("Error", message="Port must be a number (max 4 digits)")
        
    else:
        is_duplicate = False
        load_data()
        if selected_value == 1:
            for name in df_backbone["Name"].to_list():
                if name_entry.get() in name:
                    response = messagebox.askyesnocancel("Error", message=f"The name: '{name_data}' already exists in Backbone file. Overwrite?\n\n'Yes' to overwrite 'No' to add anyway")
                    if response == None:
                        is_duplicate = True
                        break
                    elif response == False:
                        is_duplicate = False
                    elif response == True:
                        # Overwrite existing duplicate name
                        if name in df_backbone["Name"].to_list():
                            df_backbone.loc[df_backbone["Name"] == name, ["Rack", "Host", "Port", "Name"]] = [rack_data, host_data, port_data, name_data]
                            df_backbone.to_csv(fr"C:\Users\{username}\path\to\Backbone_List.csv", mode="w", header=True, index=False)
                            messagebox.showinfo(title="Updated", message=f"Overwritten '{name_data}' in Backbone file")
                            refresh()
                        is_duplicate = True
                    break
        elif selected_value == 2:
            for name in df_access["Name"].to_list():
                if name_entry.get() in name:
                    response = messagebox.askyesnocancel("Error", message=f"The name: '{name_data}' already exists in Access Server file. Overwrite?\n\n'Yes' to overwrite 'No' to add anyway")
                    if response == None:
                        is_duplicate = True
                        break
                    elif response == False:
                        is_duplicate = False
                    elif response == True:
                        # Overwrite existing duplicate name
                        if name in df_access["Name"].to_list():
                            df_access.loc[df_access["Name"] == name, ["Rack", "Host", "Port", "Name"]] = [rack_data, host_data, port_data, name_data]
                            df_access.to_csv(fr"C:\Users\{username}\path\to\Access_Server_List.csv", mode="w", header=True, index=False)
                            messagebox.showinfo(title="Updated", message=f"Overwritten '{name_data}' in Access Server file")
                            refresh()
                        is_duplicate = True
                    break

        if not is_duplicate:
            if selected_value == 1:
                new_data.to_csv(fr"C:\Users\{username}\path\to\Backbone_List.csv", mode="a", header=not pd.io.common.file_exists(fr"C:\Users\{username}\path\to\Backbone_List.csv"))
                messagebox.showinfo(title="Added", message=f"Added '{name_data}' to Backbone file \nHost: {host_data}\nPort: {port_data}")
            elif selected_value == 2:
                new_data.to_csv(fr"C:\Users\{username}\path\to\Access_Server_List.csv", mode="a", header=not pd.io.common.file_exists(fr"C:\Users\{username}\path\to\Access_Server_List.csv"))
                messagebox.showinfo(title="Added", message=f"Added '{name_data}' to Access Server file \nHost: {host_data}\nPort: {port_data}")
            
            load_data()
            refresh()
        
def on_focus_in(event):
    """Clears the text selection when the combobox is clicked."""
    event.widget.selection_clear()

def main_menu():
    '''The main menu'''
    global connect_button, backbone_button, access_server_button, name_menu, rack_menu, update_button, connect_button_focus, delete_button_focus, add_button_focus
    # Create buttons and menus
    backbone_button = ttk.Button(window, text="Backbone", style='W.TButton', command=use_backbone)
    backbone_button.place(x=50, y=-35)

    access_server_button = ttk.Button(window, text="Access Server", style='W.TButton', command=use_access_server)
    access_server_button.place(x=160, y=-35)

    rack_menu = ttk.Combobox(window, width=6, textvariable=clicked_rack, style="TCombobox")
    rack_menu.grid(column=0, row=1, padx=6, pady=5)
    rack_menu.bind("<FocusIn>", on_focus_in)

    name_menu = ttk.Combobox(window, textvariable=clicked_name, width=20)
    name_menu.grid(column=1, row=1, padx=13, pady=5)
    name_menu.bind("<FocusIn>", on_focus_in)

    update_button = ttk.Button(window, text="Update", command=open_popup)
    update_button.grid(column=1, row=2, pady=10)

    delete_button_focus = False
    add_button_focus = False
    connect_button_focus = True

    connect_button = ttk.Button(window, text="Connect", command=connect_terra_term)
    connect_button.grid(column=2, row=1, padx=5, pady=10)
    connect_button.focus_set()

    # Set initial trace for the Backbone data
    clicked_rack.trace_add("write", lambda *args: update_hosts())

    # The Backbone data will be displayed by default
    use_backbone()

main_menu()

window.mainloop()
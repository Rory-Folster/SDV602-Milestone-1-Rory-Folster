from email import message
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
from tkinter import END, messagebox

#https://data.world/bryantahb/crime-in-atlanta-2009-2017 - Original CSV location.

'''
Functions for creating seperate csv's for the different chart data we need. Kept for later revision if needed.
'''
# Highest crime areas pie chart csv

#df = pd.read_csv('data\\atlcrime.csv') #reading csv file
#df['count'] = 1
#new_df = df.groupby(['crime', 'neighborhood']).count()['count'].sort_values(ascending=False)
#new_df.to_csv('highest_crime_areas.csv')

# Total crimes bar chart csv

#df = pd.read_csv('data\\atlcrime.csv') #reading csv file
#df['count'] = 1
#df['date'] = pd.to_datetime(df['date'])
#new_df = df.groupby(df['date'].dt.year).count()['count'].sort_values(ascending=False)
#new_df.to_csv('total_crimes.csv')

# Most common crimes pie Chart

#df = pd.read_csv('data\\atlcrime.csv') #reading csv file
#df['count'] = 1
#new_df = df.groupby(['crime']).count()['count'].sort_values(ascending=False)
#new_df.to_csv('most_common_crimes.csv')


'''
Global variables needed for application.
'''

#Used for combo box on each des.
options = [
    "Highest crime areas",
    "Total crimes per year",
    "Most common crimes"
]

'''
Global Functions
'''

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


'''
Create GUI and plots.
'''

def login():
    #Testing login
    #rory
    #Rorukz123


    #getting form data
    uname=username.get()
    pwd=password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        messagebox.showinfo('Empty fields', 'Fields cannot be empty')
    else:
      #open database
      conn = sqlite3.connect('users.db')
      #select query
      cursor = conn.execute('SELECT * from Users where USERNAME="%s" and PASSWORD="%s"'%(uname,pwd))
      #fetch data 
      if cursor.fetchone():
       messagebox.showinfo('Login success', 'Login sucess')
       root.deiconify()
       login_screen.destroy()
       highest_crime_areas()
      else:
       messagebox.showinfo('Wrong credentials', 'Incorrect username or password.')


def loginScreen():
    root.withdraw()
    global login_screen
    login_screen = tk.Toplevel()
    login_screen.geometry("350x250+100+100")
    login_screen.lift(root)

    global username
    global password
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Label(login_screen, width='300', text='Login Form').pack()
    tk.Label(login_screen, text='Username: ').place(x=20,y=40)
    tk.Entry(login_screen, textvariable=username).place(x=120,y=42) #Adding textvariable so i can grab the data in login function
    tk.Label(login_screen, text='Password: ').place(x=20,y=80)
    tk.Entry(login_screen, textvariable=password, show='*').place(x=120, y=82) #Making password input display as * to imporve security. Adding textvariable so i can grab the data for login function
    tk.Button(login_screen, text="Login", width=10, height=1, command=login, bg="#0E6655",fg="white",font=("Arial",12,"bold")).place(x=125,y=170)

    login_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.mainloop()

def most_common_crimes(): #not using code comments for this function as functionality has been explained below. Have added comments to areas that contain different code.
    data_frame = pd.read_csv('plot_data\\most_common_crimes.csv')
    pie_data = data_frame['count'].iloc[0:6].sort_values(ascending=False)
    label_data = data_frame['crime'].iloc[0:6]

    def data_input_func():
        data_input.delete(0, END)

    def save_file():
        file = filedialog.asksaveasfilename(filetypes=[("CSV Files", ".csv")], defaultextension=".csv")
        if file:
            data_frame.to_csv(file, index=False)
            messagebox.showinfo("CSV saved", "CSV file saved")

    selected_option = tk.StringVar() 
    selected_option.set(options[2])

    def check_option(event):
        if(selected_option.get() == "Highest crime areas"):
            most_common_crimes_window.destroy()
            root.deiconify()
        if(selected_option.get() == "Total crimes per year"):
            total_crimes()
            most_common_crimes_window.destroy()

    most_common_crimes_window = tk.Toplevel()
    most_common_crimes_window.title("Data Analysis Program")
    most_common_crimes_window.geometry("850x700+100+100")
    heading = tk.Label(most_common_crimes_window, text="Most common crimes in Atlanta")
    heading.grid(row=0, column=0)
    frame_charts_lt = tk.Frame(most_common_crimes_window)
    frame_charts_lt.grid(row=1, column=0)
    input_data_label = tk.Label(most_common_crimes_window, text="Enter additional data specifications here")
    input_data_label.grid(row=2, column=0)
    drop_down = tk.OptionMenu(most_common_crimes_window, selected_option, *options, command=check_option)
    drop_down.grid(row=0, column=2, pady=20)
    data_input = tk.Entry(most_common_crimes_window, width=15)
    data_input.grid(row=3, column=0, ipady=30, ipadx=270)
    download_data = tk.Button(most_common_crimes_window, text="Download", command=save_file)
    download_data.grid(row=1, column=2)
    data_input_btn = tk.Button(most_common_crimes_window, text='Submit', command=data_input_func)
    data_input_btn.grid(row=3, column=1)
    quit_btn = tk.Button(most_common_crimes_window, text='Exit', command=on_closing, height=1, width=12)
    quit_btn.grid(row=2, column=2)

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(pie_data, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
    ax.legend(label_data, title="Crimes", loc="upper left", bbox_to_anchor=(0.9, 1.00), prop={'size': 7}) # Changing the size of legend so it fits in the canvas widget
    chart = FigureCanvasTkAgg(fig, frame_charts_lt)
    chart.get_tk_widget().grid(row=1, column=0)

    most_common_crimes_window.protocol("WM_DELETE_WINDOW", on_closing)


def total_crimes():
    data_frame = pd.read_csv('plot_data\\total_crimes.csv') #Reading csv file
    yData = data_frame['date'].iloc[0:8] #Splitting each column into seperate variables to be used with the bar graph.
    xData = data_frame['count'].sort_values(ascending=False).iloc[0:8] #Selecting only 0-8 entries as the final entry (2017) does not have a full year of entries.

    def data_input_func():
        data_input.delete(0, END)

    def save_file():
        file = filedialog.asksaveasfilename(filetypes=[("CSV Files", ".csv")], defaultextension=".csv")
        if file:
            data_frame.to_csv(file, index=False)
            messagebox.showinfo("CSV saved", "CSV file saved")

    selected_option = tk.StringVar() # Setting the state of drop_down menu to the first item.
    selected_option.set(options[1])
    
    def check_option(event): #if/else statement to display window depending on combobox selection
        if(selected_option.get() == "Highest crime areas"):
            total_crimes_window.destroy() #Destroys current window
            root.deiconify() #and unhides root window
        if(selected_option.get() == "Most common crimes"):
            total_crimes_window.destroy()
            most_common_crimes()

    total_crimes_window = tk.Toplevel() #creating top level instance of tkinter as you can only have one root window
    total_crimes_window.title("Data Anlysis Program") #Setting the title
    total_crimes_window.geometry("850x700+100+100") #Setting the size of the gui
    heading = tk.Label(total_crimes_window, text="Total amount of crimes per year in Atlanta") #Creating a heading so the user knows which window they're on
    heading.grid(row=0, column=0) #Using grid() instead of pack() so i can adjust where the widgets sit on the page.
    input_data_label = tk.Label(total_crimes_window, text="Enter additional data specifications here")
    input_data_label.grid(row=2, column=0)
    frameChartsLT = tk.Frame(total_crimes_window) #Creating a frame from tkinter so I can add the plot onto it
    frameChartsLT.grid(row=1, column=0) 
    drop_down = tk.OptionMenu(total_crimes_window, selected_option, *options, command=check_option) #Creating a combobox from tkinter, adding it to my TopLevel variable, adding options array and selected option Tkinter widget, as well as adding selected function.
    drop_down.grid(row=0, column=2, pady=20)
    data_input = tk.Entry(total_crimes_window, width=15)
    data_input.grid(row=3, column=0, ipady=30, ipadx=270)
    download_data = tk.Button(total_crimes_window, text="Download", command=save_file)
    download_data.grid(row=1, column=2)
    data_input_btn = tk.Button(total_crimes_window, text='Submit', command=data_input_func)
    data_input_btn.grid(row=3, column=1)
    quit_btn = tk.Button(total_crimes_window, text='Exit', command=on_closing, height=1, width=12) #Creating an exit button
    quit_btn.grid(row=2, column=2)

    fig = Figure() #Creating new figure from matplotlib 
    ax = fig.add_subplot(111) #Adding an axes to Figure 
    ax.bar(yData, xData) #Creating a bar graph and adding the two columns of data from the edited csv
    ax.set_xticks(yData) #Allowing the graph to display all years instead of skipping some.
    chart = FigureCanvasTkAgg(fig, frameChartsLT) #Adding the Figure and plot together using the FigureCanvasTkAgg interface
    chart.get_tk_widget().grid(row=1, column=0)
    
    total_crimes_window.protocol("WM_DELETE_WINDOW", on_closing)


#intializing root for first window, creating it out of function to make it global so i can deiconify it on my other pages.
root = tk.Tk() 
root.title("Data Anlysis Program")
root.geometry("850x700+100+100") # Setting display size (Width x Height) and displaying the window in specific place to increase immersion, important to keep smaller screens in mind as im coding this on a pc monitor.

def highest_crime_areas():
    data_frame = pd.read_csv('plot_data\\highest_crime_areas.csv') #reading csv file
    pie_data = data_frame['count'].iloc[0:5].sort_values(ascending=False) # getting count column as i need it for the plot
    label_data = data_frame['neighborhood'].iloc[0:5] # getting the neighbourhoods for the label aspect of the plot.

    def data_input_func():
        data_input.delete(0, END)

    def save_file():
        file = filedialog.asksaveasfilename(filetypes=[("CSV Files", ".csv")], defaultextension=".csv")
        if file:
            data_frame.to_csv(file, index=False)
            messagebox.showinfo("CSV saved", "CSV file saved")

    selected_option = tk.StringVar() # Setting the state of drop-down menu to the first item.
    selected_option.set(options[0])
    
    def check_option(event):
        if(selected_option.get() == "Total crimes per year"):
            total_crimes()
            root.withdraw()
        if(selected_option.get() == "Most common crimes"):
            most_common_crimes()
            root.withdraw()

    heading = tk.Label(root, text="Highest Crime Areas in Atlanta")
    heading.grid(row=0, column=0)
    input_data_label = tk.Label(root, text="Enter additional data specifications here")
    input_data_label.grid(row=2, column=0)
    frame_charts_lt = tk.Frame(root)
    frame_charts_lt.grid(row=1, column=0)
    drop_down = tk.OptionMenu(root, selected_option, *options, command=check_option)
    drop_down.grid(row=0, column=2, pady=20)
    data_input = tk.Entry(root, width=15)
    data_input.grid(row=3, column=0, ipady=30, ipadx=270)
    download_data = tk.Button(root, text="Download", command=save_file)
    download_data.grid(row=1, column=2)
    data_input_btn = tk.Button(root, text='Submit', command=data_input_func)
    data_input_btn.grid(row=3, column=1)
    quit_btn = tk.Button(root, text='Exit', command=on_closing, height=1, width=12)
    quit_btn.grid(row=2, column=2)

# Creating figure and adding pie plot to it.
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(pie_data, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
    ax.legend(label_data, title="Neighborhoods", loc="upper left", bbox_to_anchor=(0.9, 1.05))
    chart = FigureCanvasTkAgg(fig, frame_charts_lt)
    chart.get_tk_widget().grid(row=1, column=0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    loginScreen()
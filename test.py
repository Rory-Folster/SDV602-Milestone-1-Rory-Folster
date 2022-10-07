import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
from tkinter import Canvas, messagebox

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
       login_screen.destroy()
       highest_crime_areas()
      else:
       messagebox.showinfo('Wrong credentials', 'Incorrect username or password.')
       login_screen.lift(root)

def register():
    uname=username.get()
    pwd=password.get()
    #applying empty validation
    if uname=='' or pwd=='':
        messagebox.showinfo('Empty fields', 'Fields cannot be empty')
    else:
      #open database
      conn = sqlite3.connect('users.db')
      #select query
      conn.execute('INSERT INTO Users(username, password) VALUES("%s", "%s")'%(uname,pwd))
      #fetch data
      conn.commit()
      messagebox.showinfo('Account created', 'Account created')
      conn.close()

def loginScreen():
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
    tk.Button(login_screen, text="Register", width=10, height=1, command=register, bg="#0E6655",fg="white",font=("Arial",12,"bold")).place(x=125,y=200)

    login_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.mainloop()

root = tk.Tk() 
root.title("Data Anlysis Program")
root.geometry("800x600+100+100") # Setting display size (Width x Height) and displaying the window in specific place to increase immersion, important to keep smaller screens in mind as im coding this on a pc monitor.

def highest_crime_areas():
    #highest crime areas
    data_frame = pd.read_csv('plot_data\\highest_crime_areas.csv') #reading csv file
    pie_data = data_frame['count'].iloc[0:5].sort_values(ascending=False) # getting count column as i need it for the plot
    label_data = data_frame['neighborhood'].iloc[0:5] # getting the neighbourhoods for the label aspect of the plot.

    #total crimes
    data_frame1 = pd.read_csv('plot_data\\total_crimes.csv') #Reading csv file
    yData = data_frame1['date'].iloc[0:8] #Splitting each column into seperate variables to be used with the bar graph.
    xData = data_frame1['count'].sort_values(ascending=False).iloc[0:8] #Selecting only 0-8 entries as the final entry (2017) does not have a full year of entries.

    #most common crimes
    data_frame2 = pd.read_csv('plot_data\\most_common_crimes.csv')
    common_crimes_pie_data = data_frame2['count'].iloc[0:6].sort_values(ascending=False)
    common_crimes_label_data = data_frame2['crime'].iloc[0:6]


    headingVar = tk.StringVar()
    selected_option = tk.StringVar() # Setting the state of drop-down menu to the first item.
    selected_option.set(options[0])
    
    def check_option(event):
        if(selected_option.get() == "Highest crime areas"):
            heading.config(text="Highest crime areas")
            fig = Figure()
            ax = fig.add_subplot(111)
            ax.pie(pie_data, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
            ax.legend(label_data, title="Neighborhoods", loc="upper left", bbox_to_anchor=(0.9, 1.05))
            pie = FigureCanvasTkAgg(fig, frame_charts_lt)
            chart = pie.get_tk_widget()
            chart.grid(row=1, column=0)
        if(selected_option.get() == "Total crimes per year"):
            heading.config(text="Total crimes per year")
            newFig = Figure()
            barAx = newFig.add_subplot()
            barAx.bar(yData, xData)
            barAx.set_xticks(yData)
            bar = FigureCanvasTkAgg(newFig, frame_charts_lt)
            barChart = bar.get_tk_widget()
            barChart.grid(row=1, column=0)
        if(selected_option.get() == "Most common crimes"):
            heading.config(text="Most common crimes")
            fig = Figure()
            ax = fig.add_subplot(111)
            ax.pie(common_crimes_pie_data, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
            ax.legend(common_crimes_label_data, title="Neighborhoods", loc="upper left", bbox_to_anchor=(0.9, 1.05), prop={'size': 7})
            pie = FigureCanvasTkAgg(fig, frame_charts_lt)
            chart = pie.get_tk_widget()
            chart.grid(row=1, column=0)
    
    heading = tk.Label(root, text="Highest crime areas")
    heading.grid(row=0, column=0)
    frame_charts_lt = tk.Frame(root)
    frame_charts_lt.grid(row=1, column=0)
    drop_down = tk.OptionMenu(root, selected_option, *options, command=check_option)
    drop_down.grid(row=0, column=1, pady=20)
    data_input = tk.Entry(root)
    data_input.grid(row=2, column=0)
    quit_btn = tk.Button(root, text='Exit', command=on_closing, height=1, width=12)
    quit_btn.grid(row=2, column=1)

# Creating figure and adding pie plot to it.
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(pie_data, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
    ax.legend(label_data, title="Neighborhoods", loc="upper left", bbox_to_anchor=(0.9, 1.05))
    pie = FigureCanvasTkAgg(fig, frame_charts_lt)
    chart = pie.get_tk_widget()
    chart.grid(row=1, column=0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    loginScreen()

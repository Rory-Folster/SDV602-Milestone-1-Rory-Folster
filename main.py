from cProfile import label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#https://data.world/bryantahb/crime-in-atlanta-2009-2017 - Original CSV location.

'''
Functions for creating seperate csv's for the different chart data we need. Kept for later revision if needed.
'''
# Pie chart csv

#df = pd.read_csv('data\\atlcrime.csv') #reading csv file
#df['count'] = 1
#new_df = df.groupby(['crime', 'neighborhood']).count()['count'].sort_values(ascending=False)
#new_df.to_csv('pieData.csv')

# Bar chart csv

#df = pd.read_csv('data\\atlcrime.csv') #reading csv file
#df['count'] = 1
#df['date'] = pd.to_datetime(df['date'])
#new_df = df.groupby(df['date'].dt.year).count()['count'].sort_values(ascending=False)
#new_df.to_csv('barData.csv')

# 2 Pie Chart

#df = pd.read_csv('data\\atlcrime.csv') #reading csv file
#df['count'] = 1
#new_df = df.groupby(['crime']).count()['count'].sort_values(ascending=False)
#new_df.to_csv('mostCommonCrimes.csv')


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
Create GUI and plots.
'''

def most_common_crimes(): #not using code comments for this function as functionality has been explained below. Have added comments to areas that contain different code.
    data_frame = pd.read_csv('plot_data\\mostCommonCrimes.csv')
    pie_data = data_frame['count'].iloc[0:6].sort_values(ascending=False)
    label_data = data_frame['crime'].iloc[0:6]

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
    most_common_crimes_window.geometry("800x600+300+300")
    heading = tk.Label(most_common_crimes_window, text="Most common crimes in Atlanta")
    heading.grid(row=0, column=0)
    frame_charts_lt = tk.Frame(most_common_crimes_window)
    frame_charts_lt.grid(row=1, column=0) 
    drop_down = tk.OptionMenu(most_common_crimes_window, selected_option, *options, command=check_option)
    drop_down.grid(row=0, column=2, pady=20)
    quit_btn = tk.Button(most_common_crimes_window, text='Exit', command=root.destroy, height=1, width=12)
    quit_btn.grid(row=2, column=2)

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(pie_data, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
    ax.legend(label_data, title="Crimes", loc="upper left", bbox_to_anchor=(0.9, 1.00), prop={'size': 7}) # Changing the size of legend so it fits in the canvas widget
    chart = FigureCanvasTkAgg(fig, frame_charts_lt)
    chart.get_tk_widget().grid(row=1, column=0)

def total_crimes():
    data_frame = pd.read_csv('plot_data\\barData.csv') #Reading csv file
    yData = data_frame['date'].iloc[0:8] #Splitting each column into seperate variables to be used with the bar graph.
    xData = data_frame['count'].sort_values(ascending=False).iloc[0:8] #Selecting only 0-8 entries as the final entry (2017) does not have a full year of entries.

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
    total_crimes_window.geometry("800x600+300+300") #Setting the size of the gui
    heading = tk.Label(total_crimes_window, text="Total amount of crimes per year in Atlanta") #Creating a heading so the user knows which window they're on
    heading.grid(row=0, column=0) #Using instead of pack() so i can adjust where the widgets sit on the page.
    frameChartsLT = tk.Frame(total_crimes_window) #Creating a frame from tkinter so I can add the plot onto it
    frameChartsLT.grid(row=1, column=0) 
    drop_down = tk.OptionMenu(total_crimes_window, selected_option, *options, command=check_option) #Creating a combobox from tkinter
    drop_down.grid(row=0, column=2, pady=20)
    quit_btn = tk.Button(total_crimes_window, text='Exit', command=root.destroy, height=1, width=12) #Creating an exit button
    quit_btn.grid(row=2, column=2)

    fig = Figure() #Creating new figure from matplotlib 
    ax = fig.add_subplot(111) #Adding an axes to Figure 
    ax.bar(yData, xData) #Creating a bar graph and adding the two columns of data from the edited csv
    ax.set_xticks(yData) #Allowing the graph to display all years instead of skipping some.
    chart = FigureCanvasTkAgg(fig, frameChartsLT) #Adding the Figure and plot together using the FigureCanvasTkAgg interface
    chart.get_tk_widget().grid(row=1, column=0)


#intializing root for first window, creating it out of function to make it global so i can deiconify it on my other pages.
root = tk.Tk() 
root.title("Data Anlysis Program")
root.geometry("800x600+300+300")

def highest_crime_areas():
    data_frame = pd.read_csv('plot_data\\pieData.csv') #reading csv file
    pie_data = data_frame['count'].iloc[0:5].sort_values(ascending=False) # getting count column as i need it for the plot
    label_data = data_frame['neighborhood'].iloc[0:5] # getting the neighbourhoods for the label aspect of the plot.

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
    frame_charts_lt = tk.Frame(root)
    frame_charts_lt.grid(row=1, column=0)
    drop_down = tk.OptionMenu(root, selected_option, *options, command=check_option)
    drop_down.grid(row=0, column=2, pady=20)
    quit_btn = tk.Button(root, text='Exit', command=root.destroy, height=1, width=12)
    quit_btn.grid(row=2, column=2)

# Creating figure and adding pie plot to it.
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(pie_data, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
    ax.legend(label_data, title="Neighborhoods", loc="upper left", bbox_to_anchor=(0.9, 1.05))
    chart = FigureCanvasTkAgg(fig, frame_charts_lt)
    chart.get_tk_widget().grid(row=1, column=0)

    root.mainloop()

if __name__ == '__main__':
    highest_crime_areas()
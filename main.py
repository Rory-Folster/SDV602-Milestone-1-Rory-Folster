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

def mostCommonCrimes():
    dataFrame = pd.read_csv('plot_data\\mostCommonCrimes.csv')
    pieData = dataFrame['count'].iloc[0:6].sort_values(ascending=False)
    labelData = dataFrame['crime'].iloc[0:6]

    clicked = tk.StringVar() 
    clicked.set(options[2])

    def checkSelected(event):
        if(clicked.get() == "Highest crime areas"):
            win3.destroy()
            root.deiconify()
        if(clicked.get() == "Total crimes per year"):
            totalCrimes()
            win3.destroy()

    win3 = tk.Toplevel()
    win3.title("Data Analysis Program")
    win3.geometry("800x600+300+300")
    heading = tk.Label(win3, text="Most common crimes in Atlanta")
    heading.grid(row=0, column=0)
    frameChartsLT = tk.Frame(win3)
    frameChartsLT.grid(row=1, column=0) 
    dropDown = tk.OptionMenu(win3, clicked, *options, command=checkSelected)
    dropDown.grid(row=0, column=2, pady=20)
    quitBtn = tk.Button(win3, text='Exit', command=root.destroy, height=1, width=12)
    quitBtn.grid(row=2, column=2)

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(pieData, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
    ax.legend(labelData, title="Crimes", loc="upper left", bbox_to_anchor=(0.9, 1.00), prop={'size': 7}) # Changing the size of legend so it fits in the canvas widget
    chart = FigureCanvasTkAgg(fig, frameChartsLT)
    chart.get_tk_widget().grid(row=1, column=0)

def totalCrimes():
    dataFrame = pd.read_csv('plot_data\\barData.csv') #Reading csv file
    yData = dataFrame['date'].iloc[0:8] #Splitting each column into seperate variables to be used with the bar graph.
    xData = dataFrame['count'].sort_values(ascending=False).iloc[0:8] #Selecting only 0-8 entries as the final entry (2017) does not have a full year of entries.

    clicked = tk.StringVar() # Setting the state of dropdown menu to the first item.
    clicked.set(options[1])
    
    def checkSelected(event): #if/else statement to display window depending on combobox selection
        if(clicked.get() == "Highest crime areas"):
            win2.destroy() #Destroys current window
            root.deiconify() #and unhides root window
        if(clicked.get() == "Most common crimes"):
            win2.destroy()
            mostCommonCrimes()

    win2 = tk.Toplevel() #creating top level instance of tkinter as you can only have one root window
    win2.title("Data Anlysis Program") #Setting the title
    win2.geometry("800x600+300+300") #Setting the size of the gui
    heading = tk.Label(win2, text="Total amount of crimes per year in Atlanta") #Creating a heading so the user knows which window they're on
    heading.grid(row=0, column=0) #Using instead of pack() so i can adjust where the widgets sit on the page.
    frameChartsLT = tk.Frame(win2) #Creating a frame from tkinter so I can add the plot onto it
    frameChartsLT.grid(row=1, column=0) 
    dropDown = tk.OptionMenu(win2, clicked, *options, command=checkSelected) #Creating a combobox from tkinter
    dropDown.grid(row=0, column=2, pady=20)
    quitBtn = tk.Button(win2, text='Exit', command=root.destroy, height=1, width=12) #Creating an exit button
    quitBtn.grid(row=2, column=2)

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

def highestCrimeAreas():
    dataFrame = pd.read_csv('plot_data\\pieData.csv') #reading csv file
    pieData = dataFrame['count'].iloc[0:5].sort_values(ascending=False) # getting count column as i need it for the plot
    labelData = dataFrame['neighborhood'].iloc[0:5] # getting the neighbourhoods for the label aspect of the plot.

    clicked = tk.StringVar() # Setting the state of dropdown menu to the first item.
    clicked.set(options[0])
    
    def checkSelected(event):
        if(clicked.get() == "Total crimes per year"):
            totalCrimes()
            root.withdraw()
        if(clicked.get() == "Most common crimes"):
            mostCommonCrimes()
            root.withdraw()

    heading = tk.Label(root, text="Highest Crime Areas in Atlanta")
    heading.grid(row=0, column=0)
    frameChartsLT = tk.Frame(root)
    frameChartsLT.grid(row=1, column=0)
    dropDown = tk.OptionMenu(root, clicked, *options, command=checkSelected)
    dropDown.grid(row=0, column=2, pady=20)
    quitBtn = tk.Button(root, text='Exit', command=root.destroy, height=1, width=12)
    quitBtn.grid(row=2, column=2)

# Creating figure and adding pie plot to it.
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie(pieData, radius=1, autopct='%0.2f%%', shadow=True, startangle=140, counterclock=False)
    ax.legend(labelData, title="Neighborhoods", loc="upper left", bbox_to_anchor=(0.9, 1.05))
    chart = FigureCanvasTkAgg(fig, frameChartsLT)
    chart.get_tk_widget().grid(row=1, column=0)

    root.mainloop()

if __name__ == '__main__':
    highestCrimeAreas()
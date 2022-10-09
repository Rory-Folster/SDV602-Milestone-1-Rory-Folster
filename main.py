"""
Python application created for data analysists to read and interact with 3 pre-set DES.
The users will be able to sign-in, create an account, upload CSV files to be plotted
and chat between each other.
"""

from tkinter import END, ACTIVE, DISABLED, filedialog, messagebox
import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Used for combo box on each des.
options = ["Highest crime areas", "Total crimes per year", "Most common crimes"]


def on_closing():
    """
    Function to ask user if they want to quit, instead of just closing.
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def most_common_crimes():
    """
    Most Common Crimes DES.
    """
    data_frame = pd.read_csv("plot_data\\most_common_crimes.csv")
    pie_data = data_frame["count"].iloc[0:6].sort_values(ascending=False)
    label_data = data_frame["crime"].iloc[0:6]

    def data_input_func():
        data_input.delete(0, END)

    def reset_view():
        most_common_crimes_window.destroy()
        most_common_crimes()

    def upload_file():
        file = filedialog.askopenfilename(
            filetypes=[("CSV Files", ".csv")], defaultextension=".csv"
        )
        if file:
            try:
                most_common_crimes_window.geometry("1500x700+100+100")
                imported_file = pd.read_csv(file)
                new_pie_data = (
                    imported_file["count"].iloc[0:6].sort_values(ascending=False)
                )
                new_label_data = imported_file["crime"].iloc[0:6]

                new_fig = Figure()
                new_ax = new_fig.add_subplot(111)
                new_ax.pie(
                    new_pie_data,
                    radius=1,
                    autopct="%0.2f%%",
                    shadow=True,
                    startangle=140,
                    counterclock=False,
                )
                new_ax.legend(
                    new_label_data,
                    title="imported data",
                    loc="upper left",
                    bbox_to_anchor=(0.9, 1.05),
                    prop={"size": 7},
                )
                reset_btn.config(state=ACTIVE)
                new_frame_charts_lt = tk.Frame(most_common_crimes_window)
                new_frame_charts_lt.grid(row=1, column=3)
                new_pie = FigureCanvasTkAgg(new_fig, new_frame_charts_lt)
                new_chart = new_pie.get_tk_widget()
                new_chart.grid(row=1, column=3)
            except:
                most_common_crimes_window.geometry("850x700+100+100")
                messagebox.showinfo(
                    "CSV File can not be read.", "CSV File can not be read."
                )

    selected_option = tk.StringVar()
    selected_option.set(options[2])

    def check_option(event):
        if selected_option.get() == "Highest crime areas":
            most_common_crimes_window.destroy()
            root.deiconify()
        if selected_option.get() == "Total crimes per year":
            total_crimes()
            most_common_crimes_window.destroy()

    most_common_crimes_window = tk.Toplevel()
    most_common_crimes_window.title("Data Analysis Program")
    most_common_crimes_window.geometry("850x700+100+100")
    heading = tk.Label(most_common_crimes_window, text="Most common crimes in Atlanta")
    heading.grid(row=0, column=0)
    frame_charts_lt = tk.Frame(most_common_crimes_window)
    frame_charts_lt.grid(row=1, column=0)
    input_data_label = tk.Label(
        most_common_crimes_window, text="Enter additional data specifications here"
    )
    input_data_label.grid(row=2, column=0)
    drop_down = tk.OptionMenu(
        most_common_crimes_window, selected_option, *options, command=check_option
    )
    drop_down.grid(row=0, column=2, pady=20)
    data_input = tk.Entry(most_common_crimes_window, width=15)
    data_input.grid(row=3, column=0, ipady=30, ipadx=270)
    download_data = tk.Button(
        most_common_crimes_window, text="Upload File", command=upload_file
    )
    download_data.grid(row=1, column=2)
    data_input_btn = tk.Button(
        most_common_crimes_window, text="Submit", command=data_input_func
    )
    data_input_btn.grid(row=3, column=1)
    reset_btn = tk.Button(
        most_common_crimes_window,
        text="Remove import",
        command=reset_view,
        state=DISABLED,
    )
    reset_btn.grid(row=2, column=2)
    quit_btn = tk.Button(
        most_common_crimes_window, text="Exit", command=on_closing, height=1, width=12
    )
    quit_btn.grid(row=3, column=2)

    fig = Figure()
    plot_axes = fig.add_subplot(111)
    plot_axes.pie(
        pie_data,
        radius=1,
        autopct="%0.2f%%",
        shadow=True,
        startangle=140,
        counterclock=False,
    )
    plot_axes.legend(
        label_data,
        title="Crimes",
        loc="upper left",
        bbox_to_anchor=(0.9, 1.00),
        prop={"size": 7},
    )
    chart = FigureCanvasTkAgg(fig, frame_charts_lt)
    toolbar = NavigationToolbar2Tk(chart)
    toolbar.grid(row=2, column=0)
    chart.get_tk_widget().grid(row=1, column=0)

    most_common_crimes_window.protocol("WM_DELETE_WINDOW", on_closing)


def total_crimes():

    """
    Total Crimes DES.
    """

    data_frame = pd.read_csv("plot_data\\total_crimes.csv")  # Reading csv file
    y_data = data_frame["date"].iloc[
        0:8
    ]  # Splitting each column into seperate variables to be used with the bar graph.
    x_data = (
        data_frame["count"].sort_values(ascending=False).iloc[0:8]
    )  # Selecting only 0-8 entries as the final entry (2017) does not have a full year of entries.

    def reset_view():
        total_crimes_window.destroy()
        total_crimes()

    def data_input_func():  # placeholder function until I start making the data filtering.
        data_input.delete(0, END)

    def upload_file():  # This function has been explained below.
        file = filedialog.askopenfilename(
            filetypes=[("CSV Files", ".csv")], defaultextension=".csv"
        )
        if file:
            total_crimes_window.geometry("1500x700+100+100")
            imported_file = pd.read_csv(file)
            new_y_data = (
                imported_file["neighborhood"].iloc[0:8].sort_values(ascending=False)
            )
            new_x_data = imported_file["count"].iloc[0:8]
            reset_btn.config(state=ACTIVE)
            new_fig = Figure()
            new_ax = new_fig.add_subplot()
            new_ax.bar(new_y_data, new_x_data)
            new_ax.set_xticks(new_y_data)
            new_frame_charts_lt = tk.Frame(total_crimes_window)
            new_frame_charts_lt.grid(row=1, column=3)
            new_bar = FigureCanvasTkAgg(new_fig, new_frame_charts_lt)
            new_chart = new_bar.get_tk_widget()
            new_chart.grid(row=1, column=3)
        else:
            total_crimes_window.geometry("850x700+100+100")
            messagebox.showinfo(
                "CSV File can not be read.", "CSV File can not be read."
            )

    selected_option = (
        tk.StringVar()
    )  # Setting the state of drop_down menu to the first item.
    selected_option.set(options[1])

    def check_option(
        event,
    ):  # if/else statement to display window depending on combobox selection
        if selected_option.get() == "Highest crime areas":
            total_crimes_window.destroy()  # Destroys current window
            root.deiconify()  # and unhides root window
        if selected_option.get() == "Most common crimes":
            total_crimes_window.destroy()
            most_common_crimes()

    total_crimes_window = (
        tk.Toplevel()
    )  # creating top level instance of tkinter as you can only have one root window
    total_crimes_window.title("Data Anlysis Program")  # Setting the title
    total_crimes_window.geometry("850x700+100+100")  # Setting the size of the gui
    heading = tk.Label(
        total_crimes_window, text="Total amount of crimes per year in Atlanta"
    )  # Creating a heading so the user knows which window they're on
    heading.grid(
        row=0, column=0
    )  # Using grid() instead of pack() so i can adjust where the widgets sit on the page.
    input_data_label = tk.Label(
        total_crimes_window, text="Enter additional data specifications here"
    )
    input_data_label.grid(row=2, column=0)
    frame_charts_lt = tk.Frame(
        total_crimes_window
    )  # Creating a frame from tkinter so I can add the plot onto it
    frame_charts_lt.grid(row=1, column=0)
    drop_down = tk.OptionMenu(
        total_crimes_window, selected_option, *options, command=check_option
    )  # Creating a combobox from tkinter, adding it to my TopLevel variable,
    # adding options array and selected option Tkinter widget,
    # as well as adding selected function.
    drop_down.grid(row=0, column=2, pady=20)
    data_input = tk.Entry(total_crimes_window, width=15)
    data_input.grid(row=3, column=0, ipady=30, ipadx=270)
    data_input_btn = tk.Button(
        total_crimes_window, text="Submit", command=data_input_func
    )
    data_input_btn.grid(row=3, column=1)
    download_data = tk.Button(
        total_crimes_window, text="Upload File", command=upload_file
    )
    reset_btn = tk.Button(
        total_crimes_window,
        text="Remove import",
        command=reset_view,
        state=DISABLED,
    )
    reset_btn.grid(row=2, column=2)
    download_data.grid(row=1, column=2)
    quit_btn = tk.Button(
        total_crimes_window, text="Exit", command=on_closing, height=1, width=12
    )  # Creating an exit button
    quit_btn.grid(row=3, column=2)

    fig = Figure()  # Creating new figure from matplotlib
    plot_axes = fig.add_subplot(111)  # Adding an axes to Figure
    plot_axes.bar(
        y_data, x_data
    )  # Creating a bar graph and adding the two columns of data from the edited csv
    plot_axes.set_xticks(
        y_data
    )  # Allowing the graph to display all years instead of skipping some.
    chart = FigureCanvasTkAgg(
        fig, frame_charts_lt
    )  # Adding the Figure and plot together using the FigureCanvasTkAgg interface
    toolbar = NavigationToolbar2Tk(chart)
    toolbar.grid(row=2, column=0)
    chart.get_tk_widget().grid(row=1, column=0)

    total_crimes_window.protocol("WM_DELETE_WINDOW", on_closing)


root = tk.Tk()
root.title("Data Anlysis Program")
root.geometry(
    "850x700+100+100"
)  # Setting display size (Width x Height) and displaying the window in specific place,
# important to keep smaller screens in mind as im coding this on a pc monitor.


def highest_crime_areas():

    """
    Highest crime areas DES.
    """

    data_frame = pd.read_csv("plot_data\\highest_crime_areas.csv")  # reading csv file
    pie_data = (
        data_frame["count"].iloc[0:5].sort_values(ascending=False)
    )  # getting count column as i need it for the plot
    label_data = data_frame["neighborhood"].iloc[
        0:5
    ]  # getting the neighbourhoods for the label aspect of the plot.

    def data_input_func():
        data_input.delete(0, END)

    def upload_file():
        """
        Creating upload file function. This will involve using Tkinter's 'askopenfilename'
        to get the directory. Pandas will then be used to deconstruct the data and plot an
        additional MatPlotLib plot.
        """

        # this opens a window explorer that will allow a user to select a CSV file
        file = filedialog.askopenfilename(
            # Setting the required file to be a CSV file\
            # to help the user know which file is required.
            filetypes=[("CSV Files", ".csv")],
            defaultextension=".csv",
        )
        # If the user returns a directory, run the following code.
        if file:
            # Increase the size of the window to allow the new plot to fit.
            root.geometry("1500x700+100+100")
            # Adding the dataframe into a variable so i can deconstruct it
            imported_file = pd.read_csv(file)
            # Grabbing the first column
            new_pie_data = imported_file["count"].iloc[0:6].sort_values(ascending=False)
            # Grabbing the second column
            new_label_data = imported_file["crime"].iloc[0:6]

            # creating the new figure needed for the new plot
            new_fig = Figure()
            # Adding the pie sub-plot number, 111.
            new_ax = new_fig.add_subplot(111)
            # Adding the count column into the pie function.
            # Also changing the style so it fits and looks nice.
            new_ax.pie(
                new_pie_data,
                radius=1,
                autopct="%0.2f%%",
                shadow=True,
                startangle=140,
                counterclock=False,
            )
            # Adding a legend so the user knows what the data represents.
            new_ax.legend(
                new_label_data,
                title="imported data",
                loc="upper left",
                bbox_to_anchor=(0.9, 1.05),
                # Changing the size of the legend so it fits in the Figure.
                prop={"size": 7},
            )
            # Allowing the reset view button to be used.
            reset_btn.config(state=ACTIVE)
            # creating global variable so that it can be removed as the
            # root window can not be closed and reopened without restarting the app.
            global NEW_FRAME_CHARTS_LT
            # creating new frame
            NEW_FRAME_CHARTS_LT = tk.Frame(root)
            NEW_FRAME_CHARTS_LT.grid(row=1, column=3)
            # adding the figure into the frame and placing the frame on the window.
            new_pie = FigureCanvasTkAgg(new_fig, NEW_FRAME_CHARTS_LT)
            new_chart = new_pie.get_tk_widget()
            new_chart.grid(row=1, column=3)

    def reset_view():
        NEW_FRAME_CHARTS_LT.destroy()  # destorys the current imported plot
        root.geometry(
            "850x700+100+100"
        )  # resets the window size back to the regular size.
        reset_btn.config(state=DISABLED)  # Disables the button once again.

    selected_option = (
        tk.StringVar()
    )  # Setting the state of drop-down menu to the first item.
    selected_option.set(options[0])

    def check_option(event):
        if selected_option.get() == "Total crimes per year":
            total_crimes()
            root.withdraw()
        if selected_option.get() == "Most common crimes":
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
    download_data = tk.Button(root, text="Upload File", command=upload_file)
    download_data.grid(row=1, column=2)
    data_input_btn = tk.Button(root, text="Submit", command=data_input_func)
    data_input_btn.grid(row=3, column=1)
    reset_btn = tk.Button(
        root,
        text="Remove import",
        command=reset_view,
        # Setting the state so that the button can only be pressed when a file is imported.
        state=DISABLED,
    )
    reset_btn.grid(row=2, column=2)
    quit_btn = tk.Button(root, text="Exit", command=on_closing, height=1, width=12)
    quit_btn.grid(row=3, column=2)

    # Creating figure and adding pie plot to it.
    fig = Figure()
    plot_axes = fig.add_subplot(111)
    plot_axes.pie(
        pie_data,
        radius=1,
        autopct="%0.2f%%",
        shadow=True,
        startangle=140,
        counterclock=False,
    )
    plot_axes.legend(
        label_data, title="Neighborhoods", loc="upper left", bbox_to_anchor=(0.9, 1.05)
    )
    chart = FigureCanvasTkAgg(fig, frame_charts_lt)
    toolbar = NavigationToolbar2Tk(chart)
    toolbar.grid(row=2, column=0)
    chart.get_tk_widget().grid(row=1, column=0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    highest_crime_areas()

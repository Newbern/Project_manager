import tkinter as tk
import ttkbootstrap as ttk
import json
from time import strftime

# Uploading data
with open("data.json", "r") as file:
    data = json.load(file)

# Creating Display
window = ttk.Window(themename="darkly")
window.wm_state("zoomed")
window.title("Project Manager")
font = "25"


# Updates Data
def update():
    # Getting today's date
    Time = strftime("%Y/%m/%d")
    for item in data:
        if item["State"] != "Complete":
            if Time > item["Date"]:
                item["State"] = "Late"
            elif Time < item["Date"]:
                item["State"] = "Due"
    # Updating
    with open("data.json", "w") as new_data:
        json.dump(data, new_data, indent=3)

# Main Menu
Main_Frame = tk.Frame(master=window)
def Main_Menu():
    # Sets up The configuration for the next Screen
    def Run():
        # Erasing
        Main_Frame.pack_forget()
        Search_Bar.delete(0, tk.END)
        Add_Frame.pack()

    # Add Button
    Button = tk.Button(master=Main_Frame, text="ADD", width=20, height=2, command=Run)
    Button.pack()

    # Place Holder for ListBox & Side Buttons
    Middle_Frame = tk.Frame(master=Main_Frame)
    Middle_Frame.pack()

    # Frame for the Bottom buttons to line up right
    Left_Middle_Frame = tk.Frame(master=Middle_Frame)
    Left_Middle_Frame.pack(side=tk.LEFT)

    # ListBox Frame
    List_Frame = tk.Frame(master=Left_Middle_Frame)
    List_Frame.pack()

    # Search Frame Setup
    def Search():
        # Search Bar
        global Search_Bar
        Search_Bar = tk.Entry(master=Search_Frame, font=("Comic Sans MS", 15))
        Search_Bar.pack(side=tk.LEFT)

        # Command
        def Run_Search():
            for item in data:
                if item["Name"].count(Search_Bar.get()) \
                        or item["Name"].lower().count(Search_Bar.get())\
                        or item["Name"].upper().count(Search_Bar.get())\
                        or item["Name"].capitalize().count(Search_Bar.get()):
                    ListBox.delete(0, tk.END)

                    # Rearranging date
                    year, *args = item["Date"].split("/")
                    date = "/".join((*args, year))
                    ListBox.insert(tk.END, (item["State"], date, item["Name"]))

        # Search Button
        Search_Button = tk.Button(master=Search_Frame, text="Search", command=Run_Search)
        Search_Button.pack(side=tk.RIGHT, padx=(5, 0))

    # Search Frame
    Search_Frame = tk.Frame(master=List_Frame)
    Search_Frame.pack(anchor="ne", pady=(5, 10))
    Search()

    # ListBox
    # Making it global so the other functions can access
    global ListBox
    ListBox = tk.Listbox(master=List_Frame, width=100, height=20, font=font)
    ListBox.pack(side=tk.LEFT)

    # ListBox Scroll bar
    Scroll = tk.Scrollbar(master=List_Frame, orient="vertical")
    Scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Scroll Bar config
    ListBox.configure(yscrollcommand=Scroll.set)
    Scroll.configure(command=ListBox.yview)

    # Loading in Fresh data
    refresh("All")

    # Lower Buttons setup
    def Lower_Buttons():
        # All Button
        All_Button = tk.Button(master=Buttons_Lower, text="All", width=20, height=8, command=lambda: refresh("All"))
        All_Button.grid(row=1, column=1, padx=50)

        # Due Button
        Due_Button = tk.Button(master=Buttons_Lower, text="Due", width=20, height=8, command=lambda: refresh("Due"))
        Due_Button.grid(row=1, column=2, padx=50)

        # Late Button
        Late_Button = tk.Button(master=Buttons_Lower, text="Late", width=20, height=8, command=lambda: refresh("Late"))
        Late_Button.grid(row=1, column=3, padx=50)

        # Complete Button
        Complete_Button = tk.Button(master=Buttons_Lower, text="Complete", width=20, height=8,
                                    command=lambda: refresh("Complete"))
        Complete_Button.grid(row=1, column=4, padx=50)

    # Side Button setup
    def Side_Buttons():
        def Run_Done():
            # Checking to see if there is input
            # Getting input from ListBox
            try:
                state, date, *name = ListBox.get(tk.ANCHOR).split()
                name = ' '.join(name)
            except:
                return

            # Rearranging date
            *args, year = date.split("/")
            date = "/".join((year, *args))

            # Finding the correct data structure
            for item in data:
                if item["State"] == state:
                    if item["Date"] == date:
                        if item["Name"] == name:
                            # Changing the State
                            if item["State"] == "Complete":
                                # Checking date to make the correct state
                                if date >= strftime("%Y/%m/%d"):
                                    item["State"] = "Due"
                                elif date < strftime("%Y/%m/%d"):
                                    item["State"] = "Late"
                            # Changing to complete
                            else:
                                item["State"] = "Complete"

                            # Updating Data
                            with open("data.json", "w") as new_data:
                                json.dump(data, new_data, indent=3)

            refresh("All")

        def Run_Delete():
            # Erase Main_Frame
            Main_Frame.pack_forget()

            # Create a Delete_Frame
            Delete_Frame = tk.Frame(master=window)
            Delete_Frame.pack()

            # Checking to see if there is input
            # Getting input from ListBox
            try:
                state, date, *Name = ListBox.get(tk.ANCHOR).split()
                Item = ListBox.get(tk.ANCHOR)
                name = " ".join(Name)
            except:
                Delete_Frame.pack_forget()
                refresh("All")
                Main_Frame.pack()
                return

            # Label
            tk.Label(master=Delete_Frame, text=f"Are you sure you want to delete this task?").pack()
            tk.Label(master=Delete_Frame, text=name, font=("Impact", font)).pack()
            tk.Label(master=Delete_Frame, text=state).pack()

            def Yes(delete):
                # Rearranging to find the correct Data
                # Separating the 3 item
                _state, _date, *_name = delete.split()

                # Fixing name if there is more than one word
                if len(_name) > 1:
                    _name = " ".join(_name)
                else:

                    _name = _name[0]
                # Fixing the date to format
                *args, year = _date.split("/")
                _date = "/".join((year, *args))

                # finding the correct data item
                for item in data:
                    if item["Date"] == _date:
                        if item["State"] == _state:
                            if item["Name"] == _name:
                                # Erasing data structure
                                data.remove(item)
                                with open("data.json", "w") as New_data:
                                    json.dump(data, New_data, indent=3)

                # Loading Main Screen
                Delete_Frame.pack_forget()
                refresh("All")
                Main_Frame.pack()

            def No():
                Delete_Frame.pack_forget()
                Main_Frame.pack()

            # Yes
            tk.Button(master=Delete_Frame,
                      text="Yes",
                      width=20,
                      height=5,
                      command=lambda: Yes(Item)
                      ).pack(side=tk.LEFT, padx=25, pady=25)

            # No
            tk.Button(master=Delete_Frame,
                      text="No",
                      width=20,
                      height=5,
                      command=No
                      ).pack(side=tk.RIGHT, padx=25)

        def Run_Edit():
            Edit_Button.pack_forget()
            # Rename Frame
            Rename_Frame = tk.Frame(master=Buttons_Side)
            Rename_Frame.pack(padx=(25, 0))

            # Rename Entry
            tk.Label(master=Rename_Frame, text="Name:").pack(pady=(10, 0))
            Rename_Entry = tk.Entry(master=Rename_Frame)
            Rename_Entry.pack()

            # ReDate Entry
            tk.Label(master=Rename_Frame, text="Date:").pack()
            ReDate_Entry = tk.Entry(master=Rename_Frame)
            ReDate_Entry.pack()

            # Renaming
            def Rename():
                # Resetting Buttons
                Rename_Frame.pack_forget()
                Edit_Button.pack(pady=10)

                # Checking to see if there is input
                # Getting input from ListBox
                try:
                    state, date, *name = ListBox.get(tk.ANCHOR).split()
                    name = ' '.join(name)
                except:
                    return

                # Rearranging date
                *args, year = date.split("/")
                date = "/".join((year, *args))

                # Finding the correct data structure
                for item in data:
                    if item["State"] == state:
                        if item["Date"] == date:
                            if item["Name"] == name:
                                # Checking for Entry input
                                # Name
                                if Rename_Entry.get() != "":
                                    item["Name"] = Rename_Entry.get()

                                # Date
                                if ReDate_Entry.get() != "":
                                    *args, year = ReDate_Entry.get().split("/")
                                    date = "/".join((year, *args))
                                    item["Date"] = date

                                # Saving Changed Name
                                with open("data.json", "w") as new_data:
                                    json.dump(data, new_data, indent=3)

                                update()
                                refresh("All")

            # Rename Button
            Rename_Button = tk.Button(master=Rename_Frame, text="Submit", command=Rename)
            Rename_Button.pack(side=tk.RIGHT)

        # Done Button
        Done_Button = tk.Button(master=Buttons_Side, text="Done", width=15, height=10, command=Run_Done)
        Done_Button.pack(padx=25, pady=50)

        # Delete Button
        Delete_Button = tk.Button(master=Buttons_Side, text="Delete", width=15, height=5, command=Run_Delete)
        Delete_Button.pack()

        # Edit Button
        Edit_Button = tk.Button(master=Buttons_Side, text="Edit", width=15, command=Run_Edit)
        Edit_Button.pack(pady=10)

    # Lower Buttons Frame
    Buttons_Lower = tk.Frame(master=Left_Middle_Frame)
    Buttons_Lower.pack()
    Lower_Buttons()

    # Side Buttons Frame
    Buttons_Side = tk.Frame(master=Middle_Frame)
    Buttons_Side.pack(anchor="ne", pady=(5, 0))
    Side_Buttons()

# Add Project
Add_Frame = tk.Frame(master=window)
def Add():
    # Sets up The configuration for the next Screen
    def Run():
        # Erasing
        Add_Frame.pack_forget()
        # Reloading
        Submit_Button.grid(row=4, column=2)
        Date_Entry.delete(0, tk.END)
        Name_Entry.delete(0, tk.END)
        Edit_set()

        # Uploading
        refresh("All")
        Main_Frame.pack()

    # Back Button
    tk.Button(master=Add_Frame, text="Back", width=10, command=Run).grid(row=1, column=1)

    # Date Input Entry
    tk.Label(master=Add_Frame, text="Date:").grid(row=2, column=1)
    Date_Entry = tk.Entry(master=Add_Frame)
    Date_Entry.grid(row=2, column=2)

    # This will appear later
    Date_Label = tk.Label(master=Add_Frame, text=strftime("%m/%d/%Y"))

    # Today set function to Change the Date_Entry
    def Today_set():
        Date_Entry.grid_forget()
        Date_Label.grid(row=2, column=2)
        Today_Button["text"] = "Edit"
        Today_Button["command"] = Edit_set

    # Edit Date function to bring back the Date_Entry
    def Edit_set():
        Date_Label.grid_forget()
        Date_Entry.grid(row=2, column=2)
        Today_Button["text"] = "Today"
        Today_Button["command"] = Today_set

    # Today's Date Input Button
    Today_Button = tk.Button(master=Add_Frame, text="Today", command=Today_set)
    Today_Button.grid(row=2, column=3, padx=(5, 0))

    # Name Input Entry
    tk.Label(master=Add_Frame, text="Name:").grid(row=3, column=1)
    Name_Entry = tk.Entry(master=Add_Frame)
    Name_Entry.grid(row=3, column=2)

    # Submit function
    def Submit():
        Submit_Button.grid_forget()

        # Getting the Inputs
        Info = Today_Button["text"]
        Name = Name_Entry.get()
        Date = None

        # Getting The Date
        if Info == "Today":
            Date = Date_Entry.get()
        elif Info == "Edit":
            Date = strftime("%m/%d/%Y")


        # Rearranging Date
        *args, year = Date.split("/")
        Date = "/".join((year, *args))

        # Getting the State
        if Date >= strftime("%Y/%m/%d"):
            State = "Due"
        elif Date < strftime("%Y/%m/%d"):
            State = "Late"
        else:
            State = ""

        # Checking to see if there was Input
        if Name != "":
            if Date != "":
                # Appending to data
                data.append({"State": State, "Date": Date, "Name": Name})
                with open("data.json", "w") as new_data:
                    json.dump(data, new_data, indent=3)

    # Submit Button
    Submit_Button = tk.Button(master=Add_Frame, text="Submit", command=Submit)
    Submit_Button.grid(row=4, column=2)

# refresh the ListBox
def refresh(pick):
    # Delete all contents
    ListBox.delete(0, tk.END)

    # Ordering Dates
    Dates = sorted([x["Date"] for x in data])

    # Goes through the Dates and counts how many times it is used
    for item in Dates:
        check = Dates.count(item)

        # if it has a count higher than 2 it will remove the next one in the list
        if check > 1:
            Dates.remove(item)

    All = []
    Due = []
    Complete = []
    Late = []
    # Goes through the Dates list
    for date in Dates:
        # if they Date matches the data's date it will insert it to the ListBox
        # also if there is more than one date that match's it will insert that one as will
        for item in data:
            if date == item["Date"]:
                # Rearranging date structure
                year, *args = date.split("/")
                new_date = "/".join((*args, year))
                state = item["State"]
                name = item["Name"]
                word = " ".join((state, new_date, name))

                # Separates all into different list to be called later
                if item["State"] == "Due":
                    Due.append(word)
                elif item["State"] == "Late":
                    Late.append(word)
                elif item["State"] == "Complete":
                    Complete.append(word)

                # Collects all of them
                All.append(word)

    if pick == "All":
        pick = All
    elif pick == "Due":
        pick = Due
    elif pick == "Late":
        pick = Late
    elif pick == "Complete":
        pick = Complete
    # Showing all of them
    for item in pick:
        ListBox.insert(tk.END, item)

# Today's Date display
Label = tk.Label(master=window, text=strftime("%m/%d/%Y"), font=("Comic Sans MS", 15))
Label.pack(pady=5)

# Loading Functions // Screens
update()
Main_Menu()
Add()

# Run
Main_Frame.pack()

# Loop
window.mainloop()

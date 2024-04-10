# Project manager 
## Modules
* tkinter
* ttkbootstrap
* json
* strftime

So to make my code more readable and easier to understand i had place them in functions to run smoother and more
easier to place more "screens".

# Main page Setup
just to make it more easier to understand we would first call the functions and make some simple frames
first the basic setup
```bash
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
```
Next we will call the "Screens" and create there Frames
```bash
# Update function will go here

# Main Menu
Main_Frame = tk.Frame(master=window)
# Main_Menu function will go here

# Add Project
Add_Frame = tk.Frame(master=window)
# Add function will go here

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
```
# Update Setup
Now to make it easy we are going to go from the top to the bottom of the program
you will need to update all the new data coming in to show a more up to date data
```bash
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
```
# Main_Frame Setup
So the first thing we do is actually load up the `Add` button and it's command
```bash
# Sets up The configuration for the next Screen
    def Run():
        # Erasing
        Main_Frame.pack_forget()
        Search_Bar.delete(0, tk.END)
        Add_Frame.pack()

    # Add Button
    Button = tk.Button(master=Main_Frame, text="ADD", width=20, height=2, command=Run)
    Button.pack()
```
This will have the buttons ready for the next screen it will erase its pack and erase anything that was typed in the
search bar.

## Middle_Frame setup
Then to give a more proper format we will create a `Middle_Frame`which will help organize the format.
```bash
    # Place Holder for ListBox & Side Buttons
    Middle_Frame = tk.Frame(master=Main_Frame)
    Middle_Frame.pack()

    # Frame for the Bottom buttons to line up right
    Left_Middle_Frame = tk.Frame(master=Middle_Frame)
    Left_Middle_Frame.pack(side=tk.LEFT)

    # ListBox Frame
    List_Frame = tk.Frame(master=Left_Middle_Frame)
    List_Frame.pack()
```
Then we get the `Side_Buttons`. I had made a function to help sort through the code. I would go check that out if you
want more details in how i did that.

Next you want to show the `Side_Buttons` & `Lower_Buttons` frame.
```bash
    # Lower Buttons Frame
    Buttons_Lower = tk.Frame(master=Left_Middle_Frame)
    Buttons_Lower.pack()
    Lower_Buttons()
    
    # Side Buttons Frame
    Buttons_Side = tk.Frame(master=Middle_Frame)
    Buttons_Side.pack(anchor="ne", pady=(5, 0))
    Side_Buttons()
```
Then I created the `Search_Bar` & the Button with that but i had again placed it in a function to help make it easier to read
```bash
    # Search Frame Setup
    def Search():
        # Search Bar
        global Search_Bar
        Search_Bar = tk.Entry(master=Search_Frame, font=("Comic Sans MS", 15))
        Search_Bar.pack(side=tk.LEFT)
        
        # Run_Search function goes here
        # This just finds what your searching
        
        # Search Button
        Search_Button = tk.Button(master=Search_Frame, text="Search", command=Run_Search)
        Search_Button.pack(side=tk.RIGHT, padx=(5, 0))
        
# Search Frame
    Search_Frame = tk.Frame(master=List_Frame)
    Search_Frame.pack(anchor="ne", pady=(5, 10))
    Search()
```

Next we want to finish Setting up The `ListBox` and the `Scroll` setup
```bash
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
```
# Refresh Setup
that refresh function would probably be best to talk about next what does is just refresh the `ListBox`which was very useful
```bash
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
```
The first thing this `refresh` function does is takes a argument which will be used later in the code
Then erases everything in the `ListBox` and then recollects all teh data and collects the dates.
Next it will check the `Dates` list and see if there are multiple of the same date, so it can filter out then data correctly.
and because the data dates are formatted different it has to rearrange the date.
```bash
for item in data:
    year, *args = data[item]["Date"].split("/")
    New_Date = "/".join((*args, year))
```
as it formats that it will next insert and filter out the State of the data item and sort them individually.
Then of course we will insert all of that information in
```bash
# Showing all of them
for item in pick:
    ListBox.insert(tk.END, item)
```

# Add_Screen Setup
Next is the Add screen again we need to setup for if it goes back to the Main Menu screen
```bash
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
```

really all i did after was make a grid to help make it look nicer later, then I created a button which erased an entry
and then sets the date to the current date and makes a label. later after u hit submit it will unpack the `Submit_Button`.

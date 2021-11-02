from tkinter import *

root = Tk()
root.title("Insane Project")
root.geometry("1600x900")

bg_img = PhotoImage(file="data/gui/images/background.png")

# bg_label = Label(root, image=bg_img)
# bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# test_text = Label(root, text='Welcome', font=("Helvatica", 24))
# test_text.pack()

# Create workspace
canvas = Canvas(root, width=1600, height=900)
canvas.pack()

# Add background image
canvas.create_image(-786, 0, image=bg_img, anchor=NW)

# Add text
canvas.create_text(800, 450, text="Sample Text", font=('Helvatica', 24), fill='Gray')

# Add button
button1 = Button(root, text='Submit')
button2 = Button(root, text='Exit', command=root.quit)

# Create windows in canvas to put buttons at specific locations
button1_window = canvas.create_window(1510, 10, anchor=NW, window=button1)
button2_window = canvas.create_window(1510, 50, anchor=NW, window=button2)

# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Click commands
def command_1():
    pass

def exit_command():
    root.quit()

def helper():
    pass

# Create menu items
file_menu = Menu(my_menu)
help_menu = Menu(my_menu)

# Add menu parameters
file_menu.add_command(label='run', command=command_1)
file_menu.add_command(label='exit', command=exit_command)
help_menu.add_command(label='Launch helper', command=helper)

# Add menus to the menubar
my_menu.add_cascade(label="File", menu=file_menu)
my_menu.add_cascade(label='Help', menu=help_menu)

root.mainloop()
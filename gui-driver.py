from tkinter import *

class MainView(Tk):
    def __init__(self):
        super().__init__()
        self.title("Insane Project")
        self.geometry("1600x900")
        
        # Background Image
        self.bg_img = PhotoImage(file="data/gui/images/background.png")
        
         # Create workspace
        self.canvas = Canvas(self, width=1600, height=900)
        self.canvas.pack()


        # Add buttons
        self.exit_button = Button(self, text='Exit', command=self.exit_command)

        # Menu bar
        mbar = Menu(self)
        self.config(menu=mbar)

        # Create menu items
        file_menu = Menu(mbar)
        help_menu = Menu(mbar)

        # Add menu parameters
        file_menu.add_command(label='run', command=self.exit_command)
        file_menu.add_command(label='exit', command=self.exit_command)
        help_menu.add_command(label='Launch helper', command=self.exit_command)

        # Add menus to the menubar
        mbar.add_cascade(label="File", menu=file_menu)
        mbar.add_cascade(label='Help', menu=help_menu)

        # Dropdown menu robustness
        self.rob_options = [
            "Backdoor Attacks",
            "Data Poisoning Attacks",
            "Model Poisoning Attacks",
            "Byzantine Attacks",
            "Free-rider Attacks",
            "Inference Attacks",
            "Byzantine Robustness",
            "Sybil Robustness",
            "Certified Robustness",
        ]
        self.rob_clicked = StringVar(self)
        self.rob_clicked.set( "Select" )
        self.robustness_drop = OptionMenu(self , self.rob_clicked , *self.rob_options, command=self.rob_option_changed)

         # Dropdown menu effectiveness
        self.eff_options = [
            "Effecitveness",
        ]
        self.eff_clicked = StringVar(self)
        self.eff_clicked.set( "Select" )
        self.eff_drop = OptionMenu(self , self.eff_clicked , *self.eff_options, command=self.eff_option_changed)

         # Dropdown menu privacy
        self.priv_options = [
            "Privacy",
        ]
        self.priv_clicked = StringVar(self)
        self.priv_clicked.set( "Select" )
        self.priv_drop = OptionMenu(self , self.priv_clicked , *self.priv_options, command=self.priv_option_changed)

         # Dropdown menu fairness
        self.fair_options = [
            "Fairness",
        ]
        self.fair_clicked = StringVar(self)
        self.fair_clicked.set( "Select" )
        self.fair_drop = OptionMenu(self , self.fair_clicked , *self.fair_options, command=self.fair_option_changed)

        # Generate app template
        self.generate_template()
        
    def generate_template(self):
        self.canvas.create_image(-786, 0, image=self.bg_img, anchor=NW)
        
        self.canvas.create_text(195, 135, text="Effectiveness", font=('Helvatica', 40), fill='Gray')
        self.canvas.create_window(80, 160, anchor=NW, window=self.eff_drop)

        self.canvas.create_text(148, 330, text="Privacy ", font=('Helvatica', 40), fill='Gray')
        self.canvas.create_window(80, 360, anchor=NW, window=self.priv_drop)

        robust_btn = PhotoImage(file="data/gui/images/robustness.png")
        self.canvas.create_text(183, 530, text="Robustness", font=('Helvatica', 40), fill='Gray')
        self.canvas.create_window(80, 560, anchor=NW, window=self.robustness_drop)

        self.canvas.create_text(152, 730, text="Fairness", font=('Helvatica', 40), fill='Gray')
        self.canvas.create_window(80, 760, anchor=NW, window=self.fair_drop)

        self.canvas.create_text(800, 450, text="Welcome", font=('Helvatica', 24), fill='Gray', tags = 'del')
        self.canvas.create_window(1500, 10, anchor=NW, window=self.exit_button)
    
    def eff_option_changed(self, *args):
        self.eff_option = self.eff_clicked.get()
        if self.eff_option == self.eff_options[0]:
            self.e_page_1()

    def priv_option_changed(self, *args):
        self.priv_option = self.priv_clicked.get()
        if self.priv_option == self.priv_options[0]:
            self.p_page_1()

    def rob_option_changed(self, *args):
        self.rob_option = self.rob_clicked.get()
        if self.rob_option == self.rob_options[0]:
            self.r_page_1()
        elif self.rob_option == self.rob_options[1]:
            self.r_page_2()
        elif self.rob_option == self.rob_options[2]:
            self.r_page_3()
        elif self.rob_option == self.rob_options[3]:
            self.r_page_4()
        elif self.rob_option == self.rob_options[4]:
            self.r_page_5()
        elif self.rob_option == self.rob_options[5]:
            self.r_page_6()
        elif self.rob_option == self.rob_options[6]:
            self.r_page_7()
        elif self.rob_option == self.rob_options[7]:
            self.r_page_8()
        elif self.rob_option == self.rob_options[8]:
            self.r_page_9()
    
    def fair_option_changed(self, *args):
        self.fair_option = self.fair_clicked.get()
        if self.fair_option == self.fair_options[0]:
            self.f_page_1()
    
    def e_page_1(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Effectiveness", font=('Helvatica', 24), fill='Gray', tags='del')
        pass
    
    def p_page_1(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Privacy", font=('Helvatica', 24), fill='Gray', tags='del')
        pass

    def r_page_1(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Backdoor Attacks", font=('Helvatica', 24), fill='Gray', tags='del')
        pass
    
    def r_page_2(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Data Poisoning Attacks", font=('Helvatica', 24), fill='Gray', tags='del')
        pass
    
    def r_page_3(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Model Poisoning Attacks", font=('Helvatica', 24), fill='Gray', tags = 'del')
        pass
    
    def r_page_4(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Byzantine Attacks", font=('Helvatica', 24), fill='Gray', tags = 'del')
        pass
    
    def r_page_5(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Free-rider Attacks", font=('Helvatica', 24), fill='Gray', tags = 'del')
        pass

    def r_page_6(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Inference Attacks", font=('Helvatica', 24), fill='Gray', tags = 'del')
        pass
    
    def r_page_7(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Byzantine Robustness", font=('Helvatica', 24), fill='Gray', tags = 'del')
        pass
    
    def r_page_8(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Sybil Robustness", font=('Helvatica', 24), fill='Gray', tags = 'del')
        pass
    
    def r_page_9(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Certified Robustness", font=('Helvatica', 24), fill='Gray', tags = 'del')
        pass
    
    def f_page_1(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Fairness", font=('Helvatica', 24), fill='Gray', tags='del')
        pass

    def exit_command(self):
        self.quit()
    
    def helper():
        pass
        
    def clean(self):
        self.canvas.delete("del")
    
    def reset(self):
        self.clean()
        self.generate_template()

if __name__ == "__main__":
    app = MainView()
    app.mainloop()
from tkinter import *
from tkinter.ttk import Progressbar
import os
import subprocess
import threading
import time

class MainView(Tk):
    def __init__(self):
        super().__init__()
        self.title("Insane Project")
        self.geometry("1600x900")

        # Root dir
        self.root_dir = os.getcwd()

        # Background Image
        self.bg_img = PhotoImage(file="data/gui/images/background.png")

        # Button Image
        self.robust_btn = PhotoImage(file="data/gui/images/robustness.png")
        
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
            "Data-Free Knowledge Distillation",
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
        self.canvas.create_text(800, 100,
            text='Data-Free Knowledge Distillation for Heterogeneous Federated Learning',
            font=('Helvatica', 24), fill='Gray', tags='del')

        self.pb = Progressbar(self.canvas, orient=HORIZONTAL, length=100, mode='indeterminate')
        self.canvas.create_window(700,700,window=self.pb.place(x=700,y=700))

        def thread_init():
            self.start_thread = threading.Thread(target=start_progress)
            self.start_thread.start()

        def start_progress():
            self.pb.start()
            self.next_thread = threading.Thread(target=callback)
            self.next_thread.start()
            self.next_thread.join()
            self.pb.stop()
            self.pb.config(value=0,maximum=100)

        def callback():
            # create dataset
            #pb = Progressbar(sefl.canvas, orient=HORIZONTAL, length=100, mode='determinant')
            #self.create_window(700,700,window=pb.place(x=700,y=700))
            home = os.getcwd()
            os.chdir("Algs/FedGen/data/{}".format(self.dataset_clicked.get()))

            p = [
                "python",
                "generate_niid_dirichlet.py",
                "--n_class",
                self.classes_field.get(),
                "--sampling_ratio",
                self.sampling_field.get(),
                "--alpha",
                self.alpha_field.get(),
                "--n_user",
                "20"]

            build_data = subprocess.call(p)

            os.chdir(home)
            os.chdir("Algs/FedGen")

            # run algorithm with args
            p2 = [
                "python",
                "main.py",
                "--dataset",
                "{}-alpha{}-ratio{}".format(
                    self.dataset_clicked.get(),
                    self.alpha_field.get(),
                    self.sampling_field.get()),
                "--algorithm",
                self.alg_clicked.get(),
                "--batch_size",
                self.batch_field.get(),
                "--num_glob_iters",
                self.global_itr_field.get(),
                "--local_epochs",
                self.epoch_field.get(),
                "--num_users",
                self.users_field.get(),
                "--lamda",
                "1",
                "--learning_rate",
                self.learning_rate_field.get(),
                "--model",
                self.model_clicked.get(),
                "--personal_learning_rate",
                self.per_learning_rate_field.get(),
                "--times",
                self.training_clicked.get()]

            run_exp = subprocess.Popen(p2)

            while run_exp.poll() is None:
                pass

        """
            Args for algorithm: (need to remove some of these)
                x clients - 1,2,3 (remove)
                x dataset - mnist or emnist
                x alpha - float 0.1
                x sampling ratio - float 0.5
                x classes - 10
                x algorithm - FedGen, FedAvg, FedProx, FedDstll-FL
                x batch size - 32
                x global iterations (rounds) - 200
                x epochs - 20
                x users - 10
                x learning rate - 0.01
                x model - cnn or mfl
                x personal learning rate - 0.01
                x training iterations - 3
        """
        # options
        self.dataset_options = ['Mnist','EMnist']
        self.alg_options = ['FedGen', 'FedAvg', 'FedProx', 'FedDistll-FL']
        self.model_options = ['cnn', 'mfl']
        self.training_options = ['1', '2', '3']

        # variables
        self.dataset_clicked = StringVar(self.canvas, value='Mnist')
        self.learning_rate = StringVar(self.canvas, value='0.01')
        self.alg_clicked = StringVar(self.canvas, value='FedGen')
        self.model_clicked = StringVar(self.canvas, value='cnn')
        self.training_clicked = StringVar(self.canvas, value='1')

        # global iterations field
        self.global_itr_field = Entry(self.canvas)
        self.global_itr_field.insert(END, '5')
        self.global_itr_label = Label(self.canvas, text='Global Iterations', bg="#E2E3DB")
        self.canvas.create_window(800, 500, window=self.global_itr_label.place(x=800,y=200))
        self.canvas.create_window(900, 500, window=self.global_itr_field.place(x=950,y=200))

        # personal learning rate field
        self.per_learning_rate_field = Entry(self.canvas)
        self.per_learning_rate_field.insert(END, '0.01')
        self.per_learning_rate_label = Label(self.canvas, text='Personal Learning Rate', bg="#E2E3DB")
        self.canvas.create_window(500, 400, window=self.per_learning_rate_label.place(x=450,y=500))
        self.canvas.create_window(600, 400, window=self.per_learning_rate_field.place(x=600,y=500))

        # users size field
        self.users_field = Entry(self.canvas)
        self.users_field.insert(END, '10')
        self.users_label = Label(self.canvas, text='Users', bg="#E2E3DB")
        self.canvas.create_window(800, 400, window=self.users_label.place(x=800,y=450))
        self.canvas.create_window(900, 400, window=self.users_field.place(x=950,y=450))

        # epochs field
        self.epoch_field = Entry(self.canvas)
        self.epoch_field.insert(END, '20')
        self.epoch_label = Label(self.canvas, text='Epochs', bg="#E2E3DB")
        self.canvas.create_window(500, 450, window=self.epoch_label.place(x=450,y=450))
        self.canvas.create_window(600, 450, window=self.epoch_field.place(x=600,y=450))

        # iterations dropdown
        self.training_drop = OptionMenu(self.canvas, self.training_clicked, *self.training_options)
        self.training_drop.config(bg = "#E2E3DB")
        self.training_label = Label(self.canvas, text='Training Rounds', bg="#E2E3DB")
        self.canvas.create_window(800, 400, window=self.training_label.place(x=800,y=400))
        self.canvas.create_window(900, 400, window=self.training_drop.place(x=950,y=400))

        # batch size field
        self.batch_field = Entry(self.canvas)
        self.batch_field.insert(END, '32')
        self.batch_label = Label(self.canvas, text='Number of Batches', bg="#E2E3DB")
        self.canvas.create_window(500, 400, window=self.batch_label.place(x=450,y=400))
        self.canvas.create_window(600, 400, window=self.batch_field.place(x=600,y=400))

        # classes field
        self.classes_field = Entry(self.canvas)
        self.classes_field.insert(END, '10')
        self.classes_label = Label(self.canvas, text='Classes', bg="#E2E3DB")
        self.canvas.create_window(800, 350, window=self.classes_label.place(x=800,y=350))
        self.canvas.create_window(900, 350, window=self.classes_field.place(x=950,y=350))

        # sampling ratio field
        self.sampling_field = Entry(self.canvas)
        self.sampling_field.insert(END, '0.5')
        self.sampling_label = Label(self.canvas, text='Sampling Ratio', bg="#E2E3DB")
        self.canvas.create_window(500, 350, window=self.sampling_label.place(x=450,y=350))
        self.canvas.create_window(600, 350, window=self.sampling_field.place(x=600,y=350))

        # alpha field
        self.alpha_field = Entry(self.canvas)
        self.alpha_field.insert(END, '0.1')
        self.alpha_label = Label(self.canvas, text='Alpha', bg="#E2E3DB")
        self.canvas.create_window(800, 300, window=self.alpha_label.place(x=800,y=300))
        self.canvas.create_window(900, 300, window=self.alpha_field.place(x=950,y=300))

        # model dropdown
        self.model_drop = OptionMenu(self.canvas, self.model_clicked, *self.model_options)
        self.model_drop.config(bg = "#E2E3DB")
        self.model_label = Label(self.canvas, text='Model', bg="#E2E3DB")
        self.canvas.create_window(500, 300, window=self.model_label.place(x=450,y=300))
        self.canvas.create_window(600, 300, window=self.model_drop.place(x=600,y=300))

        # dataset dropdown
        self.dataset_drop = OptionMenu(self.canvas, self.dataset_clicked, *self.dataset_options)
        self.dataset_drop.config(bg = "#E2E3DB")
        self.dataset_label = Label(self.canvas, text='Dataset', bg="#E2E3DB")
        self.canvas.create_window(800, 200, window=self.dataset_label.place(x=450,y=200))
        self.canvas.create_window(900, 200, window=self.dataset_drop.place(x=600,y=200))

        # algorithm dropdown
        self.alg_drop = OptionMenu(self.canvas, self.alg_clicked, *self.alg_options)
        self.alg_drop.config(bg = "#E2E3DB")
        self.alg_label = Label(self.canvas, text='Algorithm', bg="#E2E3DB")
        self.canvas.create_window(500, 300, window=self.alg_label.place(x=450,y=250))
        self.canvas.create_window(600, 300, window=self.alg_drop.place(x=600,y=250))

        # learning rate field
        self.learning_rate_field = Entry(self.canvas)
        self.learning_rate_field.insert(END, '0.01')
        self.learning_rate_label = Label(self.canvas, text='Learning Rate', bg="#E2E3DB")
        self.canvas.create_window(800, 300, window=self.learning_rate_label.place(x=800,y=250))
        self.canvas.create_window(900, 300, window=self.learning_rate_field.place(x=950,y=250))

        # submit button
        self.submit_btn = Button(self.canvas, text="Submit", width=10, command=thread_init)
        self.canvas.create_window(800, 600, window=self.submit_btn.place(x=700,y=600))

        #canvas_entry_widgets = [
        #    self.submit_btn,
        #    self.learning_rate_field, self.learning_rate_label,
        #    self.alg_drop, self.alg_label,
        #    self.dataset_drop, self.dataset_label,
        #    self.model_drop, self.model_label,
        #    self.alpha_field, self.alpha_label,
        #    self.sampling_field, self.sampling_label,
        #    self.batch_field, self.batch_label,
        #    self.classes_field, self.classes_label,
        #    self.training_drop, self.training_label,
        #    self.epoch_field, self.epoch_label,
        #    self.users_field, self.users_label,
        #    self.global_itr_field, self.global_itr_label,
        #    self.per_learning_rate_field, self.per_learning_rate_label
        #    ]

    def p_page_1(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Privacy", font=('Helvatica', 24), fill='Gray', tags='del')
        pass

    def r_page_1(self):
        self.clean()
        self.canvas.create_text(800, 450, text="Backdoor Attacks", font=('Helvatica', 24), fill='Gray', tags='del')
        pass

    def r_page_2(self):
        def download_datasets():
            os.chdir("Algs/DataPoisoning/")
            p = ["python", "generate_data_distribution.py"]
            subprocess.call(p)
            p = ["python", "generate_default_models.py"]
            subprocess.call(p)
        
        def donwload_btn_actions():
            self.download_btn['text'] = 'Downloading'
            self.canvas.delete('loading_data')
        
        def download_btn_threads():
            self.download_btn['text'] = 'Downloading'
            download_process = threading.Thread(target=download_datasets)
            download_btn_act = threading.Thread(target=donwload_btn_actions)
            self.pb.start()
            download_btn_act.start()
            download_process.start()
            download_process.join()
            download_btn_act.join()
            self.pb.stop()
            self.canvas.delete('download')
            self.canvas.create_text(800, 300, text='Done downloading', font=('Helvatica', 20), fill='Gray', tags='next')
            self.next_btn = Button(self, text='Next', command=next)
            self.canvas.create_window(800, 600, window=self.next_btn, tags = 'next')
        
        def download_btn_pressed():
            self.pb = Progressbar(self.canvas, orient=HORIZONTAL, length=200, mode='indeterminate')
            self.canvas.create_window(800,550, window=self.pb, tags='download')
            self.main_thread = threading.Thread(target=download_btn_threads)
            self.main_thread.start()
        
        def next():
            self.canvas.delete('next')
            self.canvas.create_text(800, 300, text='Page 2', font=('Helvatica', 20), fill='Gray', tags='next')

        self.clean()
        self.canvas.create_text(800, 100,
            text='Data Poisoning Attacks Against Federated Learning',
            font=('Helvatica', 24), fill='Gray', tags='del')
        
        self.canvas.create_text(800, 300,
            text='Download datasets',
            font=('Helvatica', 20), fill='Gray', tags='loading_data')
  
        self.download_btn = Button(self, text='Download', command=download_btn_pressed)
        self.canvas.create_window(800, 600, window=self.download_btn, tags='download')

        # self.canvas.create_text(800, 300,
        #     text='Done',
        #     font=('Helvatica', 20), fill='Gray', tags='dd')
        
        # self.canvas.delete('d')

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
        self.canvas.create_text(800, 450, text="Federated Learning Fairness Algorithm Assessment", font=('Helvatica', 24), fill='Gray', tags='del')
        pass

    def exit_command(self):
        self.quit()

    def helper():
        pass

    def clean(self, dir_reset=True):
        if dir_reset:
            os.chdir(self.root_dir)
        self.canvas.delete("del")
    
    def reset(self):
        self.clean()
        self.generate_template()

if __name__ == "__main__":
    app = MainView()
    app.mainloop()
from tkinter import *
from tkinter.ttk import Progressbar
import os
import subprocess
import threading
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import h5py
import json

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

        self.pb = Progressbar(self.canvas, orient=HORIZONTAL, length=100, mode='determinate')
        self.canvas.create_window(700,700,window=self.pb,tags='page-1')

        def thread_init():
            self.start_thread = threading.Thread(target=start_progress)
            self.start_thread.start()

        def start_progress():
            self.pb.start()
            self.next_thread = threading.Thread(target=callback)
            self.next_thread.start()
            self.next_thread.join()
            self.pb.stop()

        def callback():
            # create dataset

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

            self.submit_btn.destroy()
            self.next_btn = Button(self, text='Next', command=results_page)
            self.canvas.create_window(700, 600, window=self.next_btn,tags='page-1')


        def page_1():
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
            self.canvas.create_window(800, 200, window=self.global_itr_label,tags='page-1')
            self.canvas.create_window(950, 200, window=self.global_itr_field,tags='page-1')

            # personal learning rate field
            self.per_learning_rate_field = Entry(self.canvas)
            self.per_learning_rate_field.insert(END, '0.01')
            self.per_learning_rate_label = Label(self.canvas, text='Personal Learning Rate', bg="#E2E3DB")
            self.canvas.create_window(400, 500, window=self.per_learning_rate_label,tags='page-1')
            self.canvas.create_window(600, 500, window=self.per_learning_rate_field,tags='page-1')

            # users size field
            self.users_field = Entry(self.canvas)
            self.users_field.insert(END, '10')
            self.users_label = Label(self.canvas, text='Users', bg="#E2E3DB")
            self.canvas.create_window(800, 450, window=self.users_label,tags='page-1')
            self.canvas.create_window(950, 450, window=self.users_field,tags='page-1')

            # epochs field
            self.epoch_field = Entry(self.canvas)
            self.epoch_field.insert(END, '20')
            self.epoch_label = Label(self.canvas, text='Epochs', bg="#E2E3DB")
            self.canvas.create_window(400, 450, window=self.epoch_label,tags='page-1')
            self.canvas.create_window(600, 450, window=self.epoch_field,tags='page-1')

            # iterations dropdown
            self.training_drop = OptionMenu(self.canvas, self.training_clicked, *self.training_options)
            self.training_drop.config(bg = "#E2E3DB")
            self.training_label = Label(self.canvas, text='Training Rounds', bg="#E2E3DB")
            self.canvas.create_window(800, 400, window=self.training_label,tags='page-1')
            self.canvas.create_window(950, 400, window=self.training_drop,tags='page-1')

            # batch size field
            self.batch_field = Entry(self.canvas)
            self.batch_field.insert(END, '32')
            self.batch_label = Label(self.canvas, text='Number of Batches', bg="#E2E3DB")
            self.canvas.create_window(400, 400, window=self.batch_label,tags='page-1')
            self.canvas.create_window(600, 400, window=self.batch_field,tags='page-1')

            # classes field
            self.classes_field = Entry(self.canvas)
            self.classes_field.insert(END, '10')
            self.classes_label = Label(self.canvas, text='Classes', bg="#E2E3DB")
            self.canvas.create_window(800, 350, window=self.classes_label,tags='page-1')
            self.canvas.create_window(950, 350, window=self.classes_field,tags='page-1')

            # sampling ratio field
            self.sampling_field = Entry(self.canvas)
            self.sampling_field.insert(END, '0.5')
            self.sampling_label = Label(self.canvas, text='Sampling Ratio', bg="#E2E3DB")
            self.canvas.create_window(400, 350, window=self.sampling_label,tags='page-1')
            self.canvas.create_window(600, 350, window=self.sampling_field,tags='page-1')

            # alpha field
            self.alpha_field = Entry(self.canvas)
            self.alpha_field.insert(END, '0.1')
            self.alpha_label = Label(self.canvas, text='Alpha', bg="#E2E3DB")
            self.canvas.create_window(800, 300, window=self.alpha_label,tags='page-1')
            self.canvas.create_window(950, 300, window=self.alpha_field,tags='page-1')

            # model dropdown
            self.model_drop = OptionMenu(self.canvas, self.model_clicked, *self.model_options)
            self.model_drop.config(bg = "#E2E3DB")
            self.model_label = Label(self.canvas, text='Model', bg="#E2E3DB")
            self.canvas.create_window(400, 300, window=self.model_label,tags='page-1')
            self.canvas.create_window(600, 300, window=self.model_drop,tags='page-1')

            # dataset dropdown
            self.dataset_drop = OptionMenu(self.canvas, self.dataset_clicked, *self.dataset_options)
            self.dataset_drop.config(bg = "#E2E3DB")
            self.dataset_label = Label(self.canvas, text='Dataset', bg="#E2E3DB")
            self.canvas.create_window(400, 200, window=self.dataset_label,tags='page-1')
            self.canvas.create_window(600, 200, window=self.dataset_drop,tags='page-1')

            # algorithm dropdown
            self.alg_drop = OptionMenu(self.canvas, self.alg_clicked, *self.alg_options)
            self.alg_drop.config(bg = "#E2E3DB")
            self.alg_label = Label(self.canvas, text='Algorithm', bg="#E2E3DB")
            self.canvas.create_window(400, 250, window=self.alg_label,tags='page-1')
            self.canvas.create_window(600, 250, window=self.alg_drop,tags='page-1')

            # learning rate field
            self.learning_rate_field = Entry(self.canvas)
            self.learning_rate_field.insert(END, '0.01')
            self.learning_rate_label = Label(self.canvas, text='Learning Rate', bg="#E2E3DB")
            self.canvas.create_window(800, 250, window=self.learning_rate_label,tags='page-1')
            self.canvas.create_window(950, 250, window=self.learning_rate_field,tags='page-1')

            # submit button
            self.submit_btn = Button(self.canvas, text="Submit", width=10, command=thread_init)
            self.canvas.create_window(700, 600, window=self.submit_btn,tags='page-1')

        def finish_btn_tasks():
            p = ["rm", "-rf", "effectiveness_results.txt"]
            subprocess.call(p)
            self.exit_command()

        def s_f_btn_tasks():
            self.exit_command()
            pass

        def results_page():
            self.canvas.delete('page-1')
            self.canvas.create_text(800, 150, text='Results', font=('Helvatica', 18), fill='Gray', tags='page-2')

            filename = "results/Mnist-alpha0.1-ratio0.5_FedGen_0.01_10u_32b_20_0_embed0.h5"
            res = {}
            x1 = 400
            x2 = 600
            offset_y = 200
            with h5py.File(filename, "r") as f:
                for x in list(f.keys()):
                    res[x] = list(f[x])
                f.close()

            self.res_key = Label(self.canvas, text="Key", bg="#E2E3DB", width=20, anchor="e")
            self.canvas.create_window(x1, offset_y, window=self.res_key,tags='res-page')
            self.res_val = Label(self.canvas, text="Values", bg="#E2E3DB", width=20)
            self.canvas.create_window(x2, offset_y, window=self.res_val,tags='res-page')

            for k,v in res.items():
                offset_x = 600
                offset_y += 20
                if len(v) == 0:
                    v = [0] * int(self.global_itr_field.get())
                if len(v) > 5:
                    v = v[0:5]
                self.res_key = Label(self.canvas, text=k + ":", bg="#E2E3DB", width=20, anchor="e")
                self.canvas.create_window(x1, offset_y, window=self.res_key,tags='res-page')
                for num in v:
                    num = round(num,3)
                    self.res_val = Label(self.canvas, text=num, bg="#E2E3DB", width=10)
                    self.canvas.create_window(offset_x, offset_y, window=self.res_val,tags='res-page')
                    offset_x += 100
            os.chdir('results')
            with open('effectiveness_results.txt', 'w') as f:
                f.write(json.dumps(res))
                f.close()

            self.finish_btn = Button(self, text='Exit', command=finish_btn_tasks)
            self.canvas.create_window(1100, 675, window=self.finish_btn, tags = 'res-page')
            self.s_f_btn = Button(self, text='Save end Exit', command=s_f_btn_tasks)
            self.canvas.create_window(1000, 675, window=self.s_f_btn, tags='res-page')

        page_1()

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
        self.canvas.create_text(800, 100,
            text='Data Poisoning Attacks Against Federated Learning',
            font=('Helvatica', 24), fill='Gray', tags='del')

        def download_datasets():
            os.chdir(self.root_dir)
            os.chdir("Algs/DataPoisoning/")
            p = ["python", "generate_data_distribution.py"]
            subprocess.call(p)
            p = ["python", "generate_default_models.py"]
            subprocess.call(p)
            time.sleep(1)

        def donwload_btn_actions():
            self.canvas.delete('loading_data')
            self.canvas.delete('download_btn')
            self.canvas.create_text(800, 300, text='Downloading...', font=('Helvatica', 20), fill='Gray', tags='download')

        def download_btn_threads():
            download_process = threading.Thread(target=download_datasets)
            download_btn_act = threading.Thread(target=donwload_btn_actions)
            self.pb.start()
            download_btn_act.start()
            download_process.start()
            download_process.join()
            download_btn_act.join()
            self.pb.stop()
            self.canvas.delete('download')
            self.canvas.create_text(800, 300,
                text='Finished downloading',
                font=('Helvatica', 20), fill='Gray', tags='page-1')
            self.next_btn = Button(self, text='Next', command=page_2)
            self.canvas.create_window(800, 650, window=self.next_btn, tags = 'page-1')

        def download_btn_pressed():
            self.pb = Progressbar(self.canvas, orient=HORIZONTAL, length=200, mode='indeterminate')
            self.canvas.create_window(800,625, window=self.pb, tags='download')
            self.main_thread = threading.Thread(target=download_btn_threads)
            self.main_thread.start()

        def run():
            os.chdir(self.root_dir)
            os.chdir("Algs/DataPoisoning")

            self.method = 'label_flipping_attack.py'

            if self.alg_clicked == 'Label Flipping Attack':
                self.method = 'label_flipping_attack.py'
            elif self.alg_clicked == 'Attack Timing':
                self.method = 'attack_timing.py'
            elif self.alg_clicked == 'Malicious Participant Availibility':
                self.method = 'malicious_participant_availability.py'

            # run algorithm with args
            p = [
                "python",
                self.method,
                "--dataset",
                self.dataset_clicked.get(),
                "--batch_size",
                self.batch_size.get(),
                "--test_batch_size",
                self.tbatch_field.get(),
                "--epochs",
                self.epochs.get(),
                "--lr",
                self.lr_field.get(),
                "--momentum",
                self.mom_field.get(),
                "--cuda",
                self.cuda_clicked.get(),
                "--log_interval",
                self.log_interval_field.get(),
                "--stepsize",
                self.step_field.get(),
                "--gamma",
                self.gamma_field.get(),
                "--save_model",
                self.save_clicked.get(),
                "--num_workers",
                self.num_workers_field.get(),
                "--num_poisoned_workers",
                self.pworkers_field.get()]

            subprocess.call(p)
            time.sleep(1)

        def run_btn_actions():
            self.canvas.delete('run_btn')
            self.canvas.create_text(800, 650, text='Running', font=('Helvatica', 18), fill='Gray', tags='page-2')

        def run_btn_threads():
            run_process = threading.Thread(target=run)
            run_btn_act = threading.Thread(target=run_btn_actions)
            self.pb.start()
            run_process.start()
            run_btn_act.start()
            run_btn_act.join()
            run_process.join()
            self.pb.stop()
            self.canvas.delete('run')
            self.next_btn = Button(self, text='Next', command=page_3)
            self.canvas.create_window(800, 650, window=self.next_btn, tags = 'page-2')

        def run_btn_pressed():
            self.pb = Progressbar(self.canvas, orient=HORIZONTAL, length=200, mode='indeterminate')
            self.canvas.create_window(800,625, window=self.pb, tags='run')
            self.main_thread = threading.Thread(target=run_btn_threads)
            self.main_thread.start()

        def page_1():
            self.canvas.create_text(800, 300, text='Download Datasets', font=('Helvatica', 20), fill='Gray', tags='loading_data')

            self.cifar_img = (Image.open("data/gui/images/CIFAR-10.png"))
            self.mnist_img = (Image.open("data/gui/images/MNIST.png"))
            self.cifar_img = self.cifar_img.resize((200, 200), Image.ANTIALIAS)
            self.mnist_img = self.mnist_img.resize((200, 200), Image.ANTIALIAS)
            self.cifar_img = ImageTk.PhotoImage(self.cifar_img)
            self.mnist_img = ImageTk.PhotoImage(self.mnist_img)

            self.canvas.create_image(575, 350, image=self.mnist_img, anchor=NW, tags='page-1')
            self.canvas.create_text((675, 575), text="Fashion MNIST", font=('Helvatica', 20), fill='Gray', tags = 'page-1')

            self.canvas.create_image(825, 350, image=self.cifar_img, anchor=NW, tags='page-1')
            self.canvas.create_text((925, 575), text="CIFAR-10", font=('Helvatica', 20), fill='Gray', tags = 'page-1')

            self.download_btn = Button(self, text='Download', command=download_btn_pressed)
            self.canvas.create_window(800, 650, window=self.download_btn, tags='download_btn')

        def page_2():
            self.canvas.delete('page-1')
            self.canvas.create_text(800, 150, text='Set parameters', font=('Helvatica', 20), fill='Gray', tags='page-2')

            # options
            self.dataset_options = ['Fashion-MNIST', 'CIFAR-10']
            self.alg_options = ['Label Flipping Attack',
                                'Attack Timing',
                                'Malicious Participant Availibility']
            self.bool_dropdown = ['True', 'False']

            # Variables
            self.alg_clicked = StringVar(self.canvas, value='Label Flipping Attack')
            self.dataset_clicked = StringVar(self.canvas, value='Fashion-MNIST')
            self.training_clicked = StringVar(self.canvas, value='1')
            self.cuda_clicked = StringVar(self.canvas, value='True')
            self.save_clicked = StringVar(self.canvas, value='False')

            # Algorithm dropdown
            self.alg_drop = OptionMenu(self.canvas, self.alg_clicked, *self.alg_options)
            self.alg_drop.config(bg = "#E2E3DB")
            self.alg_label = Label(self.canvas, text='Method', bg="#E2E3DB")
            self.canvas.create_window(450, 200, anchor=NW, window=self.alg_label, tags='page-2')
            self.canvas.create_window(600, 200, anchor=NW, window=self.alg_drop, tags='page-2')

            # Dataset dropdown
            self.dataset_drop = OptionMenu(self.canvas, self.dataset_clicked, *self.dataset_options)
            self.dataset_drop.config(bg = "#E2E3DB")
            self.dataset_label = Label(self.canvas, text='Dataset', bg="#E2E3DB")
            self.canvas.create_window(450, 250, anchor=NW, window=self.dataset_label, tags='page-2')
            self.canvas.create_window(600, 250, anchor=NW, window=self.dataset_drop, tags='page-2')

            # Batch size field
            self.batch_size = Entry(self.canvas)
            self.batch_size.insert(END, '10')
            self.batch_size_label = Label(self.canvas, text='Batch Size', bg="#E2E3DB")
            self.canvas.create_window(450, 300, anchor=NW, window=self.batch_size_label, tags='page-2')
            self.canvas.create_window(600, 300, anchor=NW, window=self.batch_size, tags='page-2')

            # Test Batch Size field
            self.tbatch_field = Entry(self.canvas)
            self.tbatch_field.insert(END, '1000')
            self.tbatch_label = Label(self.canvas, text='Test Batch Size', bg="#E2E3DB")
            self.canvas.create_window(450, 350, anchor=NW, window=self.tbatch_label, tags='page-2')
            self.canvas.create_window(600, 350, anchor=NW, window=self.tbatch_field, tags='page-2')

            # Epochs field
            self.epochs = Entry(self.canvas)
            self.epochs.insert(END, '10')
            self.epochs_label = Label(self.canvas, text='Epochs', bg="#E2E3DB")
            self.canvas.create_window(450, 400, anchor=NW, window=self.epochs_label, tags='page-2')
            self.canvas.create_window(600, 400, anchor=NW, window=self.epochs, tags='page-2')

            # Learning rate field
            self.lr_field = Entry(self.canvas)
            self.lr_field.insert(END, '0.01')
            self.lr_label = Label(self.canvas, text='Learning Rate', bg="#E2E3DB")
            self.canvas.create_window(450, 450, anchor=NW, window=self.lr_label, tags='page-2')
            self.canvas.create_window(600, 450, anchor=NW, window=self.lr_field, tags='page-2')

            # Momentum Field
            self.mom_field = Entry(self.canvas)
            self.mom_field.insert(END, '0.5')
            self.mom_label = Label(self.canvas, text='Momentum', bg="#E2E3DB")
            self.canvas.create_window(450, 500, anchor=NW, window=self.mom_label, tags='page-2')
            self.canvas.create_window(600, 500, anchor=NW, window=self.mom_field, tags='page-2')

            # Use GPU field
            self.cuda_field = OptionMenu(self.canvas, self.cuda_clicked, *self.bool_dropdown)
            self.cuda_field.config(bg = "#E2E3DB")
            self.cuda_label = Label(self.canvas, text='GPU acceleration', bg="#E2E3DB")
            self.canvas.create_window(825, 200, anchor=NW, window=self.cuda_label, tags='page-2')
            self.canvas.create_window(975, 200, anchor=NW, window=self.cuda_field, tags='page-2')

            # Stepsize field
            self.step_field = Entry(self.canvas)
            self.step_field.insert(END, '50')
            self.step_label = Label(self.canvas, text='Step size', bg="#E2E3DB")
            self.canvas.create_window(825, 250, anchor=NW, window=self.step_label, tags='page-2')
            self.canvas.create_window(975, 250, anchor=NW, window=self.step_field, tags='page-2')

            # Gamma field
            self.gamma_field = Entry(self.canvas)
            self.gamma_field.insert(END, '0.5')
            self.gamma_label = Label(self.canvas, text='Gamma', bg="#E2E3DB")
            self.canvas.create_window(825, 300, anchor=NW, window=self.gamma_label, tags='page-2')
            self.canvas.create_window(975, 300, anchor=NW, window=self.gamma_field, tags='page-2')

            # Save menu
            self.save_field = OptionMenu(self.canvas, self.save_clicked, *self.bool_dropdown)
            self.save_field.config(bg = "#E2E3DB")
            self.save_label = Label(self.canvas, text='Save model', bg="#E2E3DB")
            self.canvas.create_window(825, 350, anchor=NW, window=self.save_label, tags='page-2')
            self.canvas.create_window(975, 350, anchor=NW, window=self.save_field, tags='page-2')

            # Number of workers
            self.num_workers_field = Entry(self.canvas)
            self.num_workers_field.insert(END, '50')
            self.num_workers_label = Label(self.canvas, text='# of workers', bg="#E2E3DB")
            self.canvas.create_window(825, 400, anchor=NW, window=self.num_workers_label, tags='page-2')
            self.canvas.create_window(975, 400, anchor=NW, window=self.num_workers_field, tags='page-2')

            # Number of poisoned workers
            self.pworkers_field = Entry(self.canvas)
            self.pworkers_field.insert(END, '25')
            self.pworkers_label = Label(self.canvas, text='# of poisoned workers', bg="#E2E3DB")
            self.canvas.create_window(825, 450, anchor=NW, window=self.pworkers_label, tags='page-2')
            self.canvas.create_window(975, 450, anchor=NW, window=self.pworkers_field, tags='page-2')

            # Log interval
            self.log_interval_field = Entry(self.canvas)
            self.log_interval_field.insert(END, '100')
            self.log_interval_label = Label(self.canvas, text='Log interval', bg="#E2E3DB")
            self.canvas.create_window(825, 500, anchor=NW, window=self.log_interval_label, tags='page-2')
            self.canvas.create_window(975, 500, anchor=NW, window=self.log_interval_field, tags='page-2')

            self.run_btn = Button(self, text='Run', command=run_btn_pressed)
            self.canvas.create_window(800, 650, window=self.run_btn, tags='run_btn')

        def finish_btn_tasks():
            p = ["rm", "-rf", "temp.png"]
            subprocess.call(p)
            self.exit_command()

        def s_f_btn_tasks():
            p = ["mv", "temp.png", "Algs/DataPoisoning/saved_plots/acc_plot_"+self.method[:-3]+".png"]
            subprocess.call(p)
            self.exit_command()
            pass

        def page_3():
            os.chdir(self.root_dir)
            self.canvas.delete('page-2')
            self.canvas.create_text(800, 150, text='Results', font=('Helvatica', 18), fill='Gray', tags='page-3')

            FILEPATH = 'Algs/DataPoisoning/3000_results.csv'
            df = pd.read_csv(FILEPATH, header=None)
            acc_plt = plt
            acc_plt.plot(df[0], color='blue')
            acc_plt.xlabel('Epochs')
            acc_plt.ylabel('Accuracy (%)')
            acc_plt.savefig('temp.png')

            self.acc_plot_fig = (Image.open("temp.png"))
            self.acc_plot_fig = ImageTk.PhotoImage(self.acc_plot_fig)

            self.canvas.create_image(500, 175, image=self.acc_plot_fig, anchor=NW, tags='page-3')
            self.canvas.create_text(600, 675, text="Final Accuracy: " + str(df[0][int(self.epochs.get()) - 1]),
                                    font=('Helvatica', 18), fill='Gray', tags='page-3')

            self.finish_btn = Button(self, text='Exit', command=finish_btn_tasks)
            self.canvas.create_window(1100, 675, window=self.finish_btn, tags = 'page-3')
            self.s_f_btn = Button(self, text='Save end Exit', command=s_f_btn_tasks)
            self.canvas.create_window(1000, 675, window=self.s_f_btn, tags='page-3')

        page_1()

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
        
        def download_datasets():
            os.chdir(self.root_dir)
            os.chdir("Algs/Fairness/")
            p = ["python", "generate_fedtask.py"]
            subprocess.call(p)
            #p = ["python", "main.py"]
            #subprocess.call(p)
            time.sleep(1)
            
        def donwload_btn_actions():
            self.canvas.delete('loading_data')
            self.canvas.delete('download_btn')
            self.canvas.create_text(800, 300, text='Downloading...', font=('Helvatica', 20), fill='Gray', tags='download')
        
        def download_btn_threads():
            download_process = threading.Thread(target=download_datasets)
            download_btn_act = threading.Thread(target=donwload_btn_actions)
            self.pb.start()
            download_btn_act.start()
            download_process.start()
            download_process.join()
            download_btn_act.join()
            self.pb.stop()
            self.canvas.delete('download')
            self.canvas.create_text(800, 300, 
                text='Finished downloading', 
                font=('Helvatica', 20), fill='Gray', tags='page-1')
            self.next_btn = Button(self, text='Next', command=page_2)
            self.canvas.create_window(800, 650, window=self.next_btn, tags = 'page-1')
        
        def download_btn_pressed():
            self.pb = Progressbar(self.canvas, orient=HORIZONTAL, length=200, mode='indeterminate')
            self.canvas.create_window(800,625, window=self.pb, tags='download')
            path = 'Algs/Fairness/fedtask/mnist_client100_dist0_beta0_noise0/record/'
            files = os.listdir(path)

            # remove any existing files from previous runs
            for f in files:
                os.remove(path+f)

            self.main_thread = threading.Thread(target=download_btn_threads)
            self.main_thread.start()

        def run():

            os.chdir(self.root_dir)
            os.chdir("Algs/Fairness")

            self.method = 'fedavg'

            if self.method_clicked == 'FedAvg':
                self.method = 'fedavg'
            elif self.method_clicked == 'FedProx':
                self.method = 'fedprox'
            elif self.method_clicked == 'FedFV':
                self.method = 'fedfv'        
            
            # run algorithm with args
            # python main.py --task mnist_client100_dist0_beta0_noise0 --model cnn --method fedavg --num_rounds 20 --num_epochs 5 --learning_rate 0.215 --proportion 0.1 --batch_size 10 --train_rate 1 --eval_interval 1
            p = [
                "python",
                "main.py",
                "--task", 
                "mnist_client100_dist0_beta0_noise0",
                "--model",
                "cnn",
                "--method",
                self.method,
                "--num_rounds",
                self.num_rounds.get(),
                "--num_epochs",
                self.epochs.get(),
                "--learning_rate",
                self.lr.get(),
                "--proportion",
                self.proportion.get(),
                "--batch_size",
                self.batch_size.get(),
                "--train_rate",
                self.train_rate.get(),
                "--eval_interval",
                self.eval_interval.get(),
                ]

            self.tic = time.perf_counter()
            subprocess.call(p)
            self.toc = time.perf_counter()
            time.sleep(1)

        def run_btn_actions():
            self.canvas.delete('run_btn')
            self.canvas.create_text(800, 650, text='Running', font=('Helvatica', 18), fill='Gray', tags='page-2')

        def run_btn_threads():
            run_process = threading.Thread(target=run)
            run_btn_act = threading.Thread(target=run_btn_actions)
            self.pb.start()
            run_process.start()
            run_btn_act.start()
            run_btn_act.join()
            run_process.join()
            self.pb.stop()
            self.canvas.delete('run')
            self.next_btn = Button(self, text='Next', command=page_3)
            self.canvas.create_window(800, 650, window=self.next_btn, tags = 'page-2')

        def run_btn_pressed():
            self.pb = Progressbar(self.canvas, orient=HORIZONTAL, length=200, mode='indeterminate')
            self.canvas.create_window(800,625, window=self.pb, tags='run')
            self.main_thread = threading.Thread(target=run_btn_threads)
            self.main_thread.start()

        def page_1():
            self.canvas.create_text(800, 250, text="Federated Learning Fairness Algorithm Assessment", font=('Helvatica', 24), fill='Black', tags='loading_data')
            self.canvas.create_text(800, 600, text='Download Datasets', font=('Helvatica', 30), fill='Black', tags='loading_data')
            self.canvas.create_text(800, 300, text='Using the MNIST Dataset', font=('Helvatica', 20), fill='Black', tags='loading_data')
            self.download_btn = Button(self, text='Download', command=download_btn_pressed)
            self.canvas.create_window(800, 650, window=self.download_btn, tags='download_btn')
        
        def page_2():
            self.canvas.delete('page-1')
            self.canvas.create_text(800, 150, text='Set parameters', font=('Helvatica', 20), fill='Gray', tags='page-2')

            # options
            self.method_options = ['FedAvg', 
                                'FedProx', 
                                'FedFV']
            self.bool_dropdown = ['True', 'False']

            # Variables
            self.method_clicked = StringVar(self.canvas, value='FedAvg')
            self.training_clicked = StringVar(self.canvas, value='1')
            self.cuda_clicked = StringVar(self.canvas, value='True')
            self.save_clicked = StringVar(self.canvas, value='False')

            # python main.py --task mnist_client100_dist0_beta0_noise0 --model cnn --method fedavg --num_rounds 20 --num_epochs 5 --learning_rate 0.215 --proportion 0.1 --batch_size 10 --train_rate 1 --eval_interval 1
            # Method dropdown
            self.method_drop = OptionMenu(self.canvas, self.method_clicked, *self.method_options)
            self.method_drop.config(bg = "#E2E3DB")
            self.method_label = Label(self.canvas, text='Method', bg="#E2E3DB")
            self.canvas.create_window(450, 200, anchor=NW, window=self.method_label, tags='page-2')
            self.canvas.create_window(600, 200, anchor=NW, window=self.method_drop, tags='page-2')
            
            # Number of Rounds Size field
            self.num_rounds = Entry(self.canvas)
            self.num_rounds.insert(END, '10')
            self.num_rounds_label = Label(self.canvas, text='Number of Rounds', bg="#E2E3DB")
            self.canvas.create_window(450, 250, anchor=NW, window=self.num_rounds_label, tags='page-2')
            self.canvas.create_window(600, 250, anchor=NW, window=self.num_rounds, tags='page-2')

            # Epochs field
            self.epochs = Entry(self.canvas)
            self.epochs.insert(END, '5')
            self.epochs_label = Label(self.canvas, text='Epochs', bg="#E2E3DB")
            self.canvas.create_window(450, 300, anchor=NW, window=self.epochs_label, tags='page-2')
            self.canvas.create_window(600, 300, anchor=NW, window=self.epochs, tags='page-2')

            # Learning rate field
            self.lr = Entry(self.canvas)
            self.lr.insert(END, '0.215')
            self.lr_label = Label(self.canvas, text='Learning Rate', bg="#E2E3DB")
            self.canvas.create_window(450, 350, anchor=NW, window=self.lr_label, tags='page-2')
            self.canvas.create_window(600, 350, anchor=NW, window=self.lr, tags='page-2')

            # Proportion field
            self.proportion = Entry(self.canvas)
            self.proportion.insert(END, '0.1')
            self.proportion_label = Label(self.canvas, text='Proportion', bg="#E2E3DB")
            self.canvas.create_window(450, 400, anchor=NW, window=self.proportion_label, tags='page-2')
            self.canvas.create_window(600, 400, anchor=NW, window=self.proportion, tags='page-2')

            # Batch Size field
            self.batch_size = Entry(self.canvas)
            self.batch_size.insert(END, '10')
            self.batch_size_label = Label(self.canvas, text='Batch Size', bg="#E2E3DB")
            self.canvas.create_window(450, 450, anchor=NW, window=self.batch_size_label, tags='page-2')
            self.canvas.create_window(600, 450, anchor=NW, window=self.batch_size, tags='page-2')

            # Training Rate field
            self.train_rate = Entry(self.canvas)
            self.train_rate.insert(END, '1')
            self.train_rate_label = Label(self.canvas, text='Training Rate', bg="#E2E3DB")
            self.canvas.create_window(450, 500, anchor=NW, window=self.train_rate_label, tags='page-2')
            self.canvas.create_window(600, 500, anchor=NW, window=self.train_rate, tags='page-2')

            # Eval Interval field
            self.eval_interval = Entry(self.canvas)
            self.eval_interval.insert(END, '1')
            self.eval_interval_label = Label(self.canvas, text='Evaluation Interval', bg="#E2E3DB")
            self.canvas.create_window(450, 550, anchor=NW, window=self.eval_interval_label, tags='page-2')
            self.canvas.create_window(600, 550, anchor=NW, window=self.eval_interval, tags='page-2')

            # Save menu
            self.save_field = OptionMenu(self.canvas, self.save_clicked, *self.bool_dropdown)
            self.save_field.config(bg = "#E2E3DB")
            self.save_label = Label(self.canvas, text='Save model', bg="#E2E3DB")
            self.canvas.create_window(825, 350, anchor=NW, window=self.save_label, tags='page-2')
            self.canvas.create_window(975, 350, anchor=NW, window=self.save_field, tags='page-2')

            self.run_btn = Button(self, text='Run', command=run_btn_pressed)
            self.canvas.create_window(800, 650, window=self.run_btn, tags='run_btn')
        
        def finish_btn_tasks():
            p = ["rm", "-rf", "temp.png"]
            subprocess.call(p)
            self.exit_command()
        
        def s_f_btn_tasks():
            p = ["mv", "temp.png", "Algs/Fairness/saved_plots/acc_plot_"+self.method[:-3]+".png"]
            subprocess.call(p)
            self.exit_command()
            pass

        def page_3():
            os.chdir(self.root_dir)
            self.canvas.delete('page-2')
            self.canvas.create_text(800, 150, text='Results', font=('Helvatica', 18), fill='Gray', tags='page-3')
            
            path = 'Algs/Fairness/fedtask/mnist_client100_dist0_beta0_noise0/record/'
            files = os.listdir(path)

            for f in files:
                with open(path+f) as json_data:
                    data = json.load(json_data)

            accuracy = data['valid_accs']    

            print(accuracy)

            acc_plt = plt
            acc_plt.plot(accuracy, color='green')
            acc_plt.xlabel('Number of Rounds')
            acc_plt.ylabel('Accuracy (%)')
            acc_plt.savefig('temp.png')

            self.acc_plot_fig = (Image.open("temp.png"))
            self.acc_plot_fig = ImageTk.PhotoImage(self.acc_plot_fig)

            self.canvas.create_image(500, 175, image=self.acc_plot_fig, anchor=NW, tags='page-3')
            self.canvas.create_text(600, 675, text="Final Accuracy: " + str(accuracy[int(self.num_rounds.get()) - 1]), 
                                    font=('Helvatica', 18), fill='Gray', tags='page-3')
            self.canvas.create_text(600, 715, text="Elapsed time: " + str(self.toc - self.tic), 
                                    font=('Helvatica', 18), fill='Gray', tags='page-3')                        
        
            self.finish_btn = Button(self, text='Exit', command=finish_btn_tasks)
            self.canvas.create_window(1100, 675, window=self.finish_btn, tags = 'page-3')
            self.s_f_btn = Button(self, text='Save end Exit', command=s_f_btn_tasks)
            self.canvas.create_window(1000, 675, window=self.s_f_btn, tags='page-3')

        page_1()

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

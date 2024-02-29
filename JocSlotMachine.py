import tkinter as tk
from tkinter import PhotoImage
import random
import time
import winsound

class SlotMachine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SlotMachine 2024")
        self.geometry("800x800")


        # Load sound effects
        self.win_sound = "win.wav"  
        self.spin_sound = "suspans.wav" 

        # Simboluri
        self.symbols = ["Cireasa", "Pepene", "Portocala", "Pruna", "Mar", "Capsuna"]

        #dictionar cu numele la imagini
        self.image_paths = {
            "Cireasa": "cherries.png",
            "Pepene": "watermelon.png",
            "Portocala": "orange.png",
            "Pruna": "plum.png",
            "Mar": "apple.png",
            "Capsuna": "strawberry.png"
        }

        self.reels = [[self.random_symbol() for _ in range(3)] for _ in range(3)]

        self.images = [[PhotoImage(file=self.image_paths[symbol]) for symbol in row] for row in self.reels]

        self.labels = [[tk.Label(self, image=self.images[i][j]) for j in range(3)] for i in range(3)]

        #creare tabel 3x3
        for i in range(3):
            for j in range(3):
                self.labels[i][j].grid(row=i, column=j, padx=10, pady=10)

        ##
                ##Butoane
                        ##Primul e Butonul de actiune
        self.spin_button = tk.Button(self, text="SPIN!", command=self.spin_reels, state="disabled", font=("Arial", 14))
        self.spin_button.grid(row=3, column=1, pady=10)

        self.signup_button = tk.Button(self, text="Inregistrare", font=("Arial", 14), command=self.show_signup_window)
        self.signup_button.grid(row=4, column=2, pady=10)

        self.balance_label = tk.Label(self, text="Balance: $0", fg = "blue", font=("Arial", 14))
        self.balance_label.grid(row=3, column=2, pady=10)

        self.message_label = tk.Label(self, text="",font=("Arial", 12))
        self.message_label.grid(row=5, column=0, columnspan=3, pady=10)

        self.login_button = tk.Button(self, text="Logare", command=self.show_login_window, font=("Arial", 14))
        self.login_button.grid(row=4, column=0, pady=10)

        self.logged_in_user = None
        #self.logged_in_user_balance = 1000

        self.user_data = self.load_user_data()

    def random_symbol(self):
        return random.choice(self.symbols)

    #Creates random simboles~~~                                         333
    def spin_reels(self): 
        result = [[self.random_symbol() for _ in range(3)] for _ in range(3)] ##memoreaza rezultatul
        self.update_images(result)
        self.check_win(result)

    def update_images(self, result):
        for i in range(3):
            for j in range(3):
                self.images[i][j] = PhotoImage(file=self.image_paths[result[i][j]])
                self.labels[i][j].config(image=self.images[i][j])
                

    def check_win(self, result):
        # Check rows
        for i in range(3):
            if result[i][0] == result[i][1] == result[i][2]:
                self.show_win_message(result[i][0])
                return

        # Check columns
        for j in range(3):
            if result[0][j] == result[1][j] == result[2][j]:
                self.show_win_message(result[0][j])
                return

        # Check diagonals
        if result[0][0] == result[1][1] == result[2][2]:
            self.show_win_message(result[0][0])
            return
        if result[0][2] == result[1][1] == result[2][0]:
            self.show_win_message(result[0][2])
            return

        # No win
        self.show_no_win_message()

    def show_win_message(self, symbol):
        message = f"Felicitari! Ati castigat cu {symbol}!"
        self.message_label.config(text=message)

        # primesti banii castigati
        self.logged_in_user_balance += random.randint(10,65)
        self.update_balance_label()

        #play wind sound
        self.play_sound(self.spin_sound)
        self.play_sound(self.win_sound)

    def show_no_win_message(self):
        message = "Ati pierdut, incercati din nou."
        self.message_label.config(text=message)

        # scad banii
        self.logged_in_user_balance -= 10
        self.update_balance_label()
        self.play_sound(self.spin_sound)

    #functia de redat suntet
    def play_sound(self, sound):
        winsound.PlaySound(sound, winsound.SND_FILENAME)

           

    def update_balance_label(self):
        self.balance_label.config(text=f"Balance: ${self.logged_in_user_balance}")
        self.user_data[self.logged_in_user]['balance'] = self.logged_in_user_balance
        self.save_user_data()

    def load_user_data(self):
        try:
            with open("users.txt", "r") as file:
                user_data = {}
                for line in file.readlines():
                    username, password, balance = line.strip().split(',')
                    user_data[username] = {'parola': password, 'balance': int(balance)}
                return user_data
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        with open("users.txt", "w") as file:
            for username, data in self.user_data.items():
                file.write(f"{username},{data['parola']},{data['balance']}\n")

    def show_login_window(self):
        login_window = tk.Toplevel(self)
        login_window.title("Logare")
        login_window.geometry("200x100")

        tk.Label(login_window, text="Utilizator:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(login_window, text="Parola:").grid(row=1, column=0, padx=5, pady=5)

        username_entry = tk.Entry(login_window)
        password_entry = tk.Entry(login_window, show="*")

        username_entry.grid(row=0, column=1, padx=5, pady=5)
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(login_window, text="Logare", command=lambda: self.login(username_entry.get(), password_entry.get(), login_window))
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def show_signup_window(self):
        signup_window = tk.Toplevel(self)
        signup_window.title("Inregistrare")
        signup_window.geometry("200x150")

        tk.Label(signup_window, text="Utilizator:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(signup_window, text="Parola:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(signup_window, text="Repetati parola:").grid(row=2, column=0, padx=5, pady=5)

        username_entry = tk.Entry(signup_window)
        password_entry = tk.Entry(signup_window, show="*")
        confirm_password_entry = tk.Entry(signup_window, show="*")

        username_entry.grid(row=0, column=1, padx=5, pady=5)
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        signup_button = tk.Button(signup_window, text="Inregistrare", command=lambda: self.signup(username_entry.get(), password_entry.get(), confirm_password_entry.get(), signup_window))
        signup_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self, username, password, login_window):
        if username in self.user_data and password == self.user_data[username]['parola']:
            self.logged_in_user = username
            self.logged_in_user_balance = self.user_data[username]['balance']
            self.update_balance_label()
            
            login_window.destroy()
            self.login_button.config(state="disabled")
            self.signup_button.config(state="disabled")
            self.spin_button.config(state="normal")
            self.message_label.config(text="")  # Clear previous messages
            return

        self.message_label.config(text="Nume utilizator sau parola gresita")

    def signup(self, username, password, confirm_password, signup_window):
        if password == confirm_password:
            if username not in self.user_data:
                self.user_data[username] = {'parola': password, 'balance': 300}  #set loggin balance
                self.save_user_data()

                signup_window.destroy()
                self.message_label.config(text="Cont inregistrat cu succes. Puteti sa va logati.")
            else:
                self.message_label.config(text="Utillizatorul deja exista")
        else:
            self.message_label.config(text="Nu se potriveste parola")

#if __name__ == "__main__":
app = SlotMachine()
app.mainloop()
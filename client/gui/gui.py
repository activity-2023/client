import customtkinter

from . import components


class Gui:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.init()

    def __call__(self, *args, **kwargs):
        self.app.mainloop()

    def button_ent(self):
        self.pwd.toggle_mask()

    def init(self):
        self.app.title("Activity Door Client")
        self.app.geometry("400x500")

        but = customtkinter.CTkButton(self.app, command=self.button_ent)
        but.pack()
        self.pwd = components.PasswordField(self.app)
        self.pwd.pack()

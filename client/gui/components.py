import customtkinter as ctk


class PasswordField(ctk.CTkEntry):
    def __init__(self, master):
        super().__init__(master, placeholder_text="password")
        self.isObfuscated = False

    def toggle_mask(self):
        if not self.isObfuscated:
            self.configure(show="*")
            self.isObfuscated = not self.isObfuscated
        else:
            self.configure(show="")
            self.isObfuscated = not self.isObfuscated

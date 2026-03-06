import customtkinter as ctk

def saludar():
    etiqueta.configure(text=f"Hola, {entrada.get()}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x250")
app.title("GUI moderna")

entrada = ctk.CTkEntry(app, placeholder_text="Escribe tu nombre")
entrada.pack(pady=20)

boton = ctk.CTkButton(app, text="Saludar", command=saludar)
boton.pack(pady=10)

etiqueta = ctk.CTkLabel(app, text="")
etiqueta.pack(pady=20)

app.mainloop()
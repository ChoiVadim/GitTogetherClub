import customtkinter as ctk

app = ctk.CTk()
app.geometry("200x400")
app.title("CTk example")

label = ctk.CTkLabel(app, text="CTkLabel")
label.pack(pady=20)

textbox = ctk.CTkTextbox(app)
textbox.pack(pady=20)

btn = ctk.CTkButton(app, text="CTkButton", command=lambda: print("Clicked!"))
btn.pack(pady=20)

app.mainloop()

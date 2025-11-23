import customtkinter as ctk

def reset_password(app):
    for widget in app.winfo_children():
        widget.destroy()

    ctk.CTkButton(app, text="Back", width=60, height=28, fg_color="#0078D7", hover_color="#005A9E", command=app.create_widgets).grid(row=0, column=0, padx=10, pady=10, sticky="w")   
    ctk.CTkLabel(
        app,
        text="Reset Password",
        font=ctk.CTkFont(size=20, weight="bold"),
        anchor="center",
        justify="center"
    ).grid(row=0, column=1, columnspan=2, pady=10, sticky="nw")
    ctk.CTkLabel(app, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    email_entry = ctk.CTkEntry(app, width=180)
    email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(app, text="Recovery Code:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    recovery_code_entry = ctk.CTkEntry(app, width=180)
    recovery_code_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    submit_btn = ctk.CTkButton(
        app, 
        text="Submit", 
        width=100, 
        state="disabled",
        command=lambda: handle_password_reset_prompt(
            app,
            email_entry.get(),
            recovery_code_entry.get()
        )
    )
    submit_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def validate_fields(*args):
        if (
            email_entry.get().strip() and
            recovery_code_entry.get().strip()
        ):
            submit_btn.configure(state="normal")
        else:
            submit_btn.configure(state="disabled")

# Implementation based on https://stackoverflow.com/questions/27215326/tkinter-keypress-and-keyrelease-events
    email_entry.bind("<KeyRelease>", validate_fields)
    recovery_code_entry.bind("<KeyRelease>", validate_fields)


def handle_password_reset_prompt(app, email, recovery_code):
    # TODO: Waiting on Backend to implement password reset logic
    if email != "admin" and recovery_code != "123":
        ctk.CTkLabel(app, text="Reset Failed: User not found and Invalid Recovery Code", text_color="red").grid(row=3, column=0, columnspan=2, pady=(0,10))
    else:
        for widget in app.winfo_children():
            widget.destroy()

        ctk.CTkButton(app, text="Back", width=60, height=28, fg_color="#0078D7", hover_color="#005A9E", command=app.create_widgets).grid(row=0, column=0, padx=10, pady=10, sticky="w")   
        ctk.CTkLabel(
            app,
            text="Set New Password",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="center",
            justify="center"
        ).grid(row=0, column=1, columnspan=2, pady=10, sticky="nw")
        ctk.CTkLabel(app, text="New Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        new_password_entry = ctk.CTkEntry(app, show="*", width=180)
        new_password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w") 
        ctk.CTkLabel(app, text="Confirm New Password:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        confirm_new_password_entry = ctk.CTkEntry(app, show="*", width=180)
        confirm_new_password_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        submit_btn = ctk.CTkButton(
            app, 
            text="Submit", 
            width=100, 
            state="disabled",
            command=lambda: handle_new_password_submission(
                app,
                new_password_entry.get(),
                confirm_new_password_entry.get()
            )
        )
        submit_btn.grid(row=5, column=0, columnspan=2, pady=20)

        def validate_fields(*args):
            if (
                new_password_entry.get().strip() and
                confirm_new_password_entry.get().strip()
            ):
                submit_btn.configure(state="normal")
            else:
                submit_btn.configure(state="disabled")

        new_password_entry.bind("<KeyRelease>", validate_fields)
        confirm_new_password_entry.bind("<KeyRelease>", validate_fields)

def handle_new_password_submission(app, new_password, confirm_new_password):
    if hash(new_password) != hash(confirm_new_password):
        ctk.CTkLabel(app, text="Password Reset Failed: Passwords do not match", text_color="red").grid(row=3, column=0, columnspan=2, pady=(0,10))
    else:
        for widget in app.winfo_children():
            widget.destroy()
        ctk.CTkLabel(app, text="Password Reset Successful! Please login with your new password.").grid(row=0, column=0, columnspan=2, pady=(30, 10))
        ctk.CTkButton(app, text="Back to Login", width=120, command=app.create_widgets).grid(row=1, column=0, columnspan=2, pady=20)

import customtkinter as ctk
import tkinter as tk
from UI.components.clear_contents import clear_contents
from UI.pages.event_details_page import view_event_details, accept_invite, decline_invite

@clear_contents
def show_invites(app):
# Hard Coded Event Invitess TODO: Wait for backend implementation
    print("user_id:", app.user_id)
    invites_frame = ctk.CTkScrollableFrame(app, width=450, height=400)
    invites_frame.place(relx=0.5, rely=0.5, anchor="center")
    ctk.CTkLabel(app, text="Invited Events", font=("Arial", 18, "bold")).pack(pady=20)

    for invite in app.invites:
        frame = ctk.CTkFrame(invites_frame)
        frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            frame,
            text=invite["name"],
            anchor="w",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            frame,
            text=invite["description"],
            wraplength=450,
            justify="left",
            anchor="w"
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            frame,
            text=f"Location: {invite['room_id']}",
            anchor="w"
        ).pack(anchor="w", padx=10, pady=(5, 10))

        button_row = ctk.CTkFrame(frame, fg_color=frame.cget("fg_color"))
        button_row.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(button_row, text="").pack(side="left", expand=True)

        ctk.CTkButton(
            button_row,
            text="Accept",
            width=100,
            height=28,
            fg_color="#33cc33",
            hover_color="#00cc00",
            command=lambda id=invite["id"]: accept_invite(app, id)
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_row,
            text="Decline",
            width=100,
            height=28,
            fg_color="#cc3333",
            hover_color="#990000",
            command=lambda id=invite["id"]: decline_invite(app, id)
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_row,
            text="View More",
            width=100,
            height=28,
            fg_color="#0078D7",
            hover_color="#005A9E",
            command=lambda id=invite["id"]: view_event_details(app, id, caller="invites")
        ).pack(side="right", padx=5)

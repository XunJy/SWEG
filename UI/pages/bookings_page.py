import customtkinter as ctk
import requests
from UI.components.clear_contents import clear_contents
from UI.pages.event_details_page import view_event_details, cancel_booking

@clear_contents
def show_my_bookings(app):
    events_frame = ctk.CTkScrollableFrame(app, width=450, height=400)
    events_frame.place(relx=0.5, rely=0.5, anchor="center")
    ctk.CTkLabel(app, text="My Bookings", font=("Arial", 18, "bold")).pack(pady=20)

    try:
        booking_refs = requests.get(
            f"http://127.0.0.1:8000/users/{app.user_id}/bookings"
        ).json()
    except requests.RequestException:
        ctk.CTkLabel(events_frame, text="Failed to load bookings.").pack(pady=20)
        return

    if not booking_refs:
        ctk.CTkLabel(events_frame, text="No bookings found.").pack(pady=20)
        return

    for ref in booking_refs:
        booking_id = ref.get("booking_id")
        if not booking_id:
            continue
        try:
            booking = requests.get(f"http://127.0.0.1:8000/bookings/{booking_id}").json()
        except requests.RequestException:
            continue

        name = booking.get("name")
        description = booking.get("description")
        room_id = booking.get("room_id")

        frame = ctk.CTkFrame(events_frame)
        frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame, text=name, anchor="w", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        ctk.CTkLabel(frame, text=description, wraplength=450, justify="left", anchor="w").pack(anchor="w", padx=10)

        button_row = ctk.CTkFrame(frame, fg_color=frame.cget("fg_color"))
        button_row.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(button_row, text=f"Location: {room_id}", anchor="w").pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            button_row,
            text="View More",
            width=100,
            height=28,
            fg_color="#0078D7",
            hover_color="#005A9E",
            command=lambda id=booking_id: view_event_details(app, id, caller="bookings")
        ).pack(side="right", padx=5)
        ctk.CTkButton(
            button_row,
            text="Cancel Booking",
            width=100,
            height=28,
            fg_color="#cc3333",
            hover_color="#990000",
            command=lambda id=booking_id: cancel_booking(app, id)
        ).pack(side="right", padx=5)
import customtkinter as ctk
import requests
from UI.components.clear_contents import clear_contents
from UI.components.theme import apply_datepicker_theme
from UI.pages.bookings_page import show_my_bookings

# https://stackoverflow.com/questions/26902034/how-to-center-a-tkinter-widget-in-a-sticky-frame
@clear_contents
def select_time_slot(app, caller, start_time, end_time, room_id=None):
    back_button = ctk.CTkButton(app, text="Back", width=60, height=28, fg_color="#0078D7", hover_color="#005A9E")
    if caller == "timeslots":
        back_button.configure(command=lambda: back_button_to_booking_room(app))
    else:
        back_button.configure(command=lambda: back_button_to_booking_date(app))
    back_button.pack(padx=55, pady=(10, 10), anchor="w")

    app.pending_booking = {
        "room_id": room_id,
        "start_time": start_time,
        "end_time": end_time,
    }

    form_frame = ctk.CTkFrame(app, fg_color="transparent")
    form_frame.pack(pady=10)

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(form_frame, text="Booking Title:").grid(
        row=0, column=0, padx=10, pady=5, sticky="e"
    )
    app.title_entry = ctk.CTkEntry(form_frame, width=250)
    app.title_entry.grid(
        row=0, column=1, padx=10, pady=5, sticky="w"
    )

    ctk.CTkLabel(form_frame, text="Booking Description:").grid(
        row=1, column=0, padx=10, pady=5, sticky="e"
    )
    app.description_entry = ctk.CTkEntry(form_frame, width=250)
    app.description_entry.grid(
        row=1, column=1, padx=10, pady=5, sticky="w"
    )

    app.submit_button = ctk.CTkButton(form_frame, text="Submit", command=lambda: submit_booking(app))
    app.submit_button.grid(
        row=2, column=0, columnspan=2, pady=20
    )

def back_button_to_booking_room(app):
    from UI.pages.booking_by_room import show_booking_room

    show_booking_room(app)

def back_button_to_booking_date(app):
    from UI.pages.booking_by_date import show_booking_date
    show_booking_date(app)
    apply_datepicker_theme(app)


def submit_booking(app):
    notification_screen = ctk.CTkToplevel(app)
    notification_screen.geometry("300x200")
    notification_screen.title("University Room Booking System - Notification")
    button = ctk.CTkButton(notification_screen, text="OK", command=notification_screen.destroy)

    if app.title_entry.get() == "":
        ctk.CTkLabel(notification_screen, text="Booking Failed! Title is required.").pack(pady=20)
    elif app.description_entry.get() == "":
        ctk.CTkLabel(notification_screen, text="Booking Failed! Description is required.").pack(pady=20)
    elif not getattr(app, "pending_booking", None):
        ctk.CTkLabel(notification_screen, text="Booking Failed! No slot selected.").pack(pady=20)
    else:
        booking_details = {
            "room_id": app.pending_booking.get("room_id"),
            "start_time": app.pending_booking.get("start_time"),
            "end_time": app.pending_booking.get("end_time"),
            "name": app.title_entry.get(),
            "description": app.description_entry.get(),
            "public": True,
        }
        try:
            response = requests.post("http://127.0.0.1:8000/bookings", json=booking_details)
            response.raise_for_status()
            booking = response.json()
            requests.post(
                "http://127.0.0.1:8000/user-bookings",
                json={
                    "user_id": getattr(app, "user_id", ""),
                    "booking_id": booking.get("booking_id"),
                    "organiser": True,
                },
            )
            ctk.CTkLabel(notification_screen, text="Booking Successful!").pack(pady=20)
            button.configure(command=lambda: handle_close_booking(app, True, notification_screen))
        except requests.HTTPError as e:
            error_text = e.response.json().get("detail", "Booking Failed!") if e.response is not None else "Booking Failed!"
            ctk.CTkLabel(notification_screen, text=error_text).pack(pady=20)
        except requests.RequestException:
            ctk.CTkLabel(notification_screen, text="Booking Failed! Network error.").pack(pady=20)
    button.pack(pady=10)
    notification_screen.focus_force()
    notification_screen.attributes("-topmost", True)
    notification_screen.after(1000, lambda: notification_screen.attributes("-topmost", False))

def handle_close_booking(app, success, notification_screen):
    notification_screen.destroy()
    if success:
        show_my_bookings(app)

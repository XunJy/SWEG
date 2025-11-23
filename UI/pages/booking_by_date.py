import customtkinter as ctk
import tkinter as tk
import tkcalendar
import datetime
import requests
from UI.components.clear_contents import clear_contents
from UI.pages.booking_submit import select_time_slot
from UI.components.theme import apply_datepicker_theme

# Reimplemented https://pythonguides.com/create-date-time-picker-using-python-tkinter in customtkinter
@clear_contents
def show_booking_date(app):
    ctk.CTkLabel(app, text="Room Booking", font=("Arial", 18, "bold")).pack(pady=20)
    ctk.CTkLabel(app, text="Please select a date:").pack(pady=(0, 10))

    app.date_picker = tkcalendar.DateEntry(app, width=15, height=15)
    apply_datepicker_theme(app)
    app.date_picker.pack(pady=(0, 20))
    ctk.CTkLabel(app, text="Select Time:", font=("Arial", 14)).pack(pady=(10, 5))

    time_frame = ctk.CTkFrame(app, fg_color="transparent")
    time_frame.pack(pady=5)

    hour_var = tk.StringVar(value="12")
    minute_var = tk.StringVar(value="00")
    ampm_var = ctk.StringVar(value="AM")

    app.hour_spin = ctk.CTkComboBox(time_frame, values=[f"{h}" for h in range(1, 13)], variable=hour_var)
    app.hour_spin.set("12")
    app.hour_spin.pack(side="left", padx=(0, 5))

    ctk.CTkLabel(time_frame, text=":", font=("Arial", 14)).pack(side="left")

    app.minute_spin = ctk.CTkComboBox(time_frame, values=[f"{m:02d}" for m in range(0, 60, 15)], variable=minute_var)
    app.minute_spin.set("00")
    app.minute_spin.pack(side="left", padx=(5, 0))

    ampm_menu = ctk.CTkOptionMenu(time_frame, values=["AM", "PM"], variable=ampm_var, width=70)
    ampm_menu.pack(side="left", padx=(10, 0))

    ctk.CTkButton(app, text="Search", command=lambda: handle_search()).pack(pady=(10, 0))

    ctk.CTkLabel(app, text="Select a Room:", font=("Arial", 14)).pack(pady=(20, 5))

    app.rooms_frame = ctk.CTkScrollableFrame(app, width=450, height=300)
    app.rooms_frame.pack(pady=10)

    def handle_room_click(selected_room, start_time, end_time):
        select_time_slot(app, "date", start_time, end_time, selected_room)

    def handle_search():
        for child in app.rooms_frame.winfo_children():
            child.destroy()

        date = app.date_picker.get_date()
        hour = int(app.hour_spin.get())
        minute = int(app.minute_spin.get())
        ampm = ampm_var.get()

        if ampm == "PM" and hour != 12:
            hour += 12
        if ampm == "AM" and hour == 12:
            hour = 0

        start_datetime = datetime.datetime.combine(date, datetime.time(hour=hour, minute=minute))
        end_datetime = start_datetime + datetime.timedelta(hours=1)

        start_time = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        end_time = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            available_rooms = requests.get(
                "http://127.0.0.1:8000/rooms/available",
                params={"start_time": start_time, "end_time": end_time}
            ).json()
        except requests.RequestException:
            ctk.CTkLabel(app.rooms_frame, text="Failed to load rooms.").pack(pady=20)
            return

        if not available_rooms:
            ctk.CTkLabel(app.rooms_frame, text="No rooms available for this time.").pack(pady=20)
            return

        for room in available_rooms:
            frame = ctk.CTkFrame(app.rooms_frame)
            frame.pack(fill="x", padx=10, pady=10)

            room_label = f"Room {room['number']} ({room['building']}) - Capacity {room['capacity']}"
            ctk.CTkLabel(frame, text=room_label, anchor="w").pack(anchor="w", padx=10, pady=(10, 5))

            ctk.CTkButton(
                frame,
                text="Book This Room",
                width=160,
                command=lambda r=room["room_id"], s=start_time, e=end_time: handle_room_click(r, s, e)
            ).pack(pady=(0, 10), anchor="e")

    handle_search()

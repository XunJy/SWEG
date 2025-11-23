import customtkinter as ctk
import tkcalendar
import datetime
import requests
from UI.components.clear_contents import clear_contents
from UI.pages.booking_submit import select_time_slot
from UI.components.theme import apply_calendar_theme

@clear_contents
def show_booking_room(app):
    ctk.CTkLabel(app, text="Room Booking", font=("Arial", 18, "bold")).pack(pady=20)
    ctk.CTkLabel(app, text="Please select a room:").pack(pady=(0,10))
    try:
        rooms = requests.get("http://127.0.0.1:8000/rooms").json()
    except requests.RequestException:
        rooms = []

    options = []
    app.room_options = {}
    for room in rooms:
        label = f"Room {room['number']} ({room['building']})"
        options.append(label)
        app.room_options[label] = room["room_id"]

    app.room_select = ctk.CTkOptionMenu(
        app,
        values=["Select a room"] + options,
        width=200,
        command=lambda value: on_room_selected(app, value)
    )
    app.room_select.pack(pady=(0,20))
    app.room_select.set("Select a room")

    app.calander = tkcalendar.Calendar(app, selectmode='day', mindate=datetime.date.today(), font=("Arial", 14))
    app.calander.selection_set(date=datetime.date.today())
    app.calander.config(state="disabled")

def on_room_selected(app, value):
    room_id = app.room_options.get(value)
    if room_id:
        app.calander.place(relx=0.5, rely=0.5, anchor="e")
        app.calander.config(state="normal")
        app.calander.bind("<<CalendarSelected>>", lambda ev, cal=app.calander: on_calendar_selected(app, ev, cal, room_id))
        apply_calendar_theme(app)
        if hasattr(app, 'time_slots_frame') and app.time_slots_frame is not None:
            app.time_slots_frame.destroy()
        app.time_slots_frame = ctk.CTkFrame(app, width=200, height=300)
        app.time_slots_frame.place(relx=0.5, rely=0.5, anchor="w")
        show_time_slots_for_date(app, room_id, datetime.date.today())

def on_calendar_selected(app, event, cal_widget, room_id):
    try:
        selected_date = cal_widget.selection_get()
    except Exception:
        selected_date = datetime.date.today()
    show_time_slots_for_date(app, room_id, selected_date)


def show_time_slots_for_date(app, room_id, date):
    if not hasattr(app, 'time_slots_frame') or app.time_slots_frame is None:
        app.time_slots_frame = ctk.CTkFrame(app, width=200, height=300)
        app.time_slots_frame.place(relx=0.5, rely=0.5, anchor="w")

    for child in app.time_slots_frame.winfo_children():
        child.destroy()

    header = ctk.CTkLabel(app.time_slots_frame, text=f"Slots for {date.isoformat()}")
    header.pack(pady=(8, 6))

    try:
        availability = requests.get(
            f"http://127.0.0.1:8000/rooms/{room_id}/availability/day",
            params={"date": date.strftime("%Y-%m-%d")}
        ).json()
        slots = availability.get("availability", [])
    except requests.RequestException:
        slots = []

    if not slots:
        ctk.CTkLabel(app.time_slots_frame, text="Unable to load availability.").pack(pady=10)
        return

    for slot in slots:
        slot_text = slot.get("slot")
        is_available = slot.get("available", False)
        if not slot_text:
            continue
        start_str, end_str = [s.strip() for s in slot_text.split("-")]
        start_time = f"{date.strftime('%Y-%m-%d')} {start_str}"
        end_time = f"{date.strftime('%Y-%m-%d')} {end_str}"

        btn = ctk.CTkButton(
            app.time_slots_frame,
            text=slot_text,
            width=160,
            height=30,
            state="normal" if is_available else "disabled",
            command=lambda s=start_time, e=end_time: select_time_slot(app, "timeslots", s, e, room_id=room_id)
        )
        btn.pack(padx=10, pady=4)

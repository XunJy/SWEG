import customtkinter as ctk
import requests
from UI.components.clear_contents import clear_contents


def _render_events_list(app, parent_frame, events, caller):
    from UI.pages.event_details_page import view_event_details

    if not events:
        ctk.CTkLabel(parent_frame, text="No events available.").pack(pady=20)
        return

    for event in events:
        booking_id = event.get("booking_id")
        name = event.get("name", "Unnamed Event")
        description = event.get("description", "")
        room_id = event.get("room_id", "-")

        frame = ctk.CTkFrame(parent_frame)
        frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame, text=name, anchor="w", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        ctk.CTkLabel(frame, text=description, wraplength=450, justify="left", anchor="w").pack(anchor="w", padx=10)
        row = ctk.CTkFrame(frame, fg_color=frame.cget("fg_color"))
        row.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(row, text=f"Location: {room_id}", anchor="w").pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            row,
            text="View More",
            width=100,
            height=28,
            fg_color="#0078D7",
            hover_color="#005A9E",
            command=lambda bid=booking_id: view_event_details(app, bid, caller=caller)
        ).pack(side="right")


@clear_contents
def show_events(app):
    events_frame = ctk.CTkScrollableFrame(app, width=450, height=400)
    events_frame.place(relx=0.5, rely=0.5, anchor="center")
    ctk.CTkLabel(app, text="Available Events", font=("Arial", 18, "bold")).pack(pady=20)

    try:
        response = requests.get(
            "http://127.0.0.1:8000/bookings/public",
            params={"user_id": getattr(app, "user_id", "")}
        )
        response.raise_for_status()
        events = response.json()
    except requests.RequestException:
        ctk.CTkLabel(events_frame, text="Failed to load events. Please try again.").pack(pady=20)
        return

    _render_events_list(app, events_frame, events, caller="events")


@clear_contents
def show_my_events(app):
    events_frame = ctk.CTkScrollableFrame(app, width=450, height=400)
    events_frame.place(relx=0.5, rely=0.5, anchor="center")
    ctk.CTkLabel(app, text="My Events", font=("Arial", 18, "bold")).pack(pady=20)

    try:
        booking_refs = requests.get(
            f"http://127.0.0.1:8000/users/{app.user_id}/bookings"
        ).json()
    except requests.RequestException:
        ctk.CTkLabel(events_frame, text="Failed to load your events.").pack(pady=20)
        return

    organiser_bookings = []
    for ref in booking_refs:
        if not ref.get("organiser"):
            continue
        booking_id = ref.get("booking_id")
        if not booking_id:
            continue
        try:
            booking = requests.get(f"http://127.0.0.1:8000/bookings/{booking_id}").json()
            organiser_bookings.append(booking)
        except requests.RequestException:
            continue

    _render_events_list(app, events_frame, organiser_bookings, caller="bookings")

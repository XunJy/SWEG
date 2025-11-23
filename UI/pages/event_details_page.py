import customtkinter as ctk
import requests
from UI.components.clear_contents import clear_contents


@clear_contents
def view_event_details(app, booking_id, caller, invite_id=None):
    from UI.pages.events_page import show_events
    from UI.pages.invites_page import show_invites
    from UI.pages.bookings_page import show_my_bookings

    back_button = ctk.CTkButton(app, text="Back", width=60, height=28, fg_color="#0078D7", hover_color="#005A9E")
    if caller == "events":
        back_button.configure(command=lambda: show_events(app))
    elif caller == "invites":
        back_button.configure(command=lambda: show_invites(app))
    elif caller == "bookings":
        back_button.configure(command=lambda: show_my_bookings(app))
    back_button.pack(padx=55, pady=(10, 10), anchor="w")

    try:
        event = requests.get(f"http://127.0.0.1:8000/bookings/{booking_id}").json()
    except requests.RequestException:
        event = None

    if event is None:
        ctk.CTkLabel(app, text="Event not found").pack(pady=(10, 20))
        ctk.CTkButton(app, text="Back to Events", width=100, height=28, command=lambda: show_events(app)).pack(pady=(10, 10))
    else:
        ctk.CTkLabel(app, text=event['name']).pack(pady=(10, 10))
        ctk.CTkLabel(app, text=event.get('description', "")).pack(pady=(0, 20))
        ctk.CTkLabel(app, text=f"Location: {event['room_id']}").pack(pady=(0, 10))
        ctk.CTkLabel(app, text=f"Start Time: {event['start_time']}").pack(pady=(0, 10))
        ctk.CTkLabel(app, text=f"End Time: {event['end_time']}").pack(pady=(0, 20))

        if caller == "events":
            ctk.CTkButton(
                app,
                text="Join Event",
                width=120,
                height=28,
                fg_color="#33cc33",
                hover_color="#00cc00",
                command=lambda bid=booking_id: join_public_event(app, bid)
            ).pack(padx=10, pady=(10, 10), anchor="e")

        if caller == "invites" and invite_id:
            ctk.CTkButton(
                app,
                text="Accept",
                width=100,
                height=28,
                fg_color="#33cc33",
                hover_color="#00cc00",
                command=lambda: accept_invite(app, invite_id, booking_id)
            ).pack(padx=10, pady=(10, 10), anchor="e")
            ctk.CTkButton(
                app,
                text="Decline",
                width=100,
                height=28,
                fg_color="#cc3333",
                hover_color="#990000",
                command=lambda: decline_invite(app, invite_id, booking_id)
            ).pack(padx=10, pady=(10, 10), anchor="e")

        if caller == "bookings":
            ctk.CTkButton(
                app,
                text="Cancel Booking",
                width=120,
                height=28,
                fg_color="#cc3333",
                hover_color="#990000",
                command=lambda: cancel_booking(app, booking_id)
            ).pack(padx=10, pady=(10, 10), anchor="e")


def accept_invite(app, invite_id, booking_id):
    try:
        requests.put(f"http://127.0.0.1:8000/invites/{invite_id}/status/accept")
        requests.post(
            "http://127.0.0.1:8000/user-bookings",
            json={"user_id": getattr(app, "user_id", ""), "booking_id": booking_id, "organiser": False},
        )
    except requests.RequestException:
        show_notification(app, "Invite Acceptance Failed")
        return

    show_notification(app, "Invite Accepted Successfully!", refresh="invites")


def decline_invite(app, invite_id, booking_id):
    try:
        requests.put(f"http://127.0.0.1:8000/invites/{invite_id}/status/decline")
    except requests.RequestException:
        show_notification(app, "Invite Decline Failed")
        return

    show_notification(app, "Invite Declined!", refresh="invites")


def join_public_event(app, booking_id):
    try:
        requests.post(
            "http://127.0.0.1:8000/user-bookings",
            json={"user_id": getattr(app, "user_id", ""), "booking_id": booking_id, "organiser": False},
        )
    except requests.RequestException:
        show_notification(app, "Unable to join event")
        return

    show_notification(app, "Joined event successfully!", refresh="events")


def cancel_booking(app, booking_id):
    request = requests.delete(f"http://127.0.0.1:8000/bookings/{booking_id}")
    if request.status_code != 200:
        show_notification(app, "Booking Cancellation Failed")
    else:
        show_notification(app, "Booking Cancelled Successfully!", refresh="bookings")


def show_notification(app, message, refresh=None):
    from UI.pages.events_page import show_events
    from UI.pages.invites_page import show_invites
    from UI.pages.bookings_page import show_my_bookings

    notification_screen = ctk.CTkToplevel(app)
    notification_screen.geometry("300x150")
    notification_screen.title("Notification")
    ctk.CTkLabel(notification_screen, text=message).pack(pady=20)

    def close_and_refresh():
        notification_screen.destroy()
        if refresh == "events":
            show_events(app)
        elif refresh == "invites":
            show_invites(app)
        elif refresh == "bookings":
            show_my_bookings(app)

    ctk.CTkButton(notification_screen, text="OK", command=close_and_refresh).pack(pady=20)
    notification_screen.focus_force()
    notification_screen.attributes("-topmost", True)
    notification_screen.after(1000, lambda: notification_screen.attributes("-topmost", False))
    

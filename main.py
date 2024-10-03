import time
from uptime import get_uptime, format_uptime
from notify import notify_uptime
from system_tray import setup_tray_icon  
import threading
days = 14

def check_uptime_threshold(threshold_days=days):
    while True:
        # Get the uptime
        uptime_seconds = get_uptime()

        # Check if the uptime exceeds the threshold
        if uptime_seconds >= threshold_days * 24 * 3600:
            # Format the uptime message
            uptime_message = (
                f"System Uptime: {format_uptime(uptime_seconds)}\n"
                f"Your system has been running for more than {days} days!\n"
                "You should consider rebooting your computer!"
            )
            # Show the toast notification
            notify_uptime(uptime_message)

            # Wait for a while before checking again to avoid multiple notifications
            time.sleep(60 * 60)  # Check every 10 minutes
        else:
            # Sleep for a shorter interval if under the threshold
            time.sleep(60 * 60 * 10)  # Check every minute

if __name__ == "__main__":
    # Start the system tray icon in a separate thread
    tray_thread = threading.Thread(target=setup_tray_icon, daemon=True)
    tray_thread.start()

    # Start monitoring the uptime
    check_uptime_threshold()

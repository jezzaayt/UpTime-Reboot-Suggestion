from plyer import notification
from uptime import get_uptime, format_uptime
from notify import notify_uptime
from system_tray import setup_tray_icon  
import threading
import platform
import logging
import time
import os

# Setup basic logging
logging.basicConfig(filename="uptime_monitor.log", level=logging.INFO, format='%(asctime)s - %(message)s')



# Days
def get_threshold_days():
    print("e")
    file_path = "./day.txt"
    if os.path.exists(file_path):
        print("e")
        try:
            with open(file_path, "r") as file:
                days = int(file.read().strip())  # Read and strip any extra whitespace
                notification.notify(
                title="Uptime Monitor",
                message=f"Using threshold: {days} days",
                timeout=5
                )
                return days
        except Exception as e:
            print("error reading")
            notification.notify(
                title="Uptime Monitor",
                message=f"Error reading day.txt. Defaulting to 14 days. Error: {str(e)}",
                timeout=5
            )
            return 14
    else:
        notification.notify(
            title="Uptime Monitor",
            message="Day.txt not found. Defaulting to 14 days.",
            timeout=5
        )
        return 14




def check_uptime_threshold(threshold_days):
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
            # Log the uptime message
            logging.info(f"Uptime exceeds {days} days: {format_uptime(uptime_seconds)}")
            # Wait for a while before checking again to avoid multiple notifications
            time.sleep(60 * 60 * 6)
            
        else:
            # Sleep for a shorter interval if under the threshold
            time.sleep(3600)  # Check every minute
            logging.info(f"Current Uptime: {format_uptime(uptime_seconds)}")   

            


if __name__ == "__main__":
    threshold_days = get_threshold_days()

    # Start the system tray icon in a separate thread
    if platform.system() == "Windows":
        tray_thread = threading.Thread(target=setup_tray_icon, daemon=True)
        tray_thread.start()
        # As laziness on Linux currently... will need to get a VM instance at some point of time to test this and create tray for Linux if necessary

    # Start monitoring the uptime
    check_uptime_threshold(threshold_days)

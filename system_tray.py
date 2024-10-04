import time
import pystray
from pystray import MenuItem as item
from pystray import Menu, Icon, MenuItem
from PIL import Image, ImageDraw
from datetime import datetime
import threading
import psutil

# Load your custom icon (make sure the path to the image is correct)
def load_icon_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Error loading icon: {e}")
        return None

# Define system tray logic
def setup_tray_icon():
    # Specify the path to your custom icon image
    icon_image_path = "./icon.png"  # Replace with your icon image path

    icon_image = load_icon_image(icon_image_path)
    print(icon_image.filename)
    if not icon_image:
        return  # Exit if the icon couldn't be loaded

    # Create the system tray icon
    icon = Icon("Uptime Monitor", icon_image, menu=Menu(
        MenuItem("Show Last Uptime Check", show_uptime),
        MenuItem("Quit", on_quit)
    ))
    threading.Thread(target=update_tooltip, args=(icon,), daemon=True).start()
    icon.run()

def show_uptime(icon, item):
    print(f"Last checked uptime at: {time.ctime()}")


# Function to calculate system uptime
def get_uptime():
    return time.time() - psutil.boot_time()

# Function to format uptime into human-readable form
def format_uptime(seconds):
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    return f"{int(days)}d {int(hours)}h {int(minutes)}m"



# Function to update the tooltip with uptime and refresh time
def update_tooltip(icon):
    while True:
        uptime_seconds = get_uptime()
        uptime = format_uptime(uptime_seconds)
        last_refreshed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        icon.title = f"Uptime: {uptime}\nLast Refreshed: {last_refreshed}"
        time.sleep(6 * 3600)  # Refresh every 6 hours

# Function to stop the tray icon
def on_quit(icon, item):
    icon.stop()


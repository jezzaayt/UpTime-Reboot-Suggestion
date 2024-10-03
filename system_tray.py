import time
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from datetime import datetime
import threading
import psutil

# Function to calculate system uptime
def get_uptime():
    return time.time() - psutil.boot_time()

# Function to format uptime into human-readable form
def format_uptime(seconds):
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    return f"{int(days)}d {int(hours)}h {int(minutes)}m"

# Create an icon for the system tray
def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

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

# Main function to set up the system tray icon
def setup_tray_icon():
    # Create the system tray icon with a custom image
    icon_image = create_image(64, 64, 'black', 'Orange')
    icon = pystray.Icon("uptime_tracker", icon_image, menu=pystray.Menu(
        item('End', on_quit)
    ))

    # Start the background thread for updating the tooltip
    threading.Thread(target=update_tooltip, args=(icon,), daemon=True).start()

    # Run the system tray icon
    icon.run()

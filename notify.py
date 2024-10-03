from plyer import notification

def notify_uptime(uptime_message):
    notification.notify(
        title="Consider Rebooting",
        message=uptime_message.replace('\n', '\n'),  # Ensures newline characters are respected
        timeout=10  # 10 seconds notification
    )

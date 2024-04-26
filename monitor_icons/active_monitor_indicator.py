import time
import win32gui
import win32api
from win10toast import ToastNotifier
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageFont

def get_active_monitor():
    # Get the handle of the window that currently has focus
    active_window = win32gui.GetForegroundWindow()

    # Get the display number of all monitors
    monitor_info = win32api.EnumDisplayMonitors(None, None)
    monitor_devices = {}
    for idx, monitor in enumerate(monitor_info, start=1):
        monitor_handle = monitor[0]
        monitor_name = win32api.GetMonitorInfo(monitor_handle).get("Device")
        monitor_devices[monitor_name] = idx

    # Get the display number of the active monitor
    active_monitor_name = win32api.GetMonitorInfo(win32api.MonitorFromWindow(active_window)).get("Device")
    active_monitor_number = monitor_devices.get(active_monitor_name, 0)

    return active_monitor_number

# Create a toast notifier object
toaster = ToastNotifier()

# Create a function to update the system tray icon
def update_icon(icon):
    active_monitor = get_active_monitor()
    icon.title = f"Active Monitor: {active_monitor}"
    icon.icon = Image.open(f"monitor_icons/monitor_{active_monitor}.png")

# Create a function to exit the program
def exit_program(icon, item):
    icon.stop()

# Create a system tray icon
image = Image.open("monitor_icons/monitor_1.png")  # Default icon
menu = (item("Exit", exit_program),)
icon = pystray.Icon("Active Monitor", image, "Active Monitor", menu)

# Start a timer to update the system tray icon periodically
def timer_update_icon():
    while True:
        update_icon(icon)
        time.sleep(0.5)  # Update every 0.5 seconds

# Start the timer in a separate thread
import threading
threading.Thread(target=timer_update_icon, daemon=True).start()

# Run the system tray icon
icon.run()

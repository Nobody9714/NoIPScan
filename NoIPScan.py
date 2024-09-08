import sys
import subprocess
import importlib

def check_and_install_dependencies():
    required_modules = {
        'tkinter': 'python3-tk',
        'PIL': 'pillow',
        'netifaces': 'netifaces',
        'getmac': 'getmac',
        'aiohttp': 'aiohttp'
    }

    missing_modules = []

    for module, package in required_modules.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append((module, package))

    if missing_modules:
        print("The following dependencies are missing:")
        for module, package in missing_modules:
            print(f"- {module}")
        
        install = input("Do you want to install the missing dependencies? (y/n): ").lower()
        if install == 'y':
            for module, package in missing_modules:
                print(f"Installing {package}...")
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    print(f"{package} installed successfully.")
                except subprocess.CalledProcessError:
                    print(f"Failed to install {package}. Please install it manually.")
                    sys.exit(1)
        else:
            print("Exiting. The script requires all dependencies to run.")
            sys.exit(1)

    print("All dependencies are installed.")

# Call the function to check and install dependencies
check_and_install_dependencies()

# Rest of your existing imports
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, font
import socket
import ipaddress
import time
import webbrowser
import platform
import ctypes
import base64
from io import BytesIO
import queue
import asyncio
import aiohttp
from PIL import Image, ImageTk
import netifaces
from getmac import get_mac_address
from asyncio import Lock
from collections import defaultdict

RATE_LIMIT = 1.5
last_request_time = 0
rate_limit_lock = Lock()
vendor_lock = threading.Lock()
devices = []
stop_event = threading.Event()
result_queue = queue.Queue()

donation_options = [
    {
        "name": "Donation Wallets",
        "image": "awsfawf",
        "description": "No donation necessary. But if you do, please only donate in the native coin or the token of the DePIN project you got this program from. Thank you."
    },
    {
        "name": "Monaro (XMR)",
        "image": "sdsf",
        "description": "46ReDpJp11aG3rDfR5dprQQdYfaCuZxXHgqpGhV6zWJUaG8RAuL8zcH2aSht73z6oFYzpNAuwUJVeAe4fD61Q7vAKmjdZjr"
    },
    {
        "name": "Polygon (MATIC)",
        "image": "sdsf",
        "description": "0x185Cf68c8A69c6b22De3D531B339B5D362067304"
    },
    {
        "name": "Solona (SOL)",
        "image": "sdsf",
        "description": "Ccz6zf12AJB1xweDZ3SHhfJB9VgLxL52iLKjtzHL2nSb"
    },
]

class AsyncioThread(threading.Thread):
    def __init__(self, loop):
        super().__init__(daemon=True)
        self.loop = loop

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.timer = None  # Initialize the timer attribute
        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.unschedule)

    def schedule(self, event=None):
        self.unschedule()
        self.timer = self.widget.after(500, self.show)

    def unschedule(self, event=None):
        if self.timer:
            self.widget.after_cancel(self.timer)
            self.timer = None
        self.hide()

    def show(self):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def set_icon_from_base64(window, base64_string):
    try:
        icon_data = base64.b64decode(base64_string)
        icon_image = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        window.iconphoto(True, icon_photo)
    except Exception as e:
        print(f"Error setting icon: {e}")

def get_network_info():
    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET][0]
    
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface).get(netifaces.AF_INET, [])
        for addr in addrs:
            ip = addr.get('addr')
            if ip and ipaddress.IPv4Address(default_gateway) in ipaddress.IPv4Network(f"{ip}/24", strict=False):
                return str(default_gateway), '.'.join(ip.split('.')[:3])
    
    return None, None

def ping(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    return subprocess.call(['ping', param, '1', '-w', '100', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

async def get_mac_vendor(mac_address, existing_vendor):
    global last_request_time
    
    if disable_mac_lookup_var.get():
        return "Lookup Disabled"
    
    if existing_vendor not in ["Unknown", "Rate limit exceeded", "Lookup Disabled"]:
        return existing_vendor
    
    async with rate_limit_lock:
        current_time = time.time()
        time_since_last_request = current_time - last_request_time
        
        if time_since_last_request < RATE_LIMIT:
            await asyncio.sleep(RATE_LIMIT - time_since_last_request)
        
        last_request_time = time.time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.macvendors.com/{mac_address}", timeout=5) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 429:
                    return "Rate limit exceeded"
                else:
                    return "Unknown"
    except asyncio.TimeoutError:
        return "Timeout"
    except Exception as e:
        return f"Error: {str(e)}"

async def scan_device(ip):
    if await asyncio.to_thread(ping, ip):
        mac = await asyncio.to_thread(get_mac_address, ip=ip) or "N/A"
        device_name = await asyncio.to_thread(get_device_name, ip)
        existing_vendor = next((d["Vendor"] for d in devices if d["IP Address"] == ip), "Unknown")
        vendor = await get_mac_vendor(mac, existing_vendor) if mac != "N/A" else "Unknown"
        return {"Device Name": device_name, "Vendor": vendor, "IP Address": ip, "MAC": mac, "Hidden MAC": False}
    return None

def get_device_name(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        if platform.system() == "Windows":
            try:
                output = subprocess.check_output(f"nbtstat -A {ip}", shell=True).decode('utf-8', errors='ignore')
                return next((line.split()[0].strip() for line in output.splitlines() if '<00>' in line), "Unknown")
            except:
                pass
    return "Unknown"

async def perform_multiple_scans():
    try:
        num_scans = min(int(num_scans_entry.get()), 10)
        total_progress = num_scans * 100
        current_progress = 0
        for scan_number in range(1, num_scans + 1):
            if stop_event.is_set():
                break
            await perform_scan(scan_number)
            current_progress += 100
            progress_var.set((current_progress / total_progress) * 100)
            root.update_idletasks()
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error in perform_multiple_scans: {e}")
    finally:
        progress_var.set(100)
        root.update_idletasks()
        root.after(0, lambda: scan_button.config(text="Scan Network", command=start_scan))
        root.after(0, lambda: status_label.config(text=f"Scan {'complete' if not stop_event.is_set() else 'stopped by user'}. Found {len(tree.get_children())} devices."))

async def perform_scan(scan_number):
    network_address = network_entry.get()
    start_range, end_range = map(int, [start_range_entry.get(), end_range_entry.get()])
    
    ip_list = [f"{network_address}.{i}" for i in range(start_range, end_range + 1)]
    total_ips = len(ip_list)

    tasks = [scan_device(ip) for ip in ip_list]
    for i, task in enumerate(asyncio.as_completed(tasks)):
        if stop_event.is_set():
            break
        try:
            result = await task
            if result:
                result_queue.put(result)
            root.after(0, update_gui, result, i + 1, total_ips, scan_number)
        except Exception as e:
            pass

    root.after(0, process_results, scan_number, total_ips)

def start_scan():
    stop_event.clear()
    devices.clear()
    tree.delete(*tree.get_children())
    scan_button.config(text="Stop Scan", command=stop_current_scan)
    open_browser_button.config(state=tk.DISABLED)
    status_label.config(text="Preparing to scan...")
    progress_var.set(0)
    asyncio.run_coroutine_threadsafe(perform_multiple_scans(), loop)

def stop_current_scan():
    stop_event.set()
    scan_button.config(text="Scan Network", command=start_scan)
    status_label.config(text="Stopping scan... Please wait.")

def process_results(scan_number, total_ips):
    scanned_ips = 0
    while not result_queue.empty():
        device = result_queue.get()
        scanned_ips += 1
        if device:
            pass
        root.after(0, update_gui, device, scanned_ips, total_ips, scan_number)

def open_browser():
    selected_item = tree.selection()
    if selected_item:
        ip_address = tree.item(selected_item)['values'][2]
        webbrowser.open(f"http://{ip_address}")
    else:
        status_label.config(text="Please select a device first.")

def open_router_ip():
    if default_gateway:
        webbrowser.open(f"http://{default_gateway}")
        status_label.config(text=f"Opening router interface at https://{default_gateway}")
    else:
        status_label.config(text="Unable to determine default gateway")

def toggle_mac_visibility():
    for item in tree.get_children():
        values = tree.item(item)['values']
        device = next((d for d in devices if d["IP Address"] == values[2]), None)
        if device:
            mac = "XX:XX:XX:XX:XX:XX" if hide_mac_var.get() and not device["Hidden MAC"] else device["MAC"]
            tree.item(item, values=(values[0], values[1], values[2], mac))
    
    status_label.config(text="MAC addresses hidden. You can still toggle individual MACs." if hide_mac_var.get() else "MAC addresses visible. You can toggle individual MACs.")

def show_context_menu(event):
    item = tree.identify_row(event.y)
    if item:
        tree.selection_set(item)
        context_menu.post(event.x_root, event.y_root)

def copy_to_clipboard(value):
    root.clipboard_clear()
    root.clipboard_append(value)

def copy_ip_address():
    selected_item = tree.selection()
    if selected_item:
        ip_address = tree.item(selected_item)['values'][2]
        copy_to_clipboard(ip_address)
        status_label.config(text="IP Address Copied")

def copy_mac_address():
    selected_item = tree.selection()
    if selected_item:
        mac_address = tree.item(selected_item)['values'][3]
        if mac_address != "XX:XX:XX:XX:XX:XX":
            copy_to_clipboard(mac_address)
            status_label.config(text="MAC Address Copied")
        else:
            status_label.config(text="MAC Address is hidden")

def open_in_browser():
    selected_item = tree.selection()
    if selected_item:
        ip_address = tree.item(selected_item)['values'][2]
        webbrowser.open(f"http://{ip_address}")
        status_label.config(text=f"Opening http://{ip_address} in browser")

def toggle_hidden_mac():
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]
        values = tree.item(item_id)['values']
        device = next((d for d in devices if d["IP Address"] == values[2]), None)
        if device:
            device["Hidden MAC"] = not device["Hidden MAC"]
            mac = device["MAC"] if device["Hidden MAC"] else "XX:XX:XX:XX:XX:XX"
            if hide_mac_var.get():
                mac = "XX:XX:XX:XX:XX:XX" if not device["Hidden MAC"] else device["MAC"]
            tree.item(item_id, values=(values[0], values[1], values[2], mac))
            status_label.config(text=f"MAC Address {'revealed' if device['Hidden MAC'] else 'hidden'} for selected device")

def create_sort_menu():
    sort_menu = tk.Menu(context_menu, tearoff=0)
    columns = ("Device Name", "Vendor", "IP Address", "MAC")
    for col in columns:
        sort_menu.add_command(label=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
    return sort_menu

def create_sun_moon_icon(canvas, is_dark_mode):
    canvas.delete("all")
    if is_dark_mode:
        canvas.create_oval(5, 5, 25, 25, fill="yellow", outline="yellow")
        canvas.create_line(15, 0, 15, 5, fill="yellow", width=2)
        canvas.create_line(15, 25, 15, 30, fill="yellow", width=2)
        canvas.create_line(0, 15, 5, 15, fill="yellow", width=2)
        canvas.create_line(25, 15, 30, 15, fill="yellow", width=2)
        canvas.create_line(4, 4, 8, 8, fill="yellow", width=2)
        canvas.create_line(22, 22, 26, 26, fill="yellow", width=2)
        canvas.create_line(4, 26, 8, 22, fill="yellow", width=2)
        canvas.create_line(22, 8, 26, 4, fill="yellow", width=2)
    else:
        canvas.create_oval(5, 5, 25, 25, fill="black", outline="black")
        canvas.create_oval(12, 5, 32, 25, fill="#D9D9D9", outline="#D9D9D9")

def update_donate_window_theme(donate_window):
    current_theme = style.theme_use()
    config = {
        "clam": {"bg": "#333333", "style_prefix": "Dark"},
        "default": {"bg": "white", "style_prefix": "Light"}
    }
    theme_config = config.get(current_theme, config["default"])
    
    donate_window.configure(bg=theme_config["bg"])
    for child in donate_window.winfo_children():
        widget_type = child.winfo_class()
        if widget_type in ["TFrame", "TLabel", "TButton", "TCombobox"]:
            child.configure(style=f"{theme_config['style_prefix']}.{widget_type}")
    
    style.configure(f"{theme_config['style_prefix']}.TCombobox", 
                    fieldbackground="#2a2a2a" if current_theme == "clam" else "white",
                    background="#2a2a2a" if current_theme == "clam" else "white",
                    foreground="white" if current_theme == "clam" else "black")

donate_window = None

def show_donate_info():
    global donate_window
    
    if donate_window is not None and donate_window.winfo_exists():
        donate_window.destroy()
        donate_window = None
        donate_button.config(text="Donate")
        return

    donate_window = tk.Toplevel(root)
    donate_window.title("Donate")
    donate_window.geometry("532x700")

    root.update_idletasks()
    main_window_x = root.winfo_x()
    main_window_y = root.winfo_y()
    main_window_width = root.winfo_width()
    donate_window.geometry(f"+{main_window_x + main_window_width}+{main_window_y}")

    donate_window.configure(bg="#333333")

    main_frame = ttk.Frame(donate_window, style="Dark.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    donation_image = tk.PhotoImage()
    image_label = ttk.Label(main_frame, image=donation_image, style="Dark.TLabel")
    image_label.pack(pady=10)

    description_label = ttk.Label(main_frame, text="", wraplength=500, style="Dark.TLabel")
    description_label.pack(pady=10)

    def update_donation_info(event):
        selected = donation_var.get()
        option = next(opt for opt in donation_options if opt["name"] == selected)
        
        image_data = base64.b64decode(option["image"])
        image = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)
        
        image_label.configure(image=photo)
        image_label.image = photo
        
        description_label.configure(text=option["description"])

    donation_var = tk.StringVar(donate_window)
    donation_var.set(donation_options[0]["name"])

    style.configure("Dark.TCombobox", 
                    fieldbackground="white",
                    background="white",
                    foreground="black")

    donation_dropdown = ttk.Combobox(main_frame, textvariable=donation_var, 
                                     values=[opt["name"] for opt in donation_options], 
                                     state="readonly", style="Dark.TCombobox")
    donation_dropdown.pack(pady=10)
    donation_dropdown.bind("<<ComboboxSelected>>", update_donation_info)

    update_donation_info(None)

    close_button = ttk.Button(main_frame, text="Close", command=donate_window.destroy, style="Dark.TButton")
    close_button.pack(pady=10)

    update_donate_window_theme(donate_window)

    donate_button.config(text="Close Donate")

def update_open_donation_windows():
    global donate_window
    if donate_window and donate_window.winfo_exists():
        update_donate_window_theme(donate_window)

def toggle_theme():
    current_theme = style.theme_use()
    new_theme = "default" if current_theme == "clam" else "clam"
    style.theme_use(new_theme)
    
    is_dark_mode = new_theme == "clam"
    root.configure(bg="#333333" if is_dark_mode else "white")
    
    for widget in [main_frame, status_label, tree, progress_bar, hide_mac_check, disable_mac_lookup_check,
                   scan_button, open_browser_button, open_router_ip_button, donate_button]:
        widget.configure(style=f"{'Dark' if is_dark_mode else 'Light'}.{widget.winfo_class()}")
    
    context_menu.configure(bg="#333333" if is_dark_mode else "white", fg="white" if is_dark_mode else "black")
    create_sun_moon_icon(theme_switch, is_dark_mode)
    theme_switch.configure(bg="#333333" if is_dark_mode else "#D9D9D9")
    
    update_open_donation_windows()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda x: tuple(map(int, x[0].split('.'))) if col == "IP Address" else x[0], reverse=reverse)

    for index, (_, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def setup_treeview():
    columns = ("Device Name", "Vendor", "IP Address", "MAC")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", style="Dark.Treeview")
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
        tree.column(col, width=150)
    
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind('<<TreeviewSelect>>', lambda e: open_browser_button.config(state=tk.NORMAL if tree.selection() else tk.DISABLED))
    tree.bind('<Button-3>', show_context_menu)
    return tree

def add_device_to_tree(device):
    existing_items = tree.get_children('')
    for item in existing_items:
        if tree.item(item)['values'][2] == device["IP Address"]:
            return

    mac = "XX:XX:XX:XX:XX:XX" if hide_mac_var.get() and not device["Hidden MAC"] else device["MAC"]
    tree.insert("", "end", values=(device["Device Name"], device["Vendor"], device["IP Address"], mac))
    tree.yview_moveto(1)

def update_gui(device, scanned_ips, total_ips, scan_number):
    if device and device["IP Address"] not in [d["IP Address"] for d in devices]:
        devices.append(device)
        add_device_to_tree(device)
    progress_var.set((scanned_ips / total_ips) * 100)
    root.update_idletasks()
    status_label.config(text=f"Scan {scan_number}/{num_scans_entry.get()}... {scanned_ips}/{total_ips} IPs checked. Found {len(tree.get_children())} devices. ({scanned_ips/total_ips*100:.1f}%)")

def on_closing():
    global donate_window
    stop_event.set()
    loop.call_soon_threadsafe(loop.stop)
    if donate_window and donate_window.winfo_exists():
        donate_window.destroy()
    root.destroy()

def validate_num_scans(P):
    return P == "" or (P.isdigit() and 1 <= int(P) <= 10)

def validate_ip_range(P):
    return P == "" or (P.isdigit() and 1 <= int(P) <= 254)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio_thread = AsyncioThread(loop)
    asyncio_thread.start()

    root = tk.Tk()
    root.title("Nobody's IP Scanner")
    root.geometry("1000x600")

    icon_base64 = "iVBORw0KGgoAAAANSUhEUgAAA..."  # Replace with your actual base64 string
    set_icon_from_base64(root, icon_base64)

    style = ttk.Style(root)
    style.theme_use("clam")

    for mode in ["Dark", "Light"]:
        style.configure(f"{mode}.TFrame", background="#333333" if mode == "Dark" else "white")
        style.configure(f"{mode}.TLabel", background="#333333" if mode == "Dark" else "white", foreground="white" if mode == "Dark" else "black")
        style.configure(f"{mode}.TButton", background="white" if mode == "Dark" else "#e0e0e0", foreground="#555555" if mode == "Dark" else "black")
        style.configure(f"{mode}.TCheckbutton", background="#333333" if mode == "Dark" else "white", foreground="white" if mode == "Dark" else "black")
        style.map(f"{mode}.TCheckbutton", background=[('active', '#444444' if mode == "Dark" else '#f0f0f0')])
        style.configure(f"{mode}.Treeview", background="#2a2a2a" if mode == "Dark" else "white", fieldbackground="#2a2a2a" if mode == "Dark" else "white", foreground="white" if mode == "Dark" else "black")
        style.configure(f"{mode}.Treeview.Heading", background="#2a2a2a" if mode == "Dark" else "white", foreground="white" if mode == "Dark" else "black")
        style.map(f"{mode}.Treeview", background=[('selected', '#4a6984' if mode == "Dark" else '#bdddf4')])
        style.configure(f"{mode}.Horizontal.TProgressbar", troughcolor="white" if mode == "Dark" else "#e0e0e0", background="#333333" if mode == "Dark" else "#0078d7")

    root.configure(bg="#333333")

    main_frame = ttk.Frame(root, padding="10", style="Dark.TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    top_frame = ttk.Frame(main_frame, style="Dark.TFrame")
    top_frame.pack(fill=tk.X, pady=(0, 10))

    options_frame = ttk.Frame(top_frame, style="Dark.TFrame")
    options_frame.pack(expand=True)

    network_frame = ttk.Frame(options_frame, style="Dark.TFrame")
    network_frame.pack(side=tk.LEFT, padx=(0, 10))

    network_label = ttk.Label(network_frame, text="Network Address:", style="Dark.TLabel")
    network_label.pack(side=tk.LEFT, padx=(0, 5))

    default_gateway, default_network = get_network_info()
    network_entry = ttk.Entry(network_frame, width=15)
    network_entry.pack(side=tk.LEFT)
    network_entry.insert(0, default_network or "192.168.1")
    ToolTip(network_entry, "Enter the network address (e.g., 192.168.1)")

    range_frame = ttk.Frame(options_frame, style="Dark.TFrame")
    range_frame.pack(side=tk.LEFT, padx=(0, 10))

    range_label = ttk.Label(range_frame, text="IP Range:", style="Dark.TLabel")
    range_label.pack(side=tk.LEFT, padx=(0, 5))

    vcmd = (root.register(validate_ip_range), '%P')
    start_range_entry = ttk.Entry(range_frame, width=3, validate="key", validatecommand=vcmd)
    start_range_entry.pack(side=tk.LEFT)
    start_range_entry.insert(0, "1")
    ToolTip(start_range_entry, "Start of IP range (1-254)")

    range_separator = ttk.Label(range_frame, text="-", style="Dark.TLabel")
    range_separator.pack(side=tk.LEFT, padx=5)

    end_range_entry = ttk.Entry(range_frame, width=3, validate="key", validatecommand=vcmd)
    end_range_entry.pack(side=tk.LEFT)
    end_range_entry.insert(0, "254")
    ToolTip(end_range_entry, "End of IP range (1-254)")

    checkboxes_frame = ttk.Frame(options_frame, style="Dark.TFrame")
    checkboxes_frame.pack(side=tk.LEFT, padx=(0, 10))

    hide_mac_var = tk.BooleanVar(value=True)
    hide_mac_check = ttk.Checkbutton(checkboxes_frame, text="Hide MAC Address", variable=hide_mac_var, command=toggle_mac_visibility, style="Dark.TCheckbutton")
    hide_mac_check.pack(side=tk.TOP, anchor=tk.W)
    ToolTip(hide_mac_check, "Show/hide MAC addresses in the device list")

    disable_mac_lookup_var = tk.BooleanVar(value=False)
    disable_mac_lookup_check = ttk.Checkbutton(checkboxes_frame, text="Disable Mac Lookup", variable=disable_mac_lookup_var, style="Dark.TCheckbutton")
    disable_mac_lookup_check.pack(side=tk.TOP, anchor=tk.W)
    ToolTip(disable_mac_lookup_check, "Disable MAC address vendor lookup")

    buttons_frame = ttk.Frame(options_frame, style="Dark.TFrame")
    buttons_frame.pack(side=tk.LEFT)

    vcmd = (root.register(validate_num_scans), '%P')
    num_scans_entry = ttk.Entry(buttons_frame, width=3, justify=tk.CENTER, style="Dark.TEntry", validate="key", validatecommand=vcmd)
    num_scans_entry.pack(side=tk.LEFT, padx=(0, 5))
    num_scans_entry.insert(0, "3")
    ToolTip(num_scans_entry, "Number of scans to perform (1-10)")

    multiply_label = ttk.Label(buttons_frame, text="×", style="Dark.TLabel")
    multiply_label.pack(side=tk.LEFT, padx=(0, 5))

    scan_button = ttk.Button(buttons_frame, text="Scan Network", command=start_scan, style="Dark.TButton")
    scan_button.pack(side=tk.LEFT, padx=(0, 5))
    ToolTip(scan_button, "Start scanning the specified network")

    open_browser_button = ttk.Button(buttons_frame, text="Open In Browser", command=open_browser, state=tk.DISABLED, style="Dark.TButton")
    open_browser_button.pack(side=tk.LEFT, padx=(0, 5))
    ToolTip(open_browser_button, "Open the selected device's IP address in a web browser")

    open_router_ip_button = ttk.Button(buttons_frame, text="Open Router IP", command=open_router_ip, style="Dark.TButton")
    open_router_ip_button.pack(side=tk.LEFT)
    ToolTip(open_router_ip_button, "Open the default gateway (router) IP in a web browser")

    tree = setup_treeview()

    context_menu = tk.Menu(root, tearoff=0, bg="#333333", fg="white")
    context_menu.add_command(label="Copy IP Address", command=copy_ip_address)
    context_menu.add_command(label="Copy MAC Address", command=copy_mac_address)
    context_menu.add_command(label="Open In Browser", command=open_in_browser)
    context_menu.add_command(label="Toggle Hidden MAC", command=toggle_hidden_mac)
    context_menu.add_cascade(label="Sort", menu=create_sort_menu())

    bottom_frame = ttk.Frame(main_frame, style="Dark.TFrame")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

    progress_frame = ttk.Frame(bottom_frame, style="Dark.TFrame")
    progress_frame.pack(fill=tk.X)

    theme_switch = tk.Canvas(progress_frame, width=30, height=30, bg="#333333", highlightthickness=0)
    theme_switch.pack(side=tk.LEFT, padx=10)
    create_sun_moon_icon(theme_switch, True)
    theme_switch.bind("<Button-1>", lambda e: toggle_theme())
    ToolTip(theme_switch, "Toggle between dark and light mode")

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_frame, length=880, variable=progress_var, maximum=100, style="Dark.Horizontal.TProgressbar")
    progress_bar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
    ToolTip(progress_bar, "Scan progress")

    status_donate_frame = ttk.Frame(bottom_frame, style="Dark.TFrame")
    status_donate_frame.pack(fill=tk.X, pady=(5, 0))

    status_label = ttk.Label(status_donate_frame, text="", style="Dark.TLabel", anchor="center")
    status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    donate_button = ttk.Button(status_donate_frame, text="Donate", command=show_donate_info, style="Dark.TButton")
    donate_button.pack(side=tk.RIGHT, padx=10)
    ToolTip(donate_button, "Support the development of this tool")

    theme_switch.bind("<Button-1>", lambda e: (toggle_theme(), update_open_donation_windows()))

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
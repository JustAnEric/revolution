from asyncio import run
from tkinter import Tk, messagebox
import ui, os, sys, requests, threading

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

async def main():
    d = ui.LoadingScreen()
    threading.Thread(target=d.start, daemon=True).start()
    try:
        if requests.get('http://revolution-web.repl.co/online-test', timeout=5).text is None:
            return messagebox.askokcancel("Offline", "Please go online to enter our app.")
    except requests.exceptions.ConnectionError as e:
        return messagebox.askokcancel("Offline", "Please go online to enter our app.")
    except requests.exceptions.Timeout as e:
        return messagebox.askokcancel("Could not connect to service", "Sorry, we could not connect to our service.\nYour internet connection may be slow or not suitable/supported.")
    d.quit()
    c = ui.run()
    threading.Thread(target=c.start, daemon=True).start()

run(main())
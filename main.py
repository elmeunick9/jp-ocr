import sys
import pyperclip
import pyautogui
from tkinter import *
from pynput import mouse, keyboard
from PIL import Image
import torch
from manga_ocr import MangaOcr

# Initialize the Manga OCR model only once
def get_mocr():
    if not hasattr(get_mocr, "instance"):
        print("Initializing Manga OCR model...")
        get_mocr.instance = MangaOcr()
    return get_mocr.instance

class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root

        # Global capturing mode flag (default to False)
        self.capturing_mode = False

        # Start with a tiny invisible window that responds to events (1x1 size)
        self.root.geometry("1x1")  # Set window size to 1x1, but it will be invisible
        self.root.overrideredirect(True)  # Remove borders
        self.root.attributes("-topmost", True)  # Keep window on top
        
        # Set transparency to 30% (semi-transparent)
        self.root.attributes("-alpha", 0.8)
        self.root.wm_attributes("-transparentcolor", "white")
        
        # Initialize drawing state
        self.start_pos = None
        self.end_pos = None
        self.drawing = False

        self.canvas = Canvas(
            root,
            highlightthickness=0,  # No default border
            bg="white",  # Transparent background
            bd=0  # No border
        )
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<Configure>", self.redraw_border)

    def redraw_border(self, event):
        self.canvas.delete("all")  # Clear previous drawings
        self.canvas.create_rectangle(
            0, 0, event.width - 1, event.height - 1,
            outline="green",  # Green border
            width=1
        )

    def mouse_click(self, x, y, button, pressed):
        if not self.capturing_mode:
            return
        
        if button == mouse.Button.middle:
            if pressed:
                print("Middle mouse button pressed globally.")
                # Show the window at the current mouse position
                self.start_pos = (x, y)
                self.end_pos = (x, y)
                self.drawing = True
                self.root.deiconify()  # Make the window visible
                self.root.geometry(f"1x1+{x}+{y}")  # Position at mouse click
                self.root.attributes("-alpha", 0.8)  # Set transparency to 30%
            else:
                print("Middle mouse button released.")
                # Capture the selected area and hide the window
                self.drawing = False
                try:
                    self.capture_screen()
                except Exception as e:
                    print(f"Error capturing screen: {e}")

                self.root.withdraw()  # Hide the window on mouse release

    def mouse_move(self, x, y):
        if self.drawing:
            self.end_pos = (x, y)
            self.update_window_geometry()

    def update_window_geometry(self):
        if self.start_pos and self.end_pos:
            x1, y1 = self.start_pos
            x2, y2 = self.end_pos
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            x_offset = min(x1, x2)
            y_offset = min(y1, y2)
            self.root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
            #print(f"Rectangle: width={width}, height={height}, x_offset={x_offset}, y_offset={y_offset}")

    def capture_screen(self):
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        if x1 > x2 or y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        print(f"Capturing screen from ({x1},{y1}) to ({x2},{y2})")

        # Capture the screen region directly using pyautogui
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        # Perform OCR on the captured screenshot (no need to convert it to a NumPy array)
        print("Performing OCR...")
        mocr = get_mocr()
        text = mocr(screenshot)  # Use the PIL Image directly

        # Copy result to clipboard
        pyperclip.copy(text)
        print("Extracted text:", text.encode("utf-8"))

    def toggle_capturing_mode(self, value=None):

        if value is not None:
            self.capturing_mode = value
        else:
            self.capturing_mode = not self.capturing_mode

        if self.capturing_mode == False:
            self.root.withdraw()
            self.drawing = False

        print(f"Toggling capturing mode: {self.capturing_mode}")


# Event handler for mouse click
def on_mouse_click(x, y, button, pressed):
    capture_app.mouse_click(x, y, button, pressed)

# Event handler for mouse move
def on_mouse_move(x, y):
    capture_app.mouse_move(x, y)


if __name__ == "__main__":
    print("Starting application...")
    root = Tk()
    capture_app = ScreenCaptureApp(root)

    # Start global listeners for mouse and keyboard
    mouse_listener = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move)
    mouse_listener.start()

    keyboard_listener = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+j': lambda: capture_app.toggle_capturing_mode(True),
        '<esc>': lambda: capture_app.toggle_capturing_mode(False)}
    )
    keyboard_listener.start()

    # Start the tkinter event loop
    root.mainloop()

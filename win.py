import webview
import pyperclip
import time

def main():
    # Initial clipboard content
    previous_clipboard_text = pyperclip.paste()

    # Construct the initial URL
    url = f'http://localhost:3000/?theme=dark&q={previous_clipboard_text}'

    # Create the webview window
    window = webview.create_window("Translator Window", url, width=500, height=900, zoomable=True, on_top=True)

    # Function to reload the URL if clipboard content changes
    def check_clipboard():
        nonlocal previous_clipboard_text, window
        while True:
            # Get the current clipboard content
            try:
                current_clipboard_text = pyperclip.paste()
            except Exception as e:
                print(f"Error reading clipboard: {e}")

            # If clipboard content has changed, update the URL and reload the webview
            if current_clipboard_text != previous_clipboard_text:
                print(f"Clipboard changed: {current_clipboard_text}")
                new_url = f'http://localhost:3000/?theme=dark&q={current_clipboard_text}'
                window.load_url(new_url)
                previous_clipboard_text = current_clipboard_text  # Update the previous clipboard content

            # Wait for a short time before checking again (e.g., 1 second)
            time.sleep(1)

    # Start the clipboard check in a background thread
    import threading
    threading.Thread(target=check_clipboard, daemon=True).start()

    # Start the webview
    webview.start()

if __name__ == "__main__":
    main()

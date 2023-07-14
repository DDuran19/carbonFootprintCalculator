import webview

def open_webview(url):
    webview.create_window("Learn more", url)
    webview.start()

if __name__ == "__main__":
    # Retrieve the URL as a command-line argument
    import sys
    url = sys.argv[1]

    # Open the webview window
    open_webview(url)

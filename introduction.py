import webview
def intro():
    webview.create_window("Carbon Footprint Calculator", "./intro.html", width=800, height=600)
    webview.start()

if __name__ == '__main__':
    intro()
import tkinter as tk

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter-YouTube_Downloader")
        self.iconbitmap(".\\icon.ico")

        self.mainloop()
        
if __name__ == "__main__":
    YouTubeDownloader()
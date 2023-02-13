import tkinter as tk

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter-YouTube_Downloader")
        self.iconbitmap(".\\icon.ico")#credit: flaticon.com
        self.config(padx=20, pady=20)

        self.columnconfigure(0, weight = 1)

        #----------Load Video/Playlist----------#
        tk.Label(self, text="Video/Playlist URL:").grid(row=0, column=0, sticky=tk.W)

        url_entry = tk.Entry(self)
        url_entry.grid(row=1, column=0, sticky = tk.EW)

        load_button = tk.Button(self, text="Load")
        load_button.grid(row=1, column=1, sticky=tk.W)

        self.mainloop()
        
if __name__ == "__main__":
    YouTubeDownloader()
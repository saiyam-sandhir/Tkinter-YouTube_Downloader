import tkinter as tk
from tkinter import ttk

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter-YouTube_Downloader")
        self.iconbitmap(".\\icon.ico")#credit: flaticon.com
        self.config(padx=20, pady=20)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        #----------Load Video/Playlist----------#
        tk.Label(self, text="Video/Playlist URL:").grid(row=0, column=0, sticky=tk.W)

        url_entry = tk.Entry(self)
        url_entry.grid(row=1, column=0, columnspan = 2, sticky = tk.NSEW)

        load_button = tk.Button(self, text="Load")
        load_button.grid(row=1, column=1, sticky=tk.E)

        #----------Thumbnail----------#
        thumbnail_labelframe = tk.LabelFrame(self, text="Thumbnail", width=400, height=225)
        thumbnail_labelframe.grid(row=2, column=1)
        thumbnail_labelframe.grid_rowconfigure(0, weight=1)
        thumbnail_labelframe.grid_columnconfigure(0, weight=1)

        #----------Loaded Video(s)----------#
        loaded_videos_frame = tk.Frame(self)
        loaded_videos_frame.grid(row=2, column=0, sticky=tk.NSEW, pady = 20, padx=(0, 20))

        tk.Label(loaded_videos_frame, text="Video(s):").grid(row=0, column=0, sticky=tk.W)
        select_all_videos_button = tk.Button(loaded_videos_frame, text="Select all")
        select_all_videos_button.grid(row=0, column=1, sticky=tk.E)
        videos_listbox = tk.Listbox(loaded_videos_frame, width = 50)
        videos_listbox.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)

        #for video option
        tk.Label(loaded_videos_frame, text="Quality:").grid(row=3, column=0, sticky=tk.W, pady=(20, 0))
        qual_var = tk.StringVar(self)
        qual_var.set("Choose video quality")
        quality_options = tk.OptionMenu(loaded_videos_frame, qual_var, "None")
        quality_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)

        #for subtitle option
        tk.Label(loaded_videos_frame, text="Language:").grid(row=3, column=0, sticky=tk.W, pady=(20, 0))
        qual_var = tk.StringVar(self)
        qual_var.set("Choose subtitle language")
        quality_options = tk.OptionMenu(loaded_videos_frame, qual_var, "None")
        quality_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)

        #----------Download----------#
        data_var = tk.StringVar(self)
        data_var.set("Video")
        data_type_options = tk.OptionMenu(self, data_var, "Video", "Audio", "Subtitle")
        data_type_options.grid(row=3, column=1, sticky = tk.NSEW)

        download_button = tk.Button(self, text="Download")
        download_button.grid(row = 4, column = 1, sticky=tk.NSEW)


        self.mainloop()
        
if __name__ == "__main__":
    YouTubeDownloader()
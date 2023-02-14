import customtkinter as ctk
import tkinter as tk
from PIL import Image

class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter-YouTube_Downloader")
        self.after(201, lambda: self.iconbitmap(".\\images\\icon.ico"))#credit: flaticon.com
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        #----------Load Video/Playlist----------#
        load_video_frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")
        load_video_frame.grid(row=1, column=0, columnspan=2,sticky=tk.NSEW)

        ctk.CTkLabel(self, text="Video/Playlist URL:", font=("Palatino", 20)).grid(row=0, column=0, sticky=tk.W)

        url_entry = ctk.CTkEntry(load_video_frame, corner_radius=10)
        url_entry.pack(side = tk.LEFT, fill=tk.BOTH, expand=True)

        load_button_img = ctk.CTkImage(light_image=Image.open(".\\images\\load.png"), dark_image=Image.open(".\\images\\load.png"), size=(40, 40))
        load_button = ctk.CTkButton(load_video_frame, text="", image=load_button_img, anchor=tk.CENTER, width=40, corner_radius=10, bg_color = "#242424", fg_color="#242424", hover_color="#EAEAEA")
        load_button.pack(side=tk.RIGHT)

        #----------Thumbnail----------#
        thumbnail_viewer = ctk.CTkTabview(self, width=400, height=225, corner_radius=10)
        thumbnail_viewer.grid(row=2, column=1)
        thumbnail_viewer.grid_rowconfigure(0, weight=1)
        thumbnail_viewer.grid_columnconfigure(0, weight=1)

        thumbnail_viewer.add("Thumbnail")

        #----------Loaded Video(s)----------#
        loaded_videos_frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")
        loaded_videos_frame.grid(row=2, column=0, sticky=tk.NSEW, pady = (25,0), padx=(0, 20))

        ctk.CTkLabel(loaded_videos_frame, text="Video(s):", font=("Palatino", 20)).grid(row=0, column=0, sticky=tk.W)
        
        select_all_videos_checkbox = ctk.CTkCheckBox(loaded_videos_frame, text="Select all", font=("Palatino", 20),onvalue="on", offvalue="off")
        select_all_videos_checkbox.grid(row=0, column=1, sticky=tk.E)
        
        videos_listbox = tk.Listbox(loaded_videos_frame, width = 50, relief=tk.FLAT, bg="#2B2B2B", highlightthickness=0)
        videos_listbox.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 20))

        #for video option
        video_option_label = ctk.CTkLabel(loaded_videos_frame, text="Quality:", font=("Palatino", 20))
        video_option_label.grid(row=3, column=0, sticky=tk.W)
        quality_options = ctk.CTkOptionMenu(loaded_videos_frame, values=["None"], fg_color="#343638", hover=False, corner_radius=10)
        quality_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
        quality_options.set("Choose Quality")

        #for subtitle option
        subtitle_option_label = ctk.CTkLabel(loaded_videos_frame, text="Language:", font=("Palatino", 20))
        subtitle_option_label.grid(row=3, column=0, sticky=tk.W)
        language_options = ctk.CTkOptionMenu(loaded_videos_frame, values=["None"], fg_color="#343638", hover=False, corner_radius=10)
        language_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
        language_options.set("Select Language")
        subtitle_option_label.grid_forget()
        language_options.grid_forget()
        

        #----------Download----------#
        data_type_options = ctk.CTkOptionMenu(self, values=["Video", "Audio", "Subtitle"], fg_color="#343638", hover=False, corner_radius=10)
        data_type_options.grid(row=3, column=1, sticky = tk.NS, pady=10)
        data_type_options.set("Video")

        download_button_img = ctk.CTkImage(light_image=Image.open(".\\images\\download.png"), dark_image=Image.open(".\\images\\download.png"), size=(20, 20))
        download_button = ctk.CTkButton(self, text="Download", image=download_button_img, fg_color="green", hover_color="#3C6255", anchor=tk.CENTER, corner_radius=10)
        download_button.grid(row=4, column=1, sticky=tk.NS)

        #----------Progress Bar----------#
        download_progress_bar = ctk.CTkProgressBar(self, corner_radius=10)
        download_progress_bar.grid(row=4, column=0, sticky=tk.NSEW, padx=(0, 20))

        self.mainloop()
        
if __name__ == "__main__":
    YouTubeDownloader()
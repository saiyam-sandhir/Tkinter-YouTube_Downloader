import customtkinter as ctk
import tkinter as tk
from PIL import Image
import pytube
import requests
from io import BytesIO
import os

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
        load_button = ctk.CTkButton(load_video_frame, text="", image=load_button_img, anchor=tk.CENTER, width=40, corner_radius=10, bg_color = "#242424", fg_color="#242424", hover_color="#EAEAEA", command=lambda: [self.load_youtube(url_entry.get())])
        load_button.pack(side=tk.RIGHT)

        self.file_not_found_error_label = ctk.CTkLabel(self, text="Error: 404, YouTube video/playlist not found", text_color="red")

        self.bind("<Return>", lambda x: [self.load_youtube(url_entry.get())])

        #----------Thumbnail----------#
        thumbnail_viewer = ctk.CTkTabview(self, width=400, height=295, corner_radius=10)
        thumbnail_viewer.grid(row=3, column=1)
        thumbnail_viewer.grid_rowconfigure(0, weight=1)
        thumbnail_viewer.grid_columnconfigure(0, weight=1)

        thumbnail_viewer.add("Thumbnail")

        self.thumbnail_image = ctk.CTkImage(light_image=Image.open(".\\images\\thumbnail.png"), dark_image=Image.open(".\\images\\thumbnail.png"), size=(100, 100))
        self.thumbnail_img = ctk.CTkButton(thumbnail_viewer.tab("Thumbnail"), text="", image=self.thumbnail_image, bg_color="#2B2B2B", fg_color="#2B2B2B", hover=False, width=320, height=180)
        self.thumbnail_img.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.title_label = ctk.CTkLabel(thumbnail_viewer.tab("Thumbnail"), text="", font=("Arial", 15), bg_color="#2B2B2B", fg_color="#2B2B2B")
        self.title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        #----------Loaded Video(s)----------#
        loaded_videos_frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")
        loaded_videos_frame.grid(row=3, column=0, sticky=tk.NSEW, pady = (25,0), padx=(0, 20))

        ctk.CTkLabel(loaded_videos_frame, text="Video(s):", font=("Palatino", 20)).grid(row=0, column=0, sticky=tk.W)
        
        self.select_all_videos_checkbox = ctk.CTkCheckBox(loaded_videos_frame, text="Select all", font=("Palatino", 20), state=tk.DISABLED, command=self.checkbox_clicked)
        self.select_all_videos_checkbox.grid(row=0, column=1, sticky=tk.E)
        
        self.videos_listbox = tk.Listbox(loaded_videos_frame, selectmode=tk.MULTIPLE, fg="white", width = 50, relief=tk.FLAT, bg="#2B2B2B", highlightthickness=0)
        self.videos_listbox.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 20))

        #for video option
        self.video_option_label = ctk.CTkLabel(loaded_videos_frame, text="Quality:", font=("Palatino", 20))
        self.video_option_label.grid(row=3, column=0, sticky=tk.W)
        self.quality_options = ctk.CTkOptionMenu(loaded_videos_frame, values=["None"], fg_color="#343638", hover=False, corner_radius=10)
        self.quality_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
        self.quality_options.set("Choose Quality")

        #for subtitle option
        self.subtitle_option_label = ctk.CTkLabel(loaded_videos_frame, text="Language:", font=("Palatino", 20))
        self.language_options = ctk.CTkOptionMenu(loaded_videos_frame, values=["None"], fg_color="#343638", hover=False, corner_radius=10)
        self.language_options.set("Select Language")

        #----------Download----------#
        self.data_type_options = ctk.CTkOptionMenu(self, values=["Video", "Audio", "Subtitle"], fg_color="#343638", hover=False, corner_radius=10, command=self.change_datatype)
        self.data_type_options.grid(row=4, column=1, sticky = tk.NS, pady=10)
        self.data_type_options.set("Video")

        download_button_img = ctk.CTkImage(light_image=Image.open(".\\images\\download.png"), dark_image=Image.open(".\\images\\download.png"), size=(20, 20))
        download_button = ctk.CTkButton(self, text="Download", image=download_button_img, fg_color="green", hover_color="#3C6255", anchor=tk.CENTER, corner_radius=10, command=lambda: [self.download(url_entry.get())])
        download_button.grid(row=5, column=1, sticky=tk.NS)

        #----------Progress Bar----------#
        self.download_progress_bar = ctk.CTkProgressBar(self, corner_radius=10, orientation=tk.HORIZONTAL)

        self.mainloop()

    def load_youtube(self, link: str):
        try:
            if not "playlist" in link:
                self.select_all_videos_checkbox.deselect()
                self.download_progress_bar.grid(row=5, column=0, sticky=tk.NSEW, padx=(0, 20))
                self.download_progress_bar.set(0)
                self.update_idletasks()
                self.yt = pytube.YouTube(link)
                self.thumbnail_img.configure(image=self.thumbnail_image)
                self.title_label.configure(text="")
                self.download_progress_bar.set(0.25)
                self.update_idletasks()
                self.videos_listbox.delete(0, tk.END)
                self.download_progress_bar.set(0.5)
                self.update_idletasks()
                self.videos_listbox.insert(0, self.yt.title)
                mp4_streams = self.yt.streams.filter(file_extension="mp4", mime_type="video/mp4").order_by("resolution")
                resolutions = {stream.resolution for stream in mp4_streams}
                self.quality_options.configure(values=resolutions)
                self.download_progress_bar.set(0.625)
                self.update_idletasks()
                subtitle_languages = self.yt.caption_tracks
                languages = {lang.name for lang in subtitle_languages}
                self.language_options.configure(values=languages)
                self.download_progress_bar.set(0.75)
                self.update_idletasks()
            else:
                self.download_progress_bar.grid(row=5, column=0, sticky=tk.NSEW, padx=(0, 20))
                self.download_progress_bar.set(0)
                self.update_idletasks()
                self.yt = pytube.Playlist(link)
                self.thumbnail_img.configure(image=self.thumbnail_image)
                self.title_label.configure(text="")
                self.download_progress_bar.set(0.25)
                self.update_idletasks()
                self.videos_listbox.delete(0, tk.END)
                self.download_progress_bar.set(0.5)
                self.update_idletasks()
                num_of_videos = len(self.yt.videos)
                for i, video in enumerate(self.yt.videos):
                    self.download_progress_bar.set((0.5+(0.25*((i+1)/num_of_videos))))
                    self.update_idletasks()
                    self.videos_listbox.insert(i, video.title)
            self.file_not_found_error_label.grid_forget()

            if type(self.yt) == pytube.YouTube:
                thumbnail_url = self.yt.thumbnail_url
            else:
                thumbnail_url = self.yt.videos[0].thumbnail_url

            response = requests.get(thumbnail_url)
            thumbnail_data = response.content
            thumbnail_img = ctk.CTkImage(light_image=Image.open(BytesIO(thumbnail_data)), dark_image=Image.open(BytesIO(thumbnail_data)), size=(320, 180))
            self.thumbnail_img.configure(image=thumbnail_img)

            if len(self.yt.title) > 40:
                self.title_label.configure(text=f"Title: {self.yt.title[0:40]}....")
            else:
                self.title_label.configure(text=f"Title: {self.yt.title}")

            self.download_progress_bar.set(1)
            self.update_idletasks()
            self.after(200, self.download_progress_bar.grid_forget)

            self.select_all_videos_checkbox.configure(state=tk.NORMAL)

        except pytube.exceptions.RegexMatchError:
            self.file_not_found_error_label.grid(row=2, column=0, sticky=tk.W)
            self.download_progress_bar.grid_forget()

    def download(self, link: str):
        if not "plalist" in link:
            datatype = self.data_type_options.get()

            if datatype == "Video":
                pass

            elif datatype == "Audio":
                audio_streams = self.yt.streams.filter(only_audio=True)
                self.download_progress_bar.grid(row=5, column=0, sticky=tk.NSEW, padx=(0, 20))
                self.download_progress_bar.set(0)
                self.update_idletasks()
                audio_stream = audio_streams.order_by("abr").last()
                file_path = tk.filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"), mustexist=True)
                self.download_progress_bar.set(0.5)
                self.update_idletasks()
                try:
                    audio_stream.download(output_path=file_path, filename=f"{self.yt.title}__AUDIO.mp3")
                except OSError:
                    audio_stream.download(output_path=file_path, filename="Tkinter_YouTubeDownloader_file__AUDIO.mp3")
                self.download_progress_bar.set(1)
                self.update_idletasks()
                self.download_progress_bar.grid_forget()
            else:
                pass

    def checkbox_clicked(self):
        if bool(self.select_all_videos_checkbox.get()):
            self.videos_listbox.selection_set(0, tk.END)
        else:
            self.videos_listbox.selection_clear(0, tk.END)

    def change_datatype(self, datatype: str):
        if datatype == "Video":
            self.video_option_label.grid(row=3, column=0, sticky=tk.W)
            self.quality_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
            self.subtitle_option_label.grid_forget()
            self.language_options.grid_forget()

        elif datatype == "Audio":
            self.video_option_label.grid_forget()
            self.quality_options.grid_forget()
            self.subtitle_option_label.grid_forget()
            self.language_options.grid_forget()

        else:
            self.subtitle_option_label.grid(row=3, column=0, sticky=tk.W)
            self.language_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
            self.video_option_label.grid_forget()
            self.quality_options.grid_forget()

if __name__ == "__main__":
    YouTubeDownloader()
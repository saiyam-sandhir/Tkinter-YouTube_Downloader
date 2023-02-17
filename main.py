import customtkinter as ctk
import tkinter as tk
from PIL import Image
import pytube
import requests
from io import BytesIO
import os
import random

class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter-YouTube_Downloader")
        self.after(201, lambda: self.iconbitmap(".\\images\\icon.ico"))#credit: flaticon.com
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        #----------TOP FRAME----------#
        top_frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")
        top_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 15))

        top_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(top_frame, text="Video/Playlist URL:", font=("Palatino", 20)).grid(row=0, column=0, sticky=tk.W)

        url_entry = ctk.CTkEntry(top_frame, corner_radius=10)
        url_entry.grid(row=1, column=0, sticky=tk.NSEW)

        load_button_img = ctk.CTkImage(light_image=Image.open(".\\images\\load.png"), dark_image=Image.open(".\\images\\load.png"), size=(40, 40))
        load_button = ctk.CTkButton(top_frame, text="", image=load_button_img, anchor=tk.CENTER, width=40, corner_radius=10, bg_color="#242424", fg_color="#242424", hover_color="#EAEAEA", command=lambda: [self.load_youtube(url_entry.get())])
        load_button.grid(column=1, row=1, sticky=tk.NSEW)

        self.file_not_found_error_label = ctk.CTkLabel(self, text="Error: 404, YouTube video/playlist not found", text_color="red")

        self.bind("<Return>", lambda x: [self.load_youtube(url_entry.get())])

        #----------LEFT FRAME----------#
        left_frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")
        left_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=(0, 20), pady=(10, 0))

        left_frame.rowconfigure(4, weight=1)

        ctk.CTkLabel(left_frame, text="Video(s):", font=("Palatino", 20)).grid(row=0, column=0, sticky=tk.W)
        
        self.select_all_videos_checkbox = ctk.CTkCheckBox(left_frame, text="Select all", font=("Palatino", 20), state=tk.DISABLED, command=self.checkbox_clicked)
        self.select_all_videos_checkbox.grid(row=0, column=1, sticky=tk.E)
        
        self.videos_listbox = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, fg="white", width=50, relief=tk.FLAT, bg="#2B2B2B", highlightthickness=0)
        self.videos_listbox.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 20))

        #for video option
        self.video_option_label = ctk.CTkLabel(left_frame, text="Quality:", font=("Palatino", 20))
        self.video_option_label.grid(row=2, column=0, sticky=tk.W)
        self.quality_options = ctk.CTkOptionMenu(left_frame, values=["None"], fg_color="#343638", hover=False, corner_radius=10)
        self.quality_options.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)
        self.quality_options.set("Choose Quality")

        self.download_progress_bar = ctk.CTkProgressBar(left_frame, progress_color="green", corner_radius=10, orientation=tk.HORIZONTAL)

        #----------RIGHT FRAME----------#
        right_frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")
        right_frame.grid(row=1, column=1, sticky=tk.NSEW)

        thumbnail_viewer = ctk.CTkTabview(right_frame, width=400, height=295, corner_radius=10)
        thumbnail_viewer.grid(row=0, column=0)

        thumbnail_viewer.add("Thumbnail")

        self.thumbnail_image = ctk.CTkImage(light_image=Image.open(".\\images\\thumbnail.png"), dark_image=Image.open(".\\images\\thumbnail.png"), size=(100, 100))
        self.thumbnail_img = ctk.CTkButton(thumbnail_viewer.tab("Thumbnail"), text="", image=self.thumbnail_image, bg_color="#2B2B2B", fg_color="#2B2B2B", hover=False, width=320, height=180)
        self.thumbnail_img.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.title_label = ctk.CTkLabel(thumbnail_viewer.tab("Thumbnail"), text="", font=("Arial", 15), bg_color="#2B2B2B", fg_color="#2B2B2B")
        self.title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        self.data_type_options = ctk.CTkOptionMenu(right_frame, values=["Video", "Audio"], fg_color="#343638", hover=False, corner_radius=10, command=self.change_datatype)
        self.data_type_options.grid(row=1, column=0, sticky=tk.NS, pady=10)
        self.data_type_options.set("Video")

        download_button_img = ctk.CTkImage(light_image=Image.open(".\\images\\download.png"), dark_image=Image.open(".\\images\\download.png"), size=(20, 20))
        download_button = ctk.CTkButton(right_frame, text="Download", image=download_button_img, fg_color="#3C6255", hover_color="green", anchor=tk.CENTER, corner_radius=10, command=lambda: [self.download(url_entry.get())])
        download_button.grid(row=2, column=0, sticky=tk.NS)

        self.mainloop()

    def load_youtube(self, link: str):
        try:
            if not "playlist" in link:
                self.select_all_videos_checkbox.deselect()
                self.download_progress_bar.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
                self.download_progress_bar.set(0)
                self.update_idletasks()
                self.yt = pytube.YouTube(link)
                self.thumbnail_img.configure(image=self.thumbnail_image)
                self.title_label.configure(text="")
                self.download_progress_bar.set(0.25)
                self.update_idletasks()
                self.videos_listbox.delete(0, tk.END)
                resolutions = "None"
                self.quality_options.configure(values=[resolutions])
                self.download_progress_bar.set(0.5)
                self.update_idletasks()
                self.videos_listbox.insert(0, self.yt.title)
                mp4_streams = self.yt.streams.filter(file_extension="mp4", mime_type="video/mp4").order_by("resolution")
                resolutions = {stream.resolution for stream in mp4_streams}
                self.quality_options.configure(values=resolutions)
                self.download_progress_bar.set(0.625)
                self.update_idletasks()

            else:
                self.select_all_videos_checkbox.deselect()
                self.download_progress_bar.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
                self.download_progress_bar.set(0)
                self.update_idletasks()
                self.yt = pytube.Playlist(link)
                self.thumbnail_img.configure(image=self.thumbnail_image)
                self.title_label.configure(text="")
                self.download_progress_bar.set(0.25)
                self.update_idletasks()
                self.videos_listbox.delete(0, tk.END)
                resolutions = "None"
                self.quality_options.configure(values=[resolutions])
                self.download_progress_bar.set(0.5)
                self.update_idletasks()
                num_of_videos = len(self.yt.videos)
                #merge below two loops
                for i, video in enumerate(self.yt.videos):
                    self.videos_listbox.insert(i, video.title)
                    self.download_progress_bar.set((0.5+(0.25*((i+1)/num_of_videos))))
                    self.update_idletasks()
                video_streams = []
                for video in self.yt.videos:
                    video_streams.append({stream.resolution for stream in video.streams.filter(file_extension="mp4", mime_type="video/mp4")})
                    self.update()
                resolutions = set.intersection(*video_streams)
                self.quality_options.configure(values=resolutions)
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
            self.after(200, self.download_progress_bar.place_forget)

            self.select_all_videos_checkbox.configure(state=tk.NORMAL)

        except pytube.exceptions.RegexMatchError:
            self.file_not_found_error_label.grid(row=2, column=0, sticky=tk.W)
            self.download_progress_bar.place_forget()

    def download(self, link: str):
        datatype = self.data_type_options.get()
        if not "playlist" in link:
            if datatype == "Video":
                video_stream = self.yt.streams.filter(res=self.quality_options.get(), file_extension="mp4").first()
                self.download_progress_bar.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
                self.download_progress_bar.set(0)
                self.update_idletasks()
                file_path = tk.filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"), mustexist=True)
                self.download_progress_bar.set(0.5)
                self.update_idletasks()
                try:
                    if ":" not in self.yt.title:
                        video_stream.download(output_path=file_path, filename=f"{self.yt.title}__VIDEO__{random.randint(0, 999999999)}.mp4")
                    else:
                        video_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__VIDEO__{random.randint(0, 999999999)}.mp4")
                except OSError:
                    video_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__VIDEO__{random.randint(0, 999999999)}.mp4")
                self.download_progress_bar.set(1)
                self.update_idletasks()
                self.download_progress_bar.place_forget()

            else:
                audio_streams = self.yt.streams.filter(only_audio=True)
                self.download_progress_bar.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
                self.download_progress_bar.set(0)
                self.update_idletasks()
                audio_stream = audio_streams.order_by("abr").last()
                file_path = tk.filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"), mustexist=True)
                self.download_progress_bar.set(0.5)
                self.update_idletasks()
                try:
                    if ":" not in self.yt.title:
                        audio_stream.download(output_path=file_path, filename=f"{self.yt.title}__AUDIO__{random.randint(0, 999999999)}.mp3")
                    else:
                        audio_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__AUDIO__{random.randint(0, 999999999)}.mp3")
                except OSError:
                    audio_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__AUDIO__{random.randint(0, 999999999)}.mp3")
                self.download_progress_bar.set(1)
                self.update_idletasks()
                self.download_progress_bar.place_forget()

        else:
            if datatype == "Video":
                resolution = self.quality_options.get()
                self.download_progress_bar.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
                self.download_progress_bar.set(0)
                self.update_idletasks()
                file_path = tk.filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"), mustexist=True)
                num_of_videos = len(self.videos_listbox.curselection())
                #no need to create YouTube object in this loop every time use self.ut.videos instead
                for i, url in enumerate(self.yt.video_urls):
                    if i in self.videos_listbox.curselection():
                        video = pytube.YouTube(url)
                        video_stream = video.streams.filter(res=resolution, file_extension="mp4").first()
                        try:
                            if ":" not in video.title:
                                video_stream.download(output_path=file_path, filename=f"{video.title}__VIDEO__{random.randint(0, 999999999)}.mp4")
                            else:
                                video_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__VIDEO__{random.randint(0, 999999999)}.mp4")

                        except OSError:
                            video_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__VIDEO__{random.randint(0, 999999999)}.mp4")
                    self.download_progress_bar.set((0+((i+1)/num_of_videos)))
                    self.update_idletasks()
                        
                self.download_progress_bar.place_forget()

            else:
                resolution = self.quality_options.get()
                self.download_progress_bar.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
                self.download_progress_bar.set(0)
                self.update_idletasks()
                file_path = tk.filedialog.askdirectory(initialdir=os.path.expanduser("~/Downloads"), mustexist=True)
                num_of_videos = len(self.videos_listbox.curselection())
                for i, url in enumerate(self.yt.video_urls):
                    #no need to create YouTube object in this loop every time use self.ut.videos instead
                    if i in self.videos_listbox.curselection():
                        video = pytube.YouTube(url)
                        audio_stream = video.streams.filter(only_audio=True).order_by("abr").last()
                        try:
                            if ":" not in video.title:
                                audio_stream.download(output_path=file_path, filename=f"{video.title}__VIDEO__{random.randint(0, 999999999)}.mp3")
                            else:
                                audio_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__AUDIO__{random.randint(0, 999999999)}.mp3")

                        except OSError:
                            audio_stream.download(output_path=file_path, filename=f"Tkinter_YouTubeDownloader_file__AUDIO__{random.randint(0, 999999999)}.mp3")
                    self.download_progress_bar.set((0+((i+1)/num_of_videos)))
                    self.update_idletasks()

                self.download_progress_bar.place_forget()

    def checkbox_clicked(self):
        if bool(self.select_all_videos_checkbox.get()):
            self.videos_listbox.selection_set(0, tk.END)
        else:
            self.videos_listbox.selection_clear(0, tk.END)

    def change_datatype(self, datatype: str):
        if datatype == "Video":
            self.video_option_label.grid(row=3, column=0, sticky=tk.W)
            self.quality_options.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)

        else:
            self.video_option_label.grid_forget()
            self.quality_options.grid_forget()

if __name__ == "__main__":
    YouTubeDownloader()
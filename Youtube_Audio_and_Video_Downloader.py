import platform, subprocess,tkinter, os, sys
from customtkinter import *
# from CTkMessagebox import CTkMessagebox
from pytube import *
import urllib

window = CTk()
window.resizable(False,False)
path_string =""
to_download = ""
# l=[]
# stream = pytube.query.StreamQuery(l)
# window.geometry("720x480")

window.title("Youtube audio & video Downloader")

set_appearance_mode("System")
set_default_color_theme("blue")

playlist_bitrates = {}
playlist_resolutions = {}

resolutions = []
bitrates = []

def audios(stream):
    yt_link_streams_audios = stream.filter(only_audio=True).order_by("abr").desc()
    bitrates=[]
    for i in yt_link_streams_audios:
        bitrates.append(i.abr)
    option_menu = CTkOptionMenu(master=window, variable=option_menu_var, values=bitrates).grid(row=1,column=2)
    option_menu_var.set(bitrates[0])
    notify_label_var.set("So you need audio :)")
    download_button = CTkButton(window, text="Download", command=lambda: download(stream, yt_link_streams_audios,bitrates)).grid(row=3, column=1)
def videos(stream):
    yt_link_streams_videos = stream.filter(progressive=True).order_by('resolution').desc()
    resolutions=[]
    for i in yt_link_streams_videos:
        resolutions.append(i.resolution)
    option_menu = CTkOptionMenu(master=window, variable=option_menu_var,values=resolutions).grid(row=1,column=2)
    option_menu_var.set(resolutions[0])
    notify_label_var.set("So you need video :)")
    download_button = CTkButton(window, text="Download", command=lambda: download(stream,yt_link_streams_videos,resolutions)).grid(row=3, column=1)
def path_select():
    notify_label_var.set("Choosing folder...")
    tkinter.messagebox.showinfo("Sure", "I just want to note you that, I will skip downloading\n\nfiles which you already have in the selected path\n\nSo make sure to give proper path")
    path_string = filedialog.askdirectory(initialdir=os.getcwd())
    # path_string = filedialog.askdirectory()
    if path_string =="":
        notify_label_var.set("no output folder")
        tkinter.messagebox.showinfo("no path", "please choose the path")
    else:
        notify_label_var.set("folder chosen")
    #path can be given like below also
    #path_string = filedialog.askdirectory(initialdir="C:/Users/JSRSPSM225/Downloads")
    #If I directly click on download without clicking on browse to choose the path then the video/audio will be downloaded to environment folder we created i.e., in summer_project here
    #That's why I activated
    path_variable.set(path_string)
def reset():
    enter_url = CTkLabel(window, text="Enter URL:").grid(row=0, column=0)
    link_pasted.set("")
    link_entry = CTkEntry(window, textvariable=link_pasted, placeholder_text="Paste the link").grid(row=0, column=1,pady=20)
    fetch = CTkButton(window, text="Fetch", command=category).grid(row=0, column=2, pady=20)
    typess = StringVar()
    audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio", state=DISABLED).grid(row=1, column=0)
    video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video", state=DISABLED).grid(row=1, column=1)
    option_menu = CTkOptionMenu(master=window, variable=option_menu_var, values=[], state=DISABLED).grid(row=1, column=2)
    option_menu_var.set("")
    download_button = CTkButton(window, text="Download", state=DISABLED).grid(row=3, column=1)
    path_variable.set("")
    notify_label_var.set("(: Have a Download :)")
def reset_after_download(stream,media_info):
    audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio", command=lambda :audios(stream)).grid(row=1,column=0)
    video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video", command=lambda :videos(stream)).grid(row=1,column=1)
    option_menu = CTkOptionMenu(master=window, variable=option_menu_var, values=media_info).grid(row=1,column=2)
    option_menu_var.set(media_info[0])
    notify_label_var.set("Go for other download")

def download(stream, info, media_info):
    # download = YouTube(link_pasted.get()).streams.get_by_resolution(option_menu_var.get()).download(path_variable.get())
    #the above one wont't work... giving error as NoneType has not attribute download
    if path_variable.get()=='':
        notify_label_var.set("no output folder")
        tkinter.messagebox.showinfo("No path","please choose the path")
    else:
        notify_label_var.set("Hurray! Downloading...")
        if(typess.get()=='video'):
            #giving error as NoneType object has no attribute download...
            #Solution from https://github.com/pytube/pytube/issues/908 --> This issue is due to YouTubes new non progressive format
            # print(option_menu_var.get())
            # print(type(option_menu_var.get()))
            # print(type(stream.get_by_resolution(option_menu_var.get())))
            # download = stream.get_by_resolution(option_menu_var.get())
            # info = stream.filter(progressive=True).order_by('resolution').desc()
            for i in info:
                if i.resolution == option_menu_var.get():
                    download = stream.get_by_itag(i.itag)
                    # if os.path.join(path_variable.get()+"\\"+YouTube(link_pasted.get()).title) in os.listdir(path_variable.get()):
                    if download.default_filename in os.listdir(path_variable.get()):
                        notify_label_var.set("already there...")
                        tkinter.messagebox.showinfo("already exists",f"Already filename exists in {path_variable.get()} folder\n\nIf you need to download other video click on reset to paste link")
                    else:
                        download.download(path_variable.get())
                        notify_label_var.set("Downloaded...")
                        tkinter.messagebox.showinfo("video download done",f"Downloaded to {path_variable.get()} \n\n Title: {download.default_filename}\n\nIf you need to download other video click on reset to paste link")
                    break
            # if(path_variable.get()+"\\"+YouTube(link_pasted.get())+download.mime_type.split("/")[-1] in os.listdir(path_string)):
            #     CTkMessagebox(message="Already Downloaded",icon='info')
            # else:
            #     download.download(path_variable.get())
            #     CTkMessagebox(message=f"Video dowloaded to {path_variable.get()}", icon='info')
            reset_after_download(stream,media_info)
        else:
            # info = stream.filter(only_audio=True).order_by('abr').desc()
            for i in info:
                if(i.abr==option_menu_var.get()):
                    download = stream.get_by_itag(i.itag)
                    bitrate =""
                    for k in i.abr:
                        if k.isdigit():
                            bitrate += k
                    if download.default_filename.split(".")[0]+".mp3" in os.listdir(path_variable.get()):
                        notify_label_var.set("already there")
                        tkinter.messagebox.showinfo("already exits",f"Already downloaded in {path_variable.get()} folder\n\nIf you need to download other video click on reset to paste link")
                    else:
                        if "ffmpeg.exe" in os.listdir():
                            path = f'{path_variable.get()}\\{download.default_filename.split(".")[0]}_audio-bitrate-{i.abr}.mp3'
                            download.download(filename=path)
                            input = hide_file(path)
                            output = f'{path_variable.get()}\\{download.default_filename.split(".")[0]}.mp3'
                            notify_label_var.set("converting to mp3")
                            subprocess.run(['ffmpeg','-i',f'{input}','-b:a', f'{bitrate}k', f'{output}'],shell=True)
                            os.remove(input)
                            notify_label_var.set("audio downloaded...")
                            tkinter.messagebox.showinfo("audio download done",f"Downloaded to {path_variable.get()} \n Title: {download.default_filename.split('.')[0]}.mp3\n\nIf you need to download other video click on reset to paste link")
                        else:
                            result = tkinter.messagebox.askyesno("No ffmpeg","ffmpeg.exe and the application you are running now, should be in the same folder. Then only, mp3 audio file which is compatible for all systems, will be downloaded. If you want me to download mp3 file, even if it wasn't compatible with other systems, you can click on YES otherwise click on NO to exit the application")
                            if result:
                                file_name = path_variable.get()+'\\'+download.default_filename.split('.')[0]+'.mp3'
                                download.download(filename=file_name)
                                tkinter.messagebox.showinfo("audio download done", f"Downloaded to {path_variable.get()} \n Title: {download.default_filename.split('.')[0]}.mp3\n\nIf you need to download other video click on reset to paste link")
                            else:
                                sys.exit()
                    break
            # if(stream.get_by_itag(itag).default_filename in (os.listdir(path_variable.get()) or os.listdir("C:\\Users\\JSRSPSM225\\Downloads")):
            #     CTkMessagebox(message="Already audio downloaded in the path "+path_string)
            # else:
            #     stream.get_by_itag(itag).download(path_variable.get())
            # CTkMessagebox(message=f"Audio dowloaded to {path_variable.get()}", icon='info')
            reset_after_download(stream,media_info)

def hide_file(path):
    if platform.system()=="Windows":
        os.system(f"attrib +h {path}")
        return path
    else:
        path = os.path.dirname(path)+"\\."+os.path.basename(path)
        return path
def pl_video_download(pl):
    if path_variable.get()=='':
        notify_label_var.set("no output folder")
        tkinter.messagebox.showinfo("No path","please choose the path")
    else:
        notify_label_var.set("Downloading...")
        now=0
        total=len(pl.videos)
        if to_download=="high_video":
            for video in pl.videos:
                now+=1
                filtered_videos = video.streams.filter(progressive=True)
                if path_variable.get() + '\\' + filtered_videos.get_highest_resolution().default_filename in os.listdir(path_variable.get()):
                    # notify_label_var.set(f"already there - {now}/{total}")
                    pass
                else:
                    # notify_label_var.set(f"Downloading - {now}/{total}")
                    filtered_videos.get_highest_resolution().download(path_variable.get())
            # notify_label_var.set("Download done")
        elif to_download == "low_video":
            for video in pl.videos:
                now+=1
                filtered_videos = video.streams.filter(progressive=True)
                if path_variable.get() + '\\' + filtered_videos.get_lowest_resolution().default_filename in os.listdir(path_variable.get()):
                    pass
                    # notify_label_var.set(f"already there - {now}/{total}")
                else:
                    print("Downloading low")
                    # notify_label_var.set(f"Downloading - {now}/{total}")
                    filtered_videos.get_lowest_resolution().download(path_variable.get())
            # notify_label_var.set("Download done")
        else:
            for video in pl.videos:
                now+=1
                filtered_videos = video.streams.filter(progressive=True)
                for i in filtered_videos:
                    if i.resolution == option_menu_var.get():
                        if path_variable.get() + '\\' + filtered_videos.get_by_itag(i.itag).default_filename in os.listdir(path_variable.get()):
                            pass
                            # notify_label_var.set(f"already there - {now}/{total}")
                        else:
                            # notify_label_var.set(f"Downloading - {now}/{total}")
                            filtered_videos.get_by_itag(i.itag).download(path_variable.get())
                        break
        notify_label_var.set("Download done")
        tkinter.messagebox.showinfo("Download done",f"Downloaded all videos to '{path_variable.get()}' folder.\n\nIf you want to paste other link click on reset and then paste it")
        # reset()
def pl_audio_download(pl):
    if path_variable.get()=='':
        notify_label_var.set("no output folder")
        tkinter.messagebox.showinfo("No path","please choose the path")
    else:
        notify_label_var.set("Downloading...")
        now=0
        boolean_value = True
        total=len(pl.videos)
        if to_download == "just_audio":
            for audio in pl.videos:
                now+=1
                filtered_audio = audio.streams.get_audio_only()
                if filtered_audio.default_filename.split(".")[0] + ".mp3" in os.listdir(path_variable.get()):
                    # notify_label_var.set(f"already there - {now}/{total}")
                    pass
                else:
                    if "ffmpeg.exe" in os.listdir():
                        path = f'{path_variable.get()}\\{filtered_audio.default_filename.split(".")[0]}_audio.mp3'
                        # notify_label_var.set(f"Downloading - {now}/{total}")
                        filtered_audio.download(filename=path)
                        input = hide_file(path)
                        output = f'{path_variable.get()}\\{filtered_audio.default_filename.split(".")[0]}.mp3'
                        # notify_label_var.set(f"converting {now}/{total} to mp3")
                        subprocess.run(['ffmpeg', '-i', f'{input}', f'{output}'], shell=True)
                        os.remove(input)
                    else:
                        if boolean_value:
                            result = tkinter.messagebox.askyesno("No ffmpeg", "ffmpeg.exe and the application you are running now, should be in the same folder. Then only, mp3 audio file which is compatible for all systems, will be downloaded. If you want me to download mp3 file, even if it wasn't compatible with other systems, you can click on YES otherwise click on NO to exit the application")
                            boolean_value = False
                        if result:
                            file_name = path_variable.get() + '\\' + filtered_audio.default_filename.split('.')[0] + '.mp3'
                            filtered_audio.download(filename=file_name)
                        else:
                            sys.exit()
            notify_label_var.set("Download done")
        else:
            for audio in pl.videos:
                now+=1
                filtered_audios = audio.streams.filter(only_audio=True)
                bitrate = ""
                for i in filtered_audios:
                    if i.abr == option_menu_var.get():
                        download = filtered_audios.get_by_itag(i.itag)
                        if download.default_filename.split(".")[0]+".mp3" in os.listdir(path_variable.get()):
                            # notify_label_var.set(f"already there - {now}/{total}")
                            pass
                        else:
                            if "ffmpeg.exe" in os.listdir():
                                path = f'{path_variable.get()}\\{download.default_filename.split(".")[0]}_audio-bitrate-{i.abr}.mp3'
                                # notify_label_var.set(f"Downloading - {now}/{total}")
                                download.download(filename=path)
                                input = hide_file(path)
                                output = f'{path_variable.get()}\\{download.default_filename.split(".")[0]}.mp3'
                                # notify_label_var.set(f"converting {now}/{total} to mp3")
                                subprocess.run(['ffmpeg', '-i', f'{input}', '-b:a', f'{bitrate}k', f'{output}'], shell=True)
                                os.remove(input)
                            else:
                                if boolean_value:
                                    result = tkinter.messagebox.askyesno("No ffmpeg",
                                                                         "ffmpeg.exe and the application you are running now, should be in the same folder. Then only, mp3 audio file which is compatible for all systems, will be downloaded. If you want me to download mp3 file, even if it wasn't compatible with other systems, you can click on YES otherwise click on NO to exit the application")
                                    boolean_value = False
                                if result:
                                    file_name = path_variable.get() + '\\' + download.default_filename.split('.')[0] + '.mp3'
                                    download.download(filename=file_name)
                                else:
                                    sys.exit()
                        break
            notify_label_var.set("Download done")
        tkinter.messagebox.showinfo("Download done",f"Downloaded all audios to '{path_variable.get()}' folder.\n\nIf you want to paste other link click on reset and then paste it")
def pl_audios(bitrates):
    notify_label_var.set("audios chosen")
    option_menu = CTkOptionMenu(master=window,variable=option_menu_var, values=bitrates).grid(row=1,column=2)
    download_button = CTkButton(window,text="Download",command = lambda : pl_audio_download(Playlist(link_pasted.get()))).grid(row=3,column=1)
    option_menu_var.set(bitrates[0])
def pl_videos(resolutions):
    notify_label_var.set("videos chosen")
    option_menu = CTkOptionMenu(master=window,variable=option_menu_var, values=resolutions).grid(row=1,column=2)
    download_button = CTkButton(window, text="Download", command=lambda: pl_video_download(Playlist(link_pasted.get()))).grid(row=3, column=1)
    option_menu_var.set(resolutions[0])

# playlist address : https://youtube.com/playlist?list=PLT9GosF8FryFDFq7amBthI7Z0_q7N2NmB
def play_list_check(playlist):
    notify_label_var.set("checking formats")
    count = 0
    for media in playlist.videos:
        count += 1
        stream_1 = media.streams.filter(progressive = True).order_by('resolution').desc()
        stream_2 = media.streams.filter(only_audio=True).order_by('abr').desc()
        for i in stream_1:
            if i.resolution not in playlist_resolutions:
                playlist_resolutions[i.resolution] = 1
            else:
                playlist_resolutions[i.resolution] +=1
        for i in stream_2:
            if i.abr not in playlist_bitrates:
                playlist_bitrates[i.abr] = 1
            else:
                playlist_bitrates[i.abr] +=1
    resolutions = [i for i in playlist_resolutions if playlist_resolutions[i] == len(playlist.videos)]
    bitrates = [i for i in playlist_bitrates if playlist_bitrates[i] == len(playlist.videos)]

    # if resolutions != []:
    #     video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video",command=lambda: pl_videos(resolutions)).grid(row=1, column=1)
    # else:
    #     def choose_alternate_video():
    #         top_level_1.destroy()
    #         typess.set("video")
    #         if alternate.get()=="low_video":
    #             to_download ="low_video"
    #         else:
    #             to_download = "high_video"
    #     def resetting():
    #         top_level_1.destroy()
    #         reset()
    #     def submit_activate():
    #         CTkButton(top_level_1, text="submit",command=choose_alternate_video).grid(row=3,column=0,pady=20)
    #     top_level_1 = CTk()
    #     top_level_1.title("No common video resolution")
    #     top_level_1.protocol("WM_DELETE_WINDOW", lambda : exit_program(top_level_1))
    #     CTkLabel(top_level_1, text="\n\nThere are no common video resolutions available to download").grid(row=0, column=0,columnspan=3)
    #     alternate = StringVar()
    #     CTkRadioButton(top_level_1, text= "Shall I download all low resolution videos",value="low_video", variable=alternate, command=submit_activate).grid(row=1, column=0, columnspan=3, pady=20)
    #     CTkRadioButton(top_level_1, text="Shall I download all high resolution videos", value="high_video", variable=alternate,command=submit_activate).grid(row=2, column=0, columnspan=3)
    #     CTkButton(top_level_1, text="submit", state=DISABLED).grid(row=3, column=0, pady=20)
    #     CTkButton(top_level_1, text="exit application", state=sys.exit).grid(row=3, column=1)
    #     CTkButton(top_level_1, text="reset", state=resetting).grid(row=2, column=2)
    #     # CTkMessagebox(message="No common quality identified to download video...\nShall I download the highest resolution video", icon='warning')
    #     # video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video",state=DISABLED).grid(row=1, column=1)
    # if bitrates !=[]:
    #     audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio",command = lambda : pl_audios(bitrates)).grid(row=1,column=0)
    # else:
    #     def choose_alternate_audio():
    #         top_level_2.destroy()
    #         typess.set("audio")
    #     def resetting():
    #         top_level_2.destroy()
    #         reset()
    #     def submit_activate():
    #         CTkButton(top_level_2, text="submit",command=choose_alternate_audio).grid(row=2,column=0)
    #     top_level_2 = CTk()
    #     top_level_2.title("No common video resolution")
    #     top_level_2.protocol("WM_DELETE_WINDOW", lambda : exit_program(top_level_2))
    #     CTkLabel(top_level_2, text="There are no common audio bitrartes available to download").grid(row=0, column=0,columnspan=3,pady=20)
    #     alternate = StringVar()
    #     CTkRadioButton(top_level_2, text="Shall I download audios of entire playlist without checking for common bitrate",value="just_audio", variable=alternate, command=submit_activate).grid(row=1,column=0,columnspan=3)
    #     CTkButton(top_level_1, text="submit", state=DISABLED).grid(row=2, column=0, pady=20)
    #     CTkButton(top_level_1, text="exit application", state=sys.exit).grid(row=2, column=1)
    #     CTkButton(top_level_1, text="reset", state=resetting).grid(row=2, column=2)
    #
    #     # CTkMessagebox(message="No common quality identified for download audio...\nShall I download the audio that I identified", icon='warning')
    #     # tkinter.messsagebox.askyesno("No common audio bitrate available", "No common quality identified for download audio...\nShall I download th/e audio that I identified?")
    #     # audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio",state=DISABLED).grid(row=1, column=0)
    # print("after if")
    if resolutions != [] and bitrates!=[]:
        notify_label_var.set("Choose audio/video")
        video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video",
                                     command=lambda: pl_videos(resolutions)).grid(row=1, column=1)
        audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio",
                                     command=lambda: pl_audios(bitrates)).grid(row=1, column=0)
    elif resolutions!=[] and bitrates==[]:
        notify_label_var.set("video only available")
        video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video",command=lambda: pl_videos(resolutions)).grid(row=1, column=1)
        tkinter.messagebox.showinfo("no common bitrate","There is no common bitrate available for audio to download\n\nIf you need to download only audio from the playlist click on RESET\n\nthen choose other option in the dialog box which was opened before")
    elif resolutions == [] and bitrates != []:
        notify_label_var.set("audio only available")
        tkinter.messagebox.showinfo("no common resolution", "There is no common resolution available for video to download\n\nIf you need to download only video from the playlist click on RESET\n\nthen choose other option in the dialog box which was opened before")
        audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio",command=lambda: pl_audios(bitrates)).grid(row=1, column=0)
    else:
        notify_label_var.set("No common formats")
        tkinter.messagebox.showinfo("nothing common","No common video resolutions or audio bitrates available\n\nIf you need to from the audios or videos from playlist click on RESET\n\nThen choose other option in the dialog box which was opened before")
def exit_program(top_level):
    result = tkinter.messagebox.askyesno("exit","Are you sure to exit the application?")
    if result:
        top_level.destroy()
        sys.exit()
    else:
        return

# video address : https://www.youtube.com/watch?v=RVLNBVK8auM
def pl_check(playlist):
    for i in playlist.videos:
        break
def category():
    if link_pasted.get() != "":
        # notify_label_var.set("Fetching")
        try:
            yt_link = link_pasted.get()
            yt_object_streams = YouTube(yt_link).streams
            notify_label_var.set("Fetched...")
            fetch = CTkButton(window, text="Fetch", command=category, state=DISABLED).grid(row=0, column=2, pady=20)
            link_entry = CTkEntry(window,textvariable=link_pasted,placeholder_text="Paste the link",state='readonly').grid(row=0,column=1,pady=20)
            audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio", command=lambda :audios(yt_object_streams)).grid(row=1, column=0)
            video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video", command=lambda :videos(yt_object_streams)).grid(row=1, column=1)
        except Exception as e:
            # print(e)
            try:
                pl_check(Playlist(link_pasted.get()))
                fetch = CTkButton(window, text="Fetch", command=category, state=DISABLED).grid(row=0, column=2, pady=20)
                link_entry = CTkEntry(window, textvariable=link_pasted, placeholder_text="Paste the link",state='readonly').grid(row=0, column=1, pady=20)
                notify_label_var.set("Fetched...")
                def top_level_result(top_level):
                    notify_label_var.set("type chosen")
                    global to_download
                    to_download = way.get()
                    if way.get() == "high_video" or way.get()=="low_video":
                        top_level.destroy()
                        typess.set("video")
                        fetch = CTkButton(window, text="Fetch", state=DISABLED).grid(row=0, column=2,pady=20)
                        download_button = CTkButton(window, text="Download", command=lambda: pl_video_download(Playlist(link_pasted.get()))).grid(row=3, column=1)
                        # typess = StringVar()
                        # audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio",state=DISABLED).grid(row=1, column=0)
                        # video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video",state=DISABLED).grid(row=1, column=1)
                    elif way.get() == "just_audio":
                        top_level.destroy()
                        typess.set("audio")
                        fetch = CTkButton(window, text="Fetch", state=DISABLED).grid(row=0, column=2, pady=20)
                        download_button = CTkButton(window, text="Download", command=lambda: pl_audio_download(Playlist(link_pasted.get()))).grid(row=3, column=1)
                    elif way.get()=="check_res_bitrate":
                        top_level.destroy()
                        fetch = CTkButton(window, text="Fetch", state=DISABLED).grid(row=0, column=2, pady=20)
                        play_list_check(Playlist(link_pasted.get()))
                def submit_activate():
                    CTkButton(top_level, text="submit", command=lambda: top_level_result(top_level)).grid(row=5,column=0)
                top_level = CTkToplevel()
                top_level.protocol("WM_DELETE_WINDOW", lambda :exit_program(top_level))
                top_level.title("Choose how to download")
                way = StringVar()
                # available in playlist
                CTkLabel(top_level, text="\n\n\nYou have given playlist link\n\nChoose what you want to download").grid(row=0,column=0)
                CTkRadioButton(top_level, text= "download all low resolution videos",value="low_video", variable=way, command=submit_activate).grid(row=1,column=0,pady=20)
                CTkRadioButton(top_level,text="download all high resolution videos", value="high_video", variable=way,command=submit_activate).grid(row=2,column=0)
                CTkRadioButton(top_level,text="Check for common audio and video formats", value="check_res_bitrate", variable=way,command=submit_activate).grid(row=3,column=0,pady=20,padx=20)
                CTkRadioButton(top_level, text="just download audios from playlist", value="just_audio", variable=way,command=submit_activate).grid(row=4,column=0)
                CTkButton(top_level, text="submit", state=DISABLED).grid(row=5,column=0,pady=20)
                # play_list_check(Playlist(link_pasted.get()))
            except Exception as k:
                #So it's not a playlist or a youtube video..."
                # video url:
                 # https://www.youtube.com/watch?v=8tea0uI4d2A
                # print(e)    -->     <urlopen error [Errno 11001] getaddrinfo failed>
                # print(type(e))  --> <class 'urllib.error.URLError'>
                # to check whether it is a network error i need to import urllib and pass "<urlopen error [Errno 11001] getaddrinfo failed>" as an argument to "urllib.error.URLError()" then "type(urllib.error.URLError("<urlopen error [Errno 11001] getaddrinfo failed>"))==type(e)"
                # print(k)
                if type(urllib.error.URLError("<urlopen error [Errno 11001] getaddrinfo failed>"))==type(e):
                    tkinter.messagebox.showerror("URL error", "Might be network issue, please check your internet connection")
                else:
                    tkinter.messagebox.showerror("invalid", f"Give valid link\n\n{e}")

                notify_label_var.set("(: Have a Download :)")
    else:
        tkinter.messagebox.showwarning("give link","Give link and then click on fetch button")
    # else:
    #     CTkMessagebox(message="Network error",icon="warning")

enter_url = CTkLabel(window, text="Enter URL:").grid(row=0, column=0)

link_pasted = StringVar()
link_entry = CTkEntry(window,textvariable=link_pasted, placeholder_text="Paste the link").grid(row=0,column=1,pady=20)

fetch = CTkButton(window,text="Fetch", command=category).grid(row=0,column=2,pady=20)

typess = StringVar()
audio_radio = CTkRadioButton(window, variable=typess, text="Audio", value="audio", state=DISABLED).grid(row=1, column=0)
video_radio = CTkRadioButton(window, variable=typess, text="Video", value="video", state=DISABLED).grid(row=1, column=1)

option_menu_var = StringVar()
option_menu = CTkOptionMenu(master=window,variable=option_menu_var, values=[],state=DISABLED).grid(row=1,column=2)

enter_path = CTkLabel(window, text="Choose path:").grid(row=2, column=0)
path_variable = StringVar()
path_text = CTkEntry(window,placeholder_text="for path click on browse",textvariable=path_variable,state=DISABLED).grid(row=2,column=1,pady=20)

path_button = CTkButton(window,text="Browse",command=path_select).grid(row=2,column=2)

exit_button = CTkButton(window,text="Exit",command=window.destroy).grid(row=3,column=0,padx=5)
download_button = CTkButton(window,text="Download",state=DISABLED).grid(row=3,column=1)
reset_button = CTkButton(window,text="Reset",command=reset).grid(row=3,column=2,padx=5)

# downloading_label_1 = CTkLabel(window,text="Have a download",justify='center').grid(row=4,column=1,pady=20)
# .place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
notify_label_var = StringVar()
notify_label = CTkEntry(window,textvariable=notify_label_var,state=DISABLED).grid(row=4,column=0,columnspan=3,pady=20)
notify_label_var.set("(: Have a Download :)")
#mainloop to perceive actions
window.mainloop()
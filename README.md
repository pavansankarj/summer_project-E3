# summer_project-E3

Let's see the proposed method...

I have proposed a desktop application designed to download audio or videos with customized bitrates and resolutions, catering to individual preferences and it also streamline the process of 
downloading YouTube playlists while minimizing user effort. Upon launching the application, a window appears, prompting the user to input the desired YouTube link for downloading audio or
video content. After clicking the "Fetch" button, the application intelligently determines whether the input corresponds to a playlist or a single video. In cases where a single video is detected, the
interface activates the audio and video buttons, granting access to a dropdown list of available bitrates and resolutions. Upon selecting the desired options, clicking the "Download" button
initiates the download process, storing the video or audio in the specified file path. However, it's worth noting that the downloaded audio may initially be concealed, as it is acquired in the MP4
or webm container format commonly preferred by YouTube. Subsequently, the application employs the ffmpeg command-line tool to convert the audio into the universally supported MP3
format, making it visible and compatible with a wide array of systems. If the provided link leads to a playlist, the application presents users with various options. These options include the ability
to download all high-resolution or low-resolution videos, exclusively download audio from the playlist, or analyze common video resolutions and audio bitrates shared among all playlist videos.
Based on user preferences, the chosen settings are applied. Upon clicking the "Download" button, the application seamlessly downloads the complete playlist, saving the files in the designated
path. This application effectively simplifies the process of downloading YouTube content, ensuring efficient playlist downloads and personalized audio/video downloads with minimal manual intervention.

Note: To download audio from this application and to convert it into proper .mp3 file you need to download the zip file of ffmpeg from this link: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
and need to place the file "ffmpeg.exe" of it in the same path i.e., in the same folder at which you place this "Youtube_Audio_and_Video_Downloader.exe" application.

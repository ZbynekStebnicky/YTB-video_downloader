import os
import subprocess
import re
from moviepy.editor import VideoFileClip, AudioFileClip

def sanitize_filename(filename):
    # Replacing not allowed symbols with _
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def download_highest_quality_video_and_audio(url, output_path, username, password):
    # Creating adress path if not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Getting video title by yt-dlp
    print("Getting video title by yt-dlp...")
    title_command = [
        "yt-dlp",
        "--username", username,
        "--password", password,
        "--get-title",
        url
    ]
    title_result = subprocess.run(title_command, capture_output=True, text=True)
    video_title = title_result.stdout.strip()
    sanitized_title = sanitize_filename(video_title)

    # Setting file names
    video_file = os.path.join(output_path, f"{sanitized_title}_video.mp4")
    audio_file = os.path.join(output_path, f"{sanitized_title}_audio.m4a")
    final_file = os.path.join(output_path, f"{sanitized_title}.mp4")

    print("Downloading video and audio by yt-dlp...")

    video_command = [
        "yt-dlp",
        "--username", username,
        "--password", password,
        "-f", "bestvideo[ext=mp4]",
        "-o", video_file,
        url
    ]
    
    audio_command = [
        "yt-dlp",
        "--username", username,
        "--password", password,
        "-f", "bestaudio[ext=m4a]",
        "-o", audio_file,
        url
    ]

    # Downloading video and audio
    subprocess.run(video_command)
    subprocess.run(audio_command)

    print("Combining video and audio...")

    # Combining video and audio by moviepy
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(final_file, codec="libx264", audio_codec="aac")

    print("Program finished")

# Enter video URL
url = input("Enter video URL: ")
# Specifie output adress
output_path = "downloaded files"
# Enter youtube username (gmail) and password
username = input("Enter youtube username (gmail): ")
password = input("Enter password: ")

download_highest_quality_video_and_audio(url, output_path, username, password)

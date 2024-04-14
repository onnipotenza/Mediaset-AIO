import os
import json
import subprocess
from modules.logo import logo

def download_video_from_m3u8(m3u8_link, output_file):
    command = [
        'drivers/ffmpeg',
        '-i', m3u8_link,
        '-c', 'copy',
        output_file
    ]
    subprocess.run(command)

def download():
    logo()
    # Step 1: Check inside the folder output/links for JSON files containing video_link
    json_files = [file for file in os.listdir("output/links") if file.endswith(".json")]
    video_files = []

    for file in json_files:
        with open(os.path.join("output/links", file), "r") as json_file:
            data = json.load(json_file)
            if any("video_link" in episode for episode in data.get("links", [])):
                video_files.append(file)

    # Step 2: Print all the names replacing underscores with spaces
    if not video_files:
        print("No JSON files with video links found.")
        return

    print("Available files:")
    for i, file in enumerate(video_files, start=1):
        print(f"{i}. {file.replace('_', ' ').replace('.json', '')}")

    # Step 3: User selects a file
    selection = input("Enter the number corresponding to the file you want to download: ")
    try:
        selection_index = int(selection) - 1
        selected_file = video_files[selection_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Check if the selected file exists
    selected_file_path = os.path.join("output/links", selected_file)
    if not os.path.exists(selected_file_path):
        print("Selected file does not exist.")
        return

    # Create a folder for the downloaded videos
    output_folder = os.path.join("output/videos", selected_file.replace(".json", ""))
    os.makedirs(output_folder, exist_ok=True)

    # Step 4: Ask the user from which episode to start
    start_episode = input("Enter the starting episode number (default is 1): ")
    try:
        start_episode = int(start_episode)
    except ValueError:
        start_episode = 1

    # Step 5: Ask the user how many episodes to download
    num_episodes = input("Enter the number of episodes to download (default is all): ")
    try:
        num_episodes = int(num_episodes)
    except ValueError:
        num_episodes = None

    # Step 6: Download and name the episodes
    with open(selected_file_path, "r") as json_file:
        data = json.load(json_file)

    print("Downloading videos...")
    for episode in data["links"]:
        if "video_link" in episode:
            episode_number = episode["episode"]
            if episode_number >= start_episode and (num_episodes is None or episode_number < start_episode + num_episodes):
                video_link = episode["video_link"].split("\n")[0]  # Take only the first link
                output_file = os.path.join(output_folder, f"ep{episode_number}.mp4")
                download_video_from_m3u8(video_link, output_file)
                print(f"Episode {episode_number} downloaded.")

    print("Videos downloaded successfully.")

if __name__ == "__main__":
    download_videos()

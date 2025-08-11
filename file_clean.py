import os
from dotenv import load_dotenv
import json

import imagehash
from PIL import Image
from collections import defaultdict

import subprocess

import keyboard

load_dotenv()
# folder_path = os.getenv('DISCORD_IMAGES_PATH')
image_folder_path = os.getenv('IMAGE_PATH')
video_folder_path = os.getenv('VIDEO_PATH')
folder_path = os.getenv('FILE_PATH')
temp_path = os.getenv('TEMP')

# image_hash_map = defaultdict(list)
image_hashes = {}
image_dupes = []
video_hashes = {}
video_dupes = []
random_files = []

def output_json(data, name):
    json_str = json.dumps(data, indent=4)
    with open(name + ".json", "w") as f:
        f.write(json_str)

def extract_frame(video_path, output_image_path, timestamp=5):
    command = [
        'ffmpeg',
        '-ss', str(timestamp),
        '-i', video_path,
        '-frames:v', '1',
        '-q:v', '2',
        '-y',
        output_image_path
    ]

    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Frame extracted: {output_image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frame: {e}")

def hash_image(image_path):
    try:
        with Image.open(image_path) as img:
            return imagehash.phash(img)
    except Exception as e:
        print(f"Hashing error: {image_path} - {e}")
        return None

def remove_duplicate_files():
    files = os.listdir(folder_path)
    n = len(files)

    for filename in files:
        path = os.path.join(folder_path, filename)

        if filename[:7] == 'pokemon':
            random_files.append(path)

        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            try:
                hash_val = hash_image(path)
                if hash_val in image_hashes:
                    image_dupes.append(path)
                else:
                    image_hashes[hash_val] = filename
            except:
                continue

        elif filename.lower().endswith(('.mp4', '.mov', '.webm', '.gif')):
            frame_path = os.path.join(temp_path, f"{os.path.splitext(filename)[0]}.jpg")

            extract_frame(path, frame_path)
            hash_val = hash_image(frame_path)
            if hash_val in video_hashes:
                video_dupes.append(path)
            else:
                video_hashes[hash_val] = filename
        else:
            random_files.append(path)

    print('-' * 20)
    print(f"{n} Total Files Found.")
    print(f'Found {len(image_hashes)} unique images, {len(video_hashes)} unique videos.')
    print(f'Found {len(image_dupes)} images dupes, {len(video_dupes)} videos dupes and {len(random_files)} Random Files.')

    delete_files()
    move_files()
    save_files()

def move_files():
    for image_file in image_hashes.values():
        old_path = os.path.join(folder_path, image_file)
        new_path = os.path.join(image_folder_path, image_file)
        os.rename(old_path, new_path)

    for video_file in video_hashes.values():
        old_path = os.path.join(folder_path, video_file)
        new_path = os.path.join(video_folder_path, video_file)
        print(old_path, new_path)
        os.rename(old_path, new_path)

def delete_files():
    print('-' * 20)
    print("Press 'd' to delete these duplicates.")
    print("Press 'x' to not delete anything.")

    while True:
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'd':
                print("Now press Enter to confirm...")
                keyboard.wait('enter')  # Waits until Enter is pressed
                print("You pressed Enter!")

                print("You pressed 'd' => Deleting Dupes")
                for name in image_dupes:
                    file = os.path.join(folder_path, name)
                    os.remove(file)
                print("Image dupes deleted!")
                for name in video_dupes:
                    file = os.path.join(folder_path, name)
                    os.remove(file)
                print("Video dupes deleted!")
                for p in random_files:
                    os.remove(p)
                print("Random Files deleted!")
                break
            if event.name == 'x':
                print("You pressed 'x' => Process Stopped")
                break

def save_files():
    output_json(list(image_hashes.values()), 'image_names')
    output_json(list(video_hashes.values()), 'video_names')
    print('Image and video names saved')

remove_duplicate_files()
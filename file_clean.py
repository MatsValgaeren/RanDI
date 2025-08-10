import os
from dotenv import load_dotenv

import imagehash
from PIL import Image
from collections import defaultdict

import subprocess

import keyboard

load_dotenv()
folder_path = r"C:\Users\matsv\Desktop\RanDI\assets\download_images"
# folder_path = os.getenv('IMAGE_PATH')
temp_path = os.getenv('TEMP')

image_hash_map = defaultdict(list)
video_hashes = {}
random_files = []

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

    for filename  in files:
        path = os.path.join(folder_path, filename)

        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            try:
                hash_val = hash_image(path)
                if hash_val:
                    image_hash_map[str(hash_val)].append(path)
            except:
                continue

            for hash_val, paths in image_hash_map.items():
                if len(paths) > 1:
                    print(f"Duplicate group ({len(paths)} images):")
                    for p in paths:
                        print("  ", p)

        elif filename.lower().endswith(('.mp4', '.mov', '.webm', '.gif')):
            frame_path = os.path.join(temp_path, f"{os.path.splitext(filename)[0]}.jpg")

            extract_frame(path, frame_path)
            h = hash_image(frame_path)
            if h:
                video_hashes[filename] = h
        else:
            random_files.append(path)

    checked = set()
    for name1, hash1 in video_hashes.items():
        for name2, hash2 in video_hashes.items():
            if name1 == name2 or (name2, name1) in checked:
                continue
            distance = abs(hash1 - hash2)
            if distance <= 5:
                print(f"Similar videos: {name1} and {name2} (distance: {distance})")
            checked.add((name1, name2))

    print('-' * 20)
    print(f"{n} Total Files Found.")
    print(f'Found {len(image_hash_map)} Image Dupes, {len(video_hashes[0])} Video Dupes ane {len(random_files)} Random Files.')
    print('-' * 20)
    print("Press 'd' to delete these duplicates.")
    print("Press 's' to stop.")

    while True:
        if keyboard.is_pressed("d"):
            print("You pressed 'd' => Deleting Dupes")
            for hash_val, paths in image_hash_map.items():
                for p in paths:
                    os.remove(p)
            print("Image dupes deleted!")
            checked = set()
            deleted = set()

            for name1, hash1 in video_hashes.items():
                for name2, hash2 in video_hashes.items():
                    if name1 == name2 or (name2, name1) in checked:
                        continue

                    distance = abs(hash1 - hash2)
                    if distance <= 5:
                        p = os.path.join(folder_path, name2)
                        if os.path.exists(p) and name2 not in deleted:
                            print(f"Deleting duplicate: {name2} (similar to {name1}, distance {distance})")
                            os.remove(p)
                            deleted.add(name2)

                    checked.add((name1, name2))
            print("Video dupes deleted!")
            for p in random_files:
                os.remove(p)
            print("Random Files deleted!")
            return
        if keyboard.is_pressed("s"):
            print("You pressed 's' => Process Stopped")
            return

remove_duplicate_files()
# When working with lots of real-world image data, corrupted images are a common occurence.
# Therefore, we firstly check if there are some invalid image files before continue.

import imghdr
import json
import os

with open('settings.json') as f:
    data = json.load(f)

proj_dir = os.path.dirname(os.path.realpath(__file__))

num_skipped = 0
for folder_name in data['labels']:
    print(folder_name)
    folder_path = os.path.join(proj_dir, "images", folder_name)
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        is_valid, image_type = False, ''
        try:
            image_type = imghdr.what(fpath)
            fobj = open(fpath, "rb")
            b = fobj.peek(10)
            is_valid = (bytearray.fromhex("89504E470D0A1A0A") in b) and (image_type == 'png')
            is_valid = (bytearray.fromhex("FFD8FF") in b) and (image_type == 'jpeg') or is_valid
        except Exception as ex:
            print(ex)
        finally:
            fobj.close()

        if not is_valid:
            num_skipped += 1
            print(f"File {fpath} appears to be an invalid image file. image_type={image_type}")
            input()

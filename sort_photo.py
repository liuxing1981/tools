import datetime
import shutil
import sys
from collections import defaultdict

import exifread
import os

result = defaultdict(set)


def get_create_time(file):
    create_time = os.stat(file).st_mtime
    dateArray = datetime.datetime.fromtimestamp(create_time)
    create_time = dateArray.strftime("%Y%m%d%H%M%S")
    return create_time


def get_take_time(file):
    with open(file, 'rb') as f:
        tags = exifread.process_file(f)
        # info = {
        #     'Image DateTime(拍摄时间)': tags.get('Image DateTime', '0').values,
        #     'GPS GPSLatitudeRef(纬度标志)': tags.get('GPS GPSLatitudeRef', '0').values,
        #     'GPS GPSLatitude(纬度)': tags.get('GPS GPSLatitude', '0').values,
        #     'GPS GPSLongitudeRef(经度标志)': tags.get('GPS GPSLongitudeRef', '0').values,
        #     'GPS GPSLongitude(经度)': tags.get('GPS GPSLongitude', '0').values
        # }
        if not tags or not hasattr(tags.get('Image DateTime', '0'), 'values'):
            # print('could not get file take photo time:' + file )
            take_time = get_create_time(file)
        else:
            take_time = tags.get('Image DateTime', '0').values
            take_time = take_time.replace(':','').replace(' ','')
        # print(file, take_time)
        result[take_time].add(file)


def process_img_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            path = os.path.join(root, f)
            # print('process: ' + path)
            get_take_time(path)


def group_result():
    new_result = {}
    keys = result.keys()
    key_list = set()
    for key in keys:
        key_list.add(key[:8])
    for take_time, files in result.items():
        for key in key_list:
            if take_time[:8] == key:
                if key not in new_result:
                    for index, file in enumerate(files):
                        if index == 0:
                            value = list()
                            value.append((take_time, file))
                            new_result[key] = value
                        else:
                            new_result[key].append((take_time, file))
                elif key in new_result:
                    for file in files:
                        new_result[key].append((take_time, file))
    for key, value in new_result.items():
        value = sorted(value, key=lambda x:x[0])
        _, old_file_name = value[0]
        path = os.path.dirname(old_file_name)
        day = key[:4] + '-' + key[4:6] + '-' + key[6:8]
        dest_folder = os.path.join(path, day)
        os.makedirs(dest_folder, exist_ok=True)
        num = len(str(len(value)))
        for index, (take_time, old_file_name) in enumerate(value):
            ext = '.' + old_file_name.split('.')[-1]
            take_time = take_time[:8]
            take_time = take_time[:4] + '-' + take_time[4:6] + '-' + take_time[6:8]
            new_file_name = os.path.join(dest_folder, take_time + '-' + format(index+1, num) + ext)
            shutil.move(old_file_name, new_file_name)


def format(n, length):
    n_str = str(n)
    zero = length - len(n_str)
    for z in range(zero):
        n_str = '0' + n_str
    return n_str


if __name__ == '__main__':
    path = sys.argv[1]
    process_img_dir(path)
    group_result()

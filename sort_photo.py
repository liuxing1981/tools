import datetime
import re
import shutil
import sys
from collections import defaultdict
import requests
import exifread
import os

result = defaultdict(set)
cache = dict()

def get_create_time(file):
    create_time = os.stat(file).st_mtime
    dateArray = datetime.datetime.fromtimestamp(create_time)
    create_time = dateArray.strftime("%Y%m%d%H%M%S")
    return create_time


def get_pos(lat, lng):
    location = lat + ',' + lng
    if location in cache:
        return cache.get('location')
    params = {'ak': 'nhlAGVABg5SIdywdUMCWFAIRGragbZ2a',
              'output': 'json',
              'coordtype': 'wgs84ll',
              'location': location
              }
    response = requests.get("http://api.map.baidu.com/reverse_geocoding/v3/", params=params)
    output = response.json()
    addr = output['result']['formatted_address']
    cache['location'] = addr
    print(addr)
    return addr


def _format_location(loc):
    val = str(loc[0].num) + '.' + str(loc[1].num) + str(loc[2].num).split('/')[0]
    return val


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
        take_time, addr = '', ''
        if tags:
            if 'Image DateTime' in tags:
                take_time = tags.get('Image DateTime', '0').values
                take_time = take_time.replace(':', '').replace(' ', '')
            else:
                take_time = get_create_time(file)
            if 'GPS GPSLongitude' in tags and 'GPS GPSLongitude' in tags:
                lng = _format_location(tags.get('GPS GPSLongitude', '0').values)
                lat = _format_location(tags.get('GPS GPSLatitude', '0').values)
                addr = get_pos(lat, lng)
        # print(file, take_time)
        result[take_time].add((file, addr))


def process_img_dir(path):
    pattern = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}_sorted')
    for root, dirs, files in os.walk(path):
        for f in files:
            path = os.path.join(root, f)
            # print('process: ' + path)
            if not pattern.search(path):
                get_take_time(path)


def group_result():
    new_result = {}
    keys = result.keys()
    key_list = set()
    for key in keys:
        key_list.add(key[:8])
    for take_time, files_and_addr in result.items():
        for key in key_list:
            if take_time[:8] == key:
                if key not in new_result:
                    for index, (file, addr) in enumerate(files_and_addr):
                        if index == 0:
                            value = list()
                            value.append((take_time, file, addr))
                            new_result[key] = value
                        else:
                            new_result[key].append((take_time, file, addr))
                elif key in new_result:
                    for (file, addr) in files_and_addr:
                        new_result[key].append((take_time, file, addr))
    for key, values in new_result.items():
        value = sorted(values, key=lambda x:x[0])
        _, old_file_name, _ = value[0]
        path = os.path.dirname(old_file_name)
        day = key[:4] + '-' + key[4:6] + '-' + key[6:8]
        dest_folder = os.path.join(path, day + '_sorted')
        index = 0
        if os.path.exists(dest_folder):
            last_file = sorted(os.listdir(dest_folder))[-1]
            if last_file != os.path.basename(dest_folder):
                index = int(last_file.split('-')[-1].split('@')[0].lstrip('0'))
        else:
            os.makedirs(dest_folder, exist_ok=True)
        num = len(str(len(value)))
        for (take_time, old_file_name, addr) in value:
            ext = '.' + old_file_name.split('.')[-1]
            take_time = take_time[:8]
            take_time = take_time[:4] + '-' + take_time[4:6] + '-' + take_time[6:8]
            new_file_name = os.path.join(dest_folder, take_time + '-' + format(index+1, num) + '@' + addr + ext)
            shutil.move(old_file_name, new_file_name)
            index = index + 1


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

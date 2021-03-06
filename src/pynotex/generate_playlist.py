import sys
import os
import re
import argparse

from common.file import Dpl, M3u

formats = {'.mp4', '.flv', '.ts', '.wmv'}
numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

def listdir(dirname, order = lambda x: x):
    filepaths = []
    paths = list(filter(
        lambda path: os.path.splitext(path)[1] in formats or os.path.isdir(os.path.join(dirname, path)),
        os.listdir(dirname)
        ))
    sorted_paths = order(paths)
    for path in sorted_paths:
        path = os.path.join(dirname, path)
        if os.path.isfile(path):
            filepaths.append(path)
        elif os.path.isdir(path):
            filepaths.extend(listdir(path, order=order))
    return filepaths

def gen_playlist(base_dir, playlist_path, playlist_type='dpl', path_type='RP', order=lambda x: x):
    Playlist = Dpl if playlist_type == 'dpl' else M3u
    playlist = Playlist(playlist_path, path_type=path_type)
    for path in listdir(base_dir, order=order):
        playlist.write_path(path)

def order(paths):
    re_number = re.compile(r'\d+')
    re_cn_number = re.compile(r'[零一二三四五六七八九十]')
    if all([re_cn_number.search(path) for path in paths]):
        print('已使用中文数字对目录重排')
        paths = sorted(paths, key=lambda path: numbers.index(re_cn_number.search(path).group(0)))
    elif all([re_number.search(path) for path in paths]):
        print('已使用数字对目录重排')
        paths = sorted(paths, key=lambda path: int(re_number.search(path).group(0)))
    else:
        print('未对目录重排')
    return paths

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wenku')
    parser.add_argument('dir', help='待生成的 dir')
    parser.add_argument('--playlist-type', default='dpl', choices=['dpl', 'm3u'], help='生成播放列表类型')
    parser.add_argument('--path-type', default='rp', choices=['rp', 'ap'], help='播放列表绝对路径/相对路径')
    parser.add_argument('--inner', action='store_true', help='是否存储在内部')
    args = parser.parse_args()
    base_dir = args.dir
    playlist_name = 'Playlist.'+args.playlist_type
    playlist_path = os.path.join(base_dir, playlist_name) if args.inner else \
                    os.path.join(os.path.dirname(base_dir), playlist_name)
    gen_playlist(base_dir, playlist_path, playlist_type=args.playlist_type,
                path_type=args.path_type.upper(), order=order)

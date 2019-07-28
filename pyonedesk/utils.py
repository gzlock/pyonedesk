import hashlib
import os
from typing import Union

import requests


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def read_bytes_in_chunks(content: bytes, chunk_size=1024):
    last = 0
    while True:
        chunk = content[last:last + chunk_size]
        if not chunk:
            break
        last += len(chunk)
        yield chunk


def get_tree_size(path: str) -> int:
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total


def md5(text: str) -> bytes:
    """快速md5，返回16位bytes"""
    return hashlib.md5(text.encode('utf-8')).hexdigest().encode('utf-8')


def upload(url, content: Union[str, bytes], chunk_size: int = 10 * 1024 * 1024) -> dict:
    """OneDrive 文件上传"""
    if isinstance(content, str):
        total_size = os.path.getsize(content)
        chunks = read_in_chunks(open(content), chunk_size)
    # elif isinstance(content, bytes):
    else:
        total_size = len(content)
        chunks = read_bytes_in_chunks(content, chunk_size)
    session = requests.session()
    session.headers.update({'Content-Type': 'application/octet-stream'})

    start_size = 0
    for chunk in chunks:
        chunk_size = len(chunk)
        headers = {
            'Content-Length': str(chunk_size),
            'Content-Range': 'bytes {start_size}-{end_size}/{total_size}'.format(
                start_size=start_size, end_size=start_size + chunk_size - 1, total_size=total_size)
        }
        res = session.put(url, headers=headers, data=chunk)
        start_size += chunk_size
        print('上传 state code', res.status_code)
        if res.status_code == 202:
            # 202 需要继续上传
            continue
        if res.status_code in [200, 201]:
            # 200 201 上传完成
            return res.json()
        raise Exception(res.json()['error']['message'])

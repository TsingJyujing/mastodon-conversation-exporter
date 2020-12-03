"""
Download statistic files
"""

import os
import shutil

import requests

if __name__ == '__main__':
    target_path = "static"
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)
    os.makedirs(target_path, exist_ok=True)
    for fn, url in {
        "jquery.min.js": "https://code.jquery.com/jquery-3.5.1.min.js",
        "bootstrap.min.css": "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css",
        "bootstrap.min.js": "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/js/bootstrap.min.js",
        "echarts.min.js": "https://cdnjs.cloudflare.com/ajax/libs/echarts/5.0.0/echarts.min.js",
        "github-markdown.min.css": "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css",
    }.items():
        print(f"Downloading {url} -> {fn}")
        resp = requests.get(url)
        resp.raise_for_status()
        with open(os.path.join(target_path, fn), "wb") as fp:
            fp.write(resp.content)

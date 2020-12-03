# Mastodon Conversation Exporter

## Introduction

Some discussion (actually quarrel) on Mastodon is too long to read, this project is for exporting and doing some simple visualization the conversation on Mastodon.

## How to Start Server

Of course you can use https://mce.tsingjyujing.com/ directly, but it requires you input some secret information like robot access token/secret something.
So it's impossible to ensure the author(actually, me) won't abuse your personal information, right?


According to the above reasons, the most recommended way is start your server by yourselves. I know it's a little bit panic for the guys can't programming, at very least I prepared the docker image, it'll be easier for you guys to use.

### For Developers

#### Environment Setup
We're using `poetry` to manage dependencies, but also exported `requirements.txt`.
You can setup environment by `poetry install` or `pip install -r requirements.txt`.

#### Download Frontend Files

Run [pages/download.py](pages/download.py) to download all files for frontend:

```
pages/static
├── bootstrap.min.css
├── bootstrap.min.js
├── echarts.min.js
├── github-markdown.min.css
└── jquery.min.js
```

#### Start Server

Run [server.py](server.py) to start server at port 8000.

#### Docker Image Build & Start
```shell
docker build -t tsingjyujing/mastodon-conversation-exporter .
docker run -it -p 8000:8000 tsingjyujing/mastodon-conversation-exporter
```

### For Docker Users

For docker users, please pull docker image directly and run:

```shell
docker run -it -p 8000:8000 tsingjyujing/mastodon-conversation-exporter
```

Then visit http://127.0.0.1:8000/


## TODO

- I'm not good at front-end developing, so if you have any improvement on interface is welcome.
    - This program also could be done by some front-end plugin only, but I'm not good at front-end...
- Please feel free to create a PR if you have any other idea about visualization something...

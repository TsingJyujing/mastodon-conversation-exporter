# Mastodon Conversation Exporter

## Introduction

Some discussion (actually quarrel) on Mastodon is too long to read, this project is for exporting and doing some simple visualization the conversation on Mastodon.

## How to use

Of course you can use https://mce.tsingjyujing.com/ directly, but it requires you input some secret information like robot access token/secret something.
So it's impossible to ensure the author(actually, me) won't abuse your personal information, right?


According to the above reasons, the most recommended way is start your server by yourselves. I know it's a little bit panic for the guys can't programming, at very least I prepared the docker image, it'll be easier for you guys to use.

### For Developers

We're using `poetry` to manage dependencies, but also exported `requirements.txt`.
You can setup environment by `poetry install` or `pip install -r requirements.txt`.


### For Users

For common users, please 
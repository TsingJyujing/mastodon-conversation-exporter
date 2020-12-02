import datetime
import logging
import re
from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from fastapi import FastAPI
from mastodon import Mastodon
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from mce.utils import NameAlias

logging.basicConfig(level=logging.INFO)

app = FastAPI()


class ExportRequest(BaseModel):
    access_token: str
    status_url: str
    use_alias: bool = True
    include_url: bool = False
    include_image: bool = False
    indent_replies: bool = True


class MastodonClient:
    def __init__(self, export_request: ExportRequest):
        self.export_request = export_request
        url_parsed = urlparse(export_request.status_url)
        self.mastodon = Mastodon(
            api_base_url="{}://{}".format(
                url_parsed.scheme,
                url_parsed.hostname
            ),
            access_token=export_request.access_token
        )
        self.status_id = re.findall("web/statuses/(\d+)", url_parsed.path)[0]

    @property
    def status(self):
        return self.mastodon.status(self.status_id)

    @property
    def replies(self):
        return self.mastodon.status_context(self.status_id)["descendants"]


class MastodonUser:
    def __init__(self, username: str, nickname: str, user_page_url: str):
        self.nickname = nickname
        self.user_page_url = user_page_url
        self.user_id = username

    @staticmethod
    def create(obj) -> "MastodonUser":
        return MastodonUser(
            obj["username"],
            obj["display_name"],
            obj["url"]
        )


class MastodonToot:
    def __init__(
            self,
            toot_id: str,
            content: str,
            user: MastodonUser,
            tick: datetime.datetime,
            images_urls: List[str] = None,
    ):
        self.content = content
        if images_urls is not None:
            self.images_urls = images_urls
        else:
            self.images_urls = []
        self.tick = tick
        self.replies = []
        self.user = user
        self.toot_id = toot_id

    def append_reply(self, toot: "MastodonToot"):
        self.replies.append(toot)
        self.replies.sort(key=lambda t: t.tick.timestamp())

    def tree_json(self, name_alias: NameAlias = None):
        if name_alias is not None:
            mentioned_ids = set(re.findall("@([a-zA-Z]+)\s", self.content))
            content = self.content
            for uid in mentioned_ids:
                content = content.replace(f"@{uid}", f"@{name_alias.alias_name(uid)}")
        else:
            content = self.content

        node = {
            "name": name_alias.alias_name(self.user.user_id) if name_alias is not None else self.user.nickname,
            "value": content,
        }
        if len(self.replies):
            node["children"] = [
                r.tree_json(name_alias)
                for r in self.replies
            ]
        return node

    @staticmethod
    def create(obj) -> "MastodonToot":
        return MastodonToot(
            obj["id"],
            content=BeautifulSoup(obj["content"]).get_text(),
            user=MastodonUser.create(obj["account"]),
            tick=obj["created_at"],
            images_urls=[
                m["url"]
                for m in obj["media_attachments"]
                if m["type"] == "image"
            ]
        )


def sort_out_timeline(status_content, replies):
    toot_pool = dict()
    root_toot = MastodonToot.create(status_content)
    toot_pool[root_toot.toot_id] = root_toot
    replies_toot = [
        (r["in_reply_to_id"], MastodonToot.create(r))
        for r in replies
    ]
    replies_toot.sort(key=lambda t: t[1].tick.timestamp())
    for reply_to_id, toot in replies_toot:
        toot_pool[reply_to_id].append_reply(toot)
        toot_pool[toot.toot_id] = toot
    return root_toot


@app.get("/")
async def homepage():
    """
    To document
    """
    return RedirectResponse("docs")


@app.post("/tree/json")
async def generate_graph_json(export_config: ExportRequest):
    """
    Generate JSON for
    :param export_config:
    :return:
    """
    mc = MastodonClient(export_config)
    root_toot = sort_out_timeline(mc.status, mc.replies)
    tree_data = root_toot.tree_json(NameAlias() if export_config.use_alias else None)
    return tree_data

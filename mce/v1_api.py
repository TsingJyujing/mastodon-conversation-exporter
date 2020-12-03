import datetime
import logging
import re
from functools import lru_cache
from typing import List, Optional
from urllib.parse import urlparse

import markdown
from bs4 import BeautifulSoup
from fastapi import FastAPI
from mastodon import Mastodon
from pydantic import BaseModel
from starlette.responses import RedirectResponse, Response, PlainTextResponse

from mce.utils import NameAlias, dump_json

logging.basicConfig(level=logging.INFO)

app = FastAPI()


class ExportRequest(BaseModel):
    access_token: str
    status_url: str
    use_alias: bool = True
    include_url: bool = False
    include_image: bool = False
    indent_replies: bool = True
    alias_language: str = "en"


class MastodonClient:
    def __init__(self, status_url: str, access_token: str):
        url_parsed = urlparse(status_url)
        self.mastodon = Mastodon(
            api_base_url="{}://{}".format(
                url_parsed.scheme,
                url_parsed.hostname
            ),
            access_token=access_token
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
        self.replies: List[MastodonToot] = []
        self.user = user
        self.toot_id = toot_id

    def append_reply(self, toot: "MastodonToot"):
        self.replies.append(toot)
        self.replies.sort(key=lambda t: t.tick.timestamp())

    def tree_json(self, name_alias: Optional[NameAlias] = None):
        """
        Generate tree data JSON for echarts
        :param name_alias:
        :return:
        """
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
        if len(self.replies) > 0:
            node["children"] = [
                r.tree_json(name_alias)
                for r in self.replies
            ]
        return node

    def markdown(
            self,
            indent: bool,
            include_url: bool,
            include_image: bool,
            name_alias: Optional[NameAlias] = None,
            indent_level: int = 0
    ):
        """
        Generate Markdown text
        :param indent:
        :param include_url:
        :param include_image:
        :param name_alias:
        :param indent_level:
        :return:
        """
        if include_url and name_alias is not None:
            raise Exception("Name aliasing is meaningless while included URL")
        if name_alias is not None:
            display_name = name_alias.alias_name(self.user.user_id)
            mentioned_ids = set(re.findall("@([a-zA-Z]+)\s", self.content))
            content = self.content
            for uid in mentioned_ids:
                content = content.replace(f"@{uid}", f"@{name_alias.alias_name(uid)}")
        else:
            display_name = self.user.nickname
            content = self.content

        if include_image:
            for images_url in self.images_urls:
                content += f" <br> ![]({images_url}) "

        if include_url:
            display_name = "[{}]({})".format(display_name, self.user.user_page_url)

        markdown_text = "{} {} : {} <br><br> \n".format(
            ">" * indent_level if indent else "",
            display_name,
            content
        )

        if len(self.replies) > 0:
            for child in self.replies:
                markdown_text += child.markdown(
                    indent,
                    include_url,
                    include_image,
                    name_alias,
                    indent_level + 1
                )
        return markdown_text

    @staticmethod
    def create(obj) -> "MastodonToot":
        return MastodonToot(
            obj["id"],
            content=BeautifulSoup(obj["content"], "html.parser").get_text(),
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


@lru_cache(maxsize=128)
def load_toot_from_config(status_url: str, access_token: str) -> MastodonToot:
    mc = MastodonClient(status_url, access_token)
    return sort_out_timeline(
        mc.status,
        mc.replies
    )


@lru_cache(maxsize=128)
def named_alias_cache(status_url: str, access_token: str, language: str) -> NameAlias:
    return NameAlias.create(language)


@app.get("/")
async def homepage():
    """
    To document
    """
    return RedirectResponse("docs")


@app.post("/export/markdown")
async def generate_raw_json(export_config: ExportRequest):
    return PlainTextResponse(
        content=load_toot_from_config(
            export_config.status_url,
            export_config.access_token
        ).markdown(
            export_config.indent_replies,
            export_config.include_url,
            export_config.include_image,
            named_alias_cache(
                export_config.status_url,
                export_config.access_token,
                export_config.alias_language
            ) if export_config.use_alias else None,
        ),
        media_type="text/markdown"
    )


@app.post("/export/html")
async def generate_raw_json(export_config: ExportRequest):
    return PlainTextResponse(
        content=markdown.markdown(
            load_toot_from_config(
                export_config.status_url,
                export_config.access_token
            ).markdown(
                export_config.indent_replies,
                export_config.include_url,
                export_config.include_image,
                named_alias_cache(
                    export_config.status_url,
                    export_config.access_token,
                    export_config.alias_language
                ) if export_config.use_alias else None,
            )
        ),
        media_type="text/html"
    )


@app.post("/export/json")
async def generate_raw_json(export_config: ExportRequest):
    mc = MastodonClient(
        export_config.status_url,
        export_config.access_token
    )
    return Response(
        content=dump_json({
            "status": mc.status,
            "replies": mc.replies
        }).encode(),
        media_type="application/json"
    )


@app.post("/tree/json")
async def generate_tree_json(export_config: ExportRequest):
    """
    Generate JSON for
    :param export_config:
    :return:
    """
    return load_toot_from_config(
        export_config.status_url,
        export_config.access_token
    ).tree_json(
        named_alias_cache(
            export_config.status_url,
            export_config.access_token,
            export_config.alias_language
        ) if export_config.use_alias else None
    )

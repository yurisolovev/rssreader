import feedparser
import time
from flask import current_app
from datetime import datetime
from math import ceil


class Pagination:
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def prev_num(self):
        if self.has_prev:
            return self.page - 1
        else:
            return None

    @property
    def next_num(self):
        if self.has_next:
            return self.page + 1
        else:
            return None

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if not (not (num <= left_edge) and not (num > self.page - left_current - 1
                                            and num < self.page + right_current)
                                            and not (num > self.pages - right_edge)):
                if last + 1 != num:
                    yield None
                yield num
                last = num


def feed_reader(feed, page):
    app = current_app._get_current_object()
    per_page = app.config['RSSREADER_PER_PAGE']
    d = feedparser.parse(feed)

    news_list = [(d["entries"][i], datetime.utcfromtimestamp(time.mktime(d["entries"][i].published_parsed)))
                 for i in range(len(d["entries"]))]

    pagination = Pagination(page=page, per_page=per_page, total_count=len(d["entries"]))

    return news_list[(per_page * (page - 1)):(per_page * page)], pagination


def feeds_reader(feeds, page):
    app = current_app._get_current_object()
    per_page = app.config['RSSREADER_PER_PAGE']

    news_list = []
    for feed in feeds:
        d = feedparser.parse(feed)
        news_list.extend([(d["entries"][i], datetime.utcfromtimestamp(time.mktime(d["entries"][i].published_parsed)))
                 for i in range(len(d["entries"]))])

    news_list.sort(key=lambda item: item[1], reverse=True)

    pagination = Pagination(page=page, per_page=per_page, total_count=len(news_list))
    return news_list[(per_page * (page - 1)):(per_page * page)], pagination

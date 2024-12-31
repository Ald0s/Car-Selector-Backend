from fastapi import Query
from fastapi_pagination import Page

from app import config


def make_page_response() -> Page:
    return Page.with_custom_options(
        size = Query(config.DEFAULT_NUM_PER_PAGE,
            ge = 1,
            le = config.MAX_NUM_PER_PAGE
        )
    )
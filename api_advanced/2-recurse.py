#!/usr/bin/python3
"""Recursively query the Reddit API for all hot article titles."""
import requests

HEADERS = {"User-Agent": "MyCustomBot/1.0"}


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of all hot post titles for a subreddit recursively.

    If the subreddit is invalid or has no results, returns None.
    """
    if hot_list is None:
        hot_list = []

    if not subreddit or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            allow_redirects=False,
            timeout=10
        )
        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        children = data.get("children", [])
        for post in children:
            hot_list.append(post.get("data", {}).get("title"))

        next_after = data.get("after")
        if next_after is not None:
            return recurse(subreddit, hot_list, next_after)

        return hot_list if hot_list else None
    except Exception:
        return None

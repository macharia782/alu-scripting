#!/usr/bin/python3
"""Query the Reddit API and print titles of the first 10 hot posts."""
import requests

HEADERS = {"User-Agent": "MyCustomBot/1.0"}


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts for a given subreddit.

    If the subreddit is invalid, prints None.
    """
    if not subreddit or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {"limit": 10}
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            allow_redirects=False,
            timeout=10
        )
        if response.status_code != 200:
            print(None)
            return

        children = response.json().get("data", {}).get("children", [])
        if not children:
            print(None)
            return

        for post in children[:10]:
            print(post.get("data", {}).get("title"))
    except Exception:
        print(None)

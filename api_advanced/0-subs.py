#!/usr/bin/python3
"""Query the Reddit API for the number of subscribers of a subreddit."""
import requests

HEADERS = {"User-Agent": "linux:alu.api.advanced:v1.0.0 (by /u/j_alu)"}


def number_of_subscribers(subreddit):
    """Return the total number of subscribers for a given subreddit.

    If the subreddit is invalid, returns 0.
    """
    if not subreddit or not isinstance(subreddit, str):
        return 0

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    try:
        response = requests.get(
            url, headers=HEADERS, allow_redirects=False, timeout=10
        )
        if response.status_code != 200:
            return 0
        data = response.json().get("data", {})
        return data.get("subscribers", 0)
    except Exception:
        return 0

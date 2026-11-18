#!/usr/bin/python3
"""Recursively query Reddit API and count keyword occurrences in titles."""
import requests

HEADERS = {"User-Agent": "MyCustomBot/1.0"}


def count_words(subreddit, word_list, after=None, counts=None, weights=None):
    """Print sorted counts of given keywords in all hot post titles."""
    if counts is None:
        counts = {}
        weights = {}
        for word in word_list:
            key = word.lower()
            weights[key] = weights.get(key, 0) + 1
            counts[key] = 0

    if not subreddit or not isinstance(subreddit, str) or not counts:
        return

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
            return

        data = response.json().get("data", {})
        children = data.get("children", [])

        for post in children:
            title = post.get("data", {}).get("title", "")
            for token in title.lower().split():
                if token in counts:
                    counts[token] += weights[token]

        next_after = data.get("after")
        if next_after is not None:
            return count_words(
                subreddit, word_list, next_after, counts, weights
            )

        sorted_items = sorted(
            [(k, v) for k, v in counts.items() if v > 0],
            key=lambda item: (-item[1], item[0])
        )
        for word, total in sorted_items:
            print("{}: {}".format(word, total))
    except Exception:
        return

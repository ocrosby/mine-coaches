import requests


def follow_redirections(url: str, max_redirects: int = 5) -> str:
    """
    Follows the redirections of a URL and returns the final URL
    """
    for _ in range(max_redirects):
        response = requests.get(url, allow_redirects=False)
        if 300 <= response.status_code < 400:
            location = response.headers.get('Location')
            if location:
                url = location
            else:
                break
        else:
            break
    return url
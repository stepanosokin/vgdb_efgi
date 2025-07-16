import requests
from vgdb_general import smart_http_request
import json


def download_efgi_reports(
    s: requests.Session,
    page_size=100000,
    page_from=0,
    page_to=13,
    cookie="сюда вставить свежий cookie из сессии браузера efgi.ru после логина, запрос search",
):
    """This function downloads the efgi geologic reports metadata database from https://efgi.ru/#/registry/search
    to reports_efgi.json file using the most silly method: log in on the website manually, 
    copy the cookie from the http request, and then use it as an input for the function. 
    Using default values the function will download up to 1 400 000 reports metadata.

    Args:
        s (requests.Session): any active requests session
        page_size (int, optional): amount of reports per page. Defaults to 100000.
        page_from (int, optional): starting page (offset) for scraping. Defaults to 0.
        page_to (int, optional): ending page (offset) for scraping. Defaults to 13.
        cookie (str, optional): You must give a fresh cookie from https://efgi.ru/#/registry/search website
        after logging in with gosuslugi. Open the site from Chrome, open devtools. perform any search. 
        Then find the 'search' request in the Network tab, and then look for the 'cookie' header.
        You need its value as an input.This cookie is temporary, so you'll need a new one after some time.
    """    
    # empty list for the result
    database = []
    # post request body in json with filtering parameters
    jdata = {
        # the offset will be updated during the loop
        "offset": 0,
        # number of pages to loop must be tied with the page size considering the total database size
        "limit": page_size,
        "filters": [
            {
                "@type": "and",
                "match": [
                    {
                        "@type": "or",
                        "match": [
                            {
                                "@type": "eq",
                                "key": "accountingObjectTypeCode",
                                "match": "1",
                            }
                        ],
                    }
                ],
            }
        ],
        "sort": [{"key": "informationDate", "direction": "DESC"}],
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        # this one the most important - it uses the authentication grabbed from devtools
        "cookie": cookie,
        "dnt": "1",
        "origin": "https://efgi.ru",
        "referer": "https://efgi.ru",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    }
    for page in range(page_from, page_to + 1):
        jdata["offset"] = page
        url = "https://efgi.ru/api/registry/search"
        status, result = smart_http_request(
            s, url=url, method="post", headers=headers, json=jdata
        )
        jresult = result.json()
        database.extend(jresult["data"])
    with open("reports_efgi.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    pass


if __name__ == "__main__":
    with requests.Session() as s:
        download_efgi_reports(
            s,
            page_size=100,
            page_to=1,
            cookie="DokuWiki=92lml7o0ee7c8fomm1mjmkepe9; EFGI_SESSION=VszeHN5GDHWADZMVUDGfiw|1752656842|GT8JUNEXlMO8p7rBkbM7A22xpQs",
        )
        # download_efgi_reports(
        #     s,
        #     cookie="DokuWiki=92lml7o0ee7c8fomm1mjmkepe9; EFGI_SESSION=VszeHN5GDHWADZMVUDGfiw|1752656842|GT8JUNEXlMO8p7rBkbM7A22xpQs",
        # )

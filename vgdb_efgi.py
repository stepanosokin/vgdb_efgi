import requests
from vgdb_general import smart_http_request
import json


def download_efgi_reports(s: requests.Session, page_from=0, page_to=1):
    database = []
    jdata = {
        "offset": 0,
        "limit": 100000,
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
        "cookie": "DokuWiki=77abhs3g4sggb3e4gucfpj76lm; EFGI_SESSION=5lYshEpLY3CWv-pUQAxNgA|1752594708|qq-7ClBnyHpLEgFyyfDRsmJqDLY",
        "dnt": "1",
        "origin": "https://efgi.ru",
        "referer": "https://efgi.ru",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    }
    for page in range(14):
        jdata['offset'] = page
        url = "https://efgi.ru/api/registry/search"
        status, result = smart_http_request(
            s, url=url, method="post", headers=headers, json=jdata
        )
        jresult = result.json()
        database.extend(jresult['data'])
    with open('reports_efgi.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    pass


if __name__ == "__main__":
    with requests.Session() as s:
        download_efgi_reports(s)

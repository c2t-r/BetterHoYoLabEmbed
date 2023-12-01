import requests
import json

def get(api_url, header):
    resp = requests.get(api_url, headers=header)
    return resp

def parse_hoyolink(url):
    header = {
        "host": "sg-public-api.hoyoverse.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "dnt": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip",
        "accept-language": "en,ja;q=0.9,ja-JP;q=0.8",
        "Connection": "close"
    }

    code = url.split("/")[-1]
    redirecting = f'https://sg-public-api.hoyoverse.com/common/short_link_user/v1/transit?code={code}&'
    response = get(redirecting, header)

    return response.url

def getPostData(url):
    header = {
        "host": "sg-public-api.hoyoverse.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "dnt": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip",
        "accept-language": "en,ja;q=0.9,ja-JP;q=0.8",
        "Connection": "close"
    }
    id = url.split("/")[-1].split("?")[0]
    if "contribution" in url:
        return f'https://bbs-api-os.hoyolab.com/community/community_contribution/wapi/contribution/info?id={id}'
    elif "article_pre" in url:
        response = get(f'https://bbs-api-os.hoyolab.com/community/post/wapi/getPostID?id={id}', header)
        postid = response.json()["data"]["post_id"]
        return f'https://bbs-api-os.hoyolab.com/community/post/wapi/getPostFull?post_id={postid}'
    elif "article" in url:
        return f'https://bbs-api-os.hoyolab.com/community/post/wapi/getPostFull?post_id={id}'
    else:
        return None

def parseResp(api_url, main_url, lang):

    if api_url == None:
        return main_url, False
    
    header = {
        "host": "bbs-api-os.hoyolab.com",
        "dnt": "1",
        "x-rpc-weekday": "6",
        "x-rpc-timezone": "Etc/GMT-9",
        "x-rpc-client_type": "4",
        "x-rpc-page_name": "",
        "x-rpc-language": lang,
        "x-rpc-hour": "23",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "accept": "application/json, text/plain, */*",
        "x-rpc-show-translated": "false",
        "origin": "https://www.hoyolab.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.hoyolab.com/",
        "accept-encoding": "gzip",
        "accept-language": "en,ja;q=0.9,ja-JP;q=0.8",
    }
    
    response = get(api_url, header)
    respjson = response.json()

    if "info?" in api_url:
        embed = {
            "color": 0x38f4af,
            "title": respjson["data"]["name"],
            "url": main_url,
            "image": {
                "url": respjson["data"]["banner_url"]
            }
        }
    elif "getPostFull?" in api_url:
        embed = {
            "color": 0x38f4af,
            "author": {
               "name": respjson["data"]["post"]["user"]["nickname"],
                "icon_url": respjson["data"]["post"]["user"]["avatar_url"]
            },
            "title": respjson["data"]["post"]["post"]["subject"],
            "url": main_url,
            "image": {
                "url": respjson["data"]["post"]["image_list"][0]["url"]
            }
        }

    formatted = json.dumps(respjson, indent=4, ensure_ascii=False)
    with open("response.json", "w", encoding="utf-8") as f:
        f.write(formatted)

    return embed, True

async def parseShortLink(url, lang):
    redirected_url = parse_hoyolink(url).split("?")[0]
    api_url = getPostData(redirected_url)
    data = parseResp(api_url, redirected_url, lang)
    print(f'{url} -> {redirected_url}')
    return data

async def parseLink(url, lang):
    redirected_url = url.split("?")[0]
    api_url = getPostData(redirected_url)
    data = parseResp(api_url, redirected_url, lang)
    print(f'{url}')
    return data

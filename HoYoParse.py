import requests
import datetime

def get(api_url, header):
    resp = requests.get(api_url, headers=header)
    return resp

def parse_hoyolink(url) -> str:
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    code = url.split("/")[-1]
    redirecting = f'https://sg-public-api.hoyoverse.com/common/short_link_user/v1/transit?code={code}&'
    response = get(redirecting, header)

    return response.url

def getPostData(url) -> str|None:
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
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

def parseResp(api_url, main_url, lang) -> tuple[dict|None, bool]:

    if api_url == None:
        return main_url, False
    
    today = datetime.datetime.now()
    header = {
        "x-rpc-timezone": "Etc/GMT-9",
        "x-rpc-client_type": "4",
        "x-rpc-page_name": "",
        "x-rpc-language": lang,
        "x-rpc-weekday": str(today.day),
        "x-rpc-hour": str(today.hour),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
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
        return embed, True
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
        return embed, True
    else:
        return main_url, False

async def parseShortLink(url, lang):
    redirected_url = parse_hoyolink(url).split("?")[0]
    api_url = getPostData(redirected_url)
    if api_url is None:
        print(f'{url} -> {redirected_url}')
        return redirected_url, False
    data = parseResp(api_url, redirected_url, lang)
    if data: print(f'{url} -> {redirected_url}')
    return data

async def parseLink(url, lang):
    redirected_url = url.split("?")[0]
    api_url = getPostData(redirected_url)
    if api_url is None: return None, False
    data = parseResp(api_url, redirected_url, lang)
    if data: print(f'{url}')
    return data

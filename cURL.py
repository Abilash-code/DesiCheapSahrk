import requests

cookies = {
    '_epicSID': 'd9cc60bf13854b42843c3e4ef8532909',
    'egs_age_gate_dob': '2006-11-25',
    'HasAcceptedAgeGates': 'Generic%3A18',
    'cf_clearance': 'VKf3y8JvgbH0VZjoimwOYWBzPht07sWqKciEJHzZ7PM-1772555140-1.2.1.1-Sz0bpA89J2Y5sjIAD9mlckIY2fv70eIjbNY9iGzgipkATKrYRZK3zaDMPQRwTzjGCBvc4s1rkMb6BQdbIwYK5QYOc4vVQ2qQKpY6esIVCnvQsrbf1x2ziC5rDXpKgM8vxR9GEsVwDbZRnWrq6C0a6cvM52oRpKDYYVLJDBsgP0KDVk_ubi3k5xcSEJhioNQa1YYSQsAUo2HK_iyuwwraW9wyXo5x_iioffWUKqI.GGw',
    '__cf_bm': 'ehOkMQ7jg_TrUBNLRXDQ.SEmw6hw0y6mP85BaptjZMA-1772555206-1.0.1.1-7fOPAlX4Y5LjeAtF9VSdT_ywpM9V5wy0ZiOow5jUGhM1BDKss4muDzTvpIf6vNvmfHtDvMrL.jLw6eiI9Dy2Craxmn4A8AdUw6WL8tiFb78',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.6',
    'if-none-match': 'W/"1273-Jj0/5HQq2c91hoiarlO9VJxiwFI"',
    'priority': 'u=1, i',
    'referer': 'https://store.epicgames.com/en-US/p/control',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Brave";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"iOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_epicSID=d9cc60bf13854b42843c3e4ef8532909; egs_age_gate_dob=2006-10-25; HasAcceptedAgeGates=Generic%3A18; cf_clearance=VKf3y8JvgbH0VZjoimwOYWBzPht07sWqKciEJHzZ7PM-1772555140-1.2.1.1-Sz0bpA89J2Y5sjIAD9mlckIY2fv70eIjbNY9iGzgipkATKrYRZK3zaDMPQRwTzjGCBvc4s1rkMb6BQdbIwYK5QYOc4vVQ2qQKpY6esIVCnvQsrbf1x2ziC5rDXpKgM8vxR9GEsVwDbZRnWrq6C0a6cvM52oRpKDYYVLJDBsgP0KDVk_ubi3k5xcSEJhioNQa1YYSQsAUo2HK_iyuwwraW9wyXo5x_iioffWUKqI.GGw; __cf_bm=ehOkMQ7jg_TrUBNLRXDQ.SEmw6hw0y6mP85BaptjZMA-1772555206-1.0.1.1-7fOPAlX4Y5LjeAtF9VSdT_ywpM9V5wy0ZiOow5jUGhM1BDKss4muDzTvpIf6vNvmfHtDvMrL.jLw6eiI9Dy2Craxmn4A8AdUw6WL8tiFb78',
}

response = requests.get(
    'https://store.epicgames.com/graphql?operationName=getCatalogOffer&variables=%7B%22locale%22:%22en-US%22,%22country%22:%22IN%22,%22offerId%22:%228a97a7d4d0e44523b9aa064f457627da%22,%22sandboxId%22:%22calluna%22%7D&extensions=%7B%22persistedQuery%22:%7B%22version%22:1,%22sha256Hash%22:%22ec112951b1824e1e215daecae17db4069c737295d4a697ddb9832923f93a326e%22%7D%7D',
    cookies=cookies,
    headers=headers,
)

print(response.status_code)
print(response.text[:500])
import requests

def send_discord_message(content, site_name, AQI, PM25, PM10, O3, username='WeHelp-Robot', avatar_url=None):
    aqi_data = int(AQI)
    if aqi_data<=100:
        advise="正常戶外活動。"
    elif aqi_data<=150:
        advise="1.一般民眾如果有不適，如眼痛，咳嗽或喉嚨痛等，應該考慮減少戶外活動。\n\n2.學生仍可進行戶外活動，但建議減少長時間劇烈運動。"
    elif aqi_data<=200:
        advise="1.一般民眾如果有不適，如眼痛，咳嗽或喉嚨痛等，應減少體力消耗，特別是減少戶外活動。\n\n2.學生應避免長時間劇烈運動，進行其他戶外活動時應增加休息時間。"
    elif aqi_data<=300:
        advise="1.一般民眾應減少戶外活動。\n\n2.學生應立即停止戶外活動，並將課程調整於室內進行。"
    else:
        advise="1.一般民眾應避免戶外活動，室內應緊閉門窗，必要外出應配戴口罩等防護用具。\n\n2.學生應立即停止戶外活動，並將課程調整於室內進行。"

    webhook_url = 'https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS'
    message = {
        # 'content': content,
        'username': username,
        'embeds': [
            {
                'content': content,
                'title': f'{site_name}今日空氣品質',
                'description': f'{content}\n要小心髒空氣',
                'color': 0xFFFF00, 
                'fields': [
                    {'name': '空氣品質AQI ❄️', 'value': AQI, 'inline': True},
                    {'name': '細懸浮微粒 PM2.5 🌬️', 'value': PM25, 'inline': True},
                    {'name': '懸浮微粒 PM10 😷', 'value': PM10, 'inline': True},
                    {'name': '臭氧 O3 🌏', 'value': O3, 'inline': True},
                    {'name': '🙂 給一般民眾的活動建議', 'value': advise, 'inline': False}
                ],
                'thumbnail': {
                    'url': 'https://play-lh.googleusercontent.com/0tGnOVRSY0Vi1624lXy5WG0Al2vRniNLbftickjmPXiUGUQbIwzrk6zo6_ACBQn-zGg'  # 替換為你的圖片URL
                },
                'image': {
                    'url': 'https://png.pngtree.com/thumb_back/fw800/background/20240527/pngtree-autumn-forest-mountains-trees-landscape-fresh-air-image_15732801.jpg'  # 替換為你的圖片URL
                },
                'footer': {
                    'text': '關心您健康的一天❤️'
                }
            }
        ]
    }
    
    if avatar_url:
        message['avatar_url'] = avatar_url

    response = requests.post(webhook_url, json=message)

    if response.status_code == 204:
        return '訊息已成功發送到Discord頻道'
    else:
        return f'發送訊息失敗，狀態碼：{response.status_code}'

# 使用範例
# result = send_discord_message(
#     content='彭彭即時空氣品質監測資訊，關心您的鼻孔',
#     username='pong pong',
#     avatar_url='https://training.pada-x.com/imgs/head1.jpg'
# )
# print(result)
# import requests

# def send_discord_message(content, username='WeHelp-Robot', avatar_url=None):
#     webhook_url = 'https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS'
#     embed = {
#     "description": "text in embed",
#     "title": "embed title"
#     }
#     message = {
#         'content': content,
#         'username': username,
#         "embeds": [
#         embed
#         ],
#     }
#     if avatar_url:
#         message['avatar_url'] = avatar_url

#     response = requests.post(webhook_url, json=message)

#     if response.status_code == 204:
#         return '訊息已成功發送到Discord頻道'
#     else:
#         return f'發送訊息失敗，狀態碼：{response.status_code}'

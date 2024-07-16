import requests

def send_discord_message(content):
    webhook_url = 'https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS'
    message = {
        'content': content
    }

    response = requests.post(webhook_url, json=message)

    if response.status_code == 204:
        return '訊息已成功發送到Discord頻道'
    else:
        return f'發送訊息失敗，狀態碼：{response.status_code}'

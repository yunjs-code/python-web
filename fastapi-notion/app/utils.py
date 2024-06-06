import requests
import logging

def post_to_notion(notion_url, headers, data):
    response = requests.post(notion_url, headers=headers, json=data)
    logging.debug(f"Notion API response status: {response.status_code}")
    logging.debug(f"Notion API response content: {response.text}")
    return response

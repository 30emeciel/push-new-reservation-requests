import os

from slack_sdk import WebClient

slack = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
slack_channel = os.environ['SLACK_CHANNEL']


def send_slack_message(txt):
    slack.chat_postMessage(
        channel=slack_channel,
        text=txt,
        unfurl_links=False,
        unfurl_media=False,
        link_names=False,
    )

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import deepdarkweb
import time

slack_token = "xoxb-6592374999974-6688032923889-2HNnPSvMIx5zHcpr77yFt18Y"
client = WebClient(token=slack_token)

def main(channel_id):
    while True:
        darkweb_crawling = deepdarkweb.Crawling('darkwebs.json')
        darkweb = darkweb_crawling.main()

        try:
            for channel_name, send_messages in darkweb.items():
                for send_message in send_messages:
                    response = client.chat_postMessage(
                        channel=channel_id, #채널 id를 입력합니다.
                        text= f'Darkweb {channel_name} : {send_message} 기업이 유출되었습니다.'
                    )
        except SlackApiError as e:
            assert e.response["error"]

        
        deepweb_crawling = deepdarkweb.Crawling('deepwebs.json')
        deepweb = deepweb_crawling.main()

        try:
            for channel_name, send_messages in deepweb.items():
                for send_message in send_messages:
                    response = client.chat_postMessage(
                        channel=channel_id, #채널 id를 입력합니다.
                        text= f'Deepweb {channel_name} : {send_message} 게시글이 올라왔습니다'
                    )
                    
        except SlackApiError as e:
            assert e.response["error"]
        
        time.sleep(300)
        
if __name__ == '__main__':
    main('C06LJFU441W')
import sys
import configparser # for password
from flask import Flask, jsonify

# Azure Text Analytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from flask import Flask, request, abort # flask is for web back-end with python, django is for larger project
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage # text only
)

#Config Parser # for password
config = configparser.ConfigParser()
config.read('config.ini')

#Config Azure
credential = AzureKeyCredential(config['Azurelanguage']['API_KEY'])


app = Flask(__name__) # 初始

channel_access_token = config['Line']['CHANNEL_ACCESS_TOKEN'] # CHANNEL_ACCESS_TOKEN
channel_secret = config['Line']['CHANNEL_SECRET']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret) #要去與對接

configuration = Configuration(
    access_token=channel_access_token
)




@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent) # reply to user
def message_text(event):
    sentiment_info = azure_sentiment(event.message.text)  # 只调用一次
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=sentiment_info)]
            )
        )

def azure_sentiment(user_input):
    # Existing setup for sentiment analysis
    text_analytics_client = TextAnalyticsClient(
        endpoint=config['Azurelanguage']['END_POINT'], credential=credential
    )

    documents = [user_input]

    # Sentiment analysis
    sentiment_response = text_analytics_client.analyze_sentiment(
        documents, show_opinion_mining=True, language="zh-Hant"
    )

    sentiment_docs = [doc for doc in sentiment_response if not doc.is_error]

    # Key phrases extraction
    key_phrases_response = text_analytics_client.extract_key_phrases(documents, language="zh-Hant")
    key_phrases_docs = [doc for doc in key_phrases_response if not doc.is_error]

    # Combine sentiment analysis and key phrases extraction results
    sentiment_info = ""
    if sentiment_docs:
        sentiment_result = sentiment_docs[0].sentiment
        confidence_scores = sentiment_docs[0].confidence_scores

        if sentiment_result == "positive":
            sentiment_info = f"正向\n信心分數 = {confidence_scores.positive:.2f}\n"
        elif sentiment_result == "neutral":
            sentiment_info = f"中性\n信心分數 = {confidence_scores.neutral:.2f}\n"
        elif sentiment_result == "negative":
            sentiment_info = f"負向\n信心分數 = {confidence_scores.negative:.2f}\n"

    if key_phrases_docs and key_phrases_docs[0].key_phrases:
        key_phrases = key_phrases_docs[0].key_phrases
        key_phrases_info = "主詞：" + ", ".join(key_phrases)
    else:
        key_phrases_info = "主詞：無"

    sentiment_info += key_phrases_info

    return sentiment_info

    


if __name__ == "__main__":
    app.run()
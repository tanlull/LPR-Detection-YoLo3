from flask import Flask, request, jsonify
import json
import params
import requests
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,
)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

token = params.get("Line","token")
secret = params.get("Line","secret")
line_bot_api = LineBotApi(token)
handler = WebhookHandler(secret)

@app.route('/') 
def main():
    return "Python Line!"

@app.route('/test') 
def test():
    return "Python Test!"

@app.route("/lpr", methods=['GET', 'POST'])
def lpr():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    lpr_search = event.message.text
    app.logger.info("LPR = " + lpr_search)
    lpr_time,lpr,lpr_original,lpr_preview = lpr_serachDB(lpr_search)
    line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(
            original_content_url=lpr_original,
            preview_image_url=lpr_preview
        )
        )


    # line_bot_api.reply_message(event.reply_token,
    #     TextSendMessage(text=event.message.text)
    #     )

        
def lpr_serachDB(lpr):

    url = "http://totsmartcity.com:59200/lpr/_search?size=1&sort=time:desc&q=lpr:'{}'".format(lpr)
    app.logger.info("url = {}".format(url))
    response = requests.get(url)
    json_data = response.json()
    #app.logger.info("DB = {}".format(json_data))
    json_data1 = json_data["hits"]["hits"][0]["_source"]
    app.logger.info("DB = {}".format(json_data1))
    lpr_time = json_data1["time"]
    lpr = json_data1["lpr"]
    lpr_original = format_image(json_data1["origin_file"])
    lpr_preview = format_image(json_data1["crop_file"])
    return lpr_time,lpr,lpr_original,lpr_preview


def format_image(image):
    base_image_url = "https://totsmartcity.com/lpr"
    out = image.replace("./output", "")
    out = out.replace("\\", "/")
    out = base_image_url+out
    app.logger.info("data = {}".format(out))
    return out

if __name__ == '__main__':
     app.run(debug=True, port=50002, host='0.0.0.0')
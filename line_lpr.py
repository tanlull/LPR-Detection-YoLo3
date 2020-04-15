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
    found,lpr_time,lpr,lpr_original,lpr_preview = lpr_serachDB1(lpr_search)
    if(found==0):
        reply_message="Not Found"
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=reply_message)
        )
    else:
        reply_message = "LPR = {}\n--------------------------{}".format(lpr,lpr_time)
        line_bot_api.reply_message(event.reply_token,[
            TextSendMessage(text=reply_message),
            ImageSendMessage(
                original_content_url=lpr_original,
                preview_image_url=lpr_preview
            )
            ]
        )


    # line_bot_api.reply_message(event.reply_token,
    #     TextSendMessage(text=event.message.text)
    #     )


def lpr_serachDB1(lpr_search):
    found,list_dict = elastic_serachDB("lpr",lpr_search,10)
    #app.logger.info("Found = {} \n elastic_serachDB OUT = {}".format(found,list_dict))
    lpr_time_all=""
    lpr=""
    lpr_original=""
    lpr_preview=""
    old_time = ""
    if(found>0):
        i=0
        for each_dict in list_dict:
            if(i==0):
                lpr = each_dict["lpr"]    
                lpr_original = format_image(each_dict["origin_file"])
                lpr_preview = format_image(each_dict["crop_file"])     
                app.logger.info("LPR = {}".format(lpr))
            each_time=format_time(each_dict["time"])
            if(old_time!=each_time): 
                lpr_time_all = "{}\n{}, {}".format(lpr_time_all,lpr,each_time)
                old_time=each_time
                
            i = i +1
            #return found,lpr_time_all,lpr,lpr_original,lpr_preview
    app.logger.info("LPR Time = {}".format(lpr_time_all))
    app.logger.info("Found = {}".format(found))
    return found,lpr_time_all,lpr,lpr_original,lpr_preview

# Elasticearch return List of Dict Result 
def elastic_serachDB(document,searchString,size=1):
    url = 'http://totsmartcity.com:59200/{}/_search?size={}&sort=time:desc&q=lpr:"{}"'.format(document,size,searchString)
    app.logger.info("url = {}".format(url))
    response = requests.get(url)
    json_data = response.json()
    #app.logger.info("DB = {}".format(json_data))
    found = int(json_data["hits"]["total"]["value"])
    output_list = []
    if(found>0):
        json_result = json_data["hits"]["hits"]
        #app.logger.info("data = {}".format(json_result[0]))
        for each_result in json_result:
            #app.logger.info("Type = {}".format(type(each_result)))
            data_each_result = each_result["_source"]
            each_dict = {}
            for key in data_each_result:
                each_dict[key]= data_each_result[key]
            output_list.append(each_dict)
        #app.logger.info("elastic_serachDB OUT = {}".format(output_list))
    return found,output_list


#return full image url
def format_image(image):
    base_image_url = "https://totsmartcity.com/lpr"
    out = image.replace("./output", "")
    out = out.replace("\\", "/")
    out = base_image_url+out
    app.logger.info("data = {}".format(out))
    return out

def format_time(time) :  #2020-04-09T15:12:30Z ->  2020-04-09T15:12
    return time[0:-4].replace("T"," ")

if __name__ == '__main__':
     app.run(debug=True, port=50002, host='0.0.0.0')
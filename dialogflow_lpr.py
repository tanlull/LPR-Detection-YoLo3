import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/lpr', methods=['GET', 'POST'])
def lpr():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)
    print(req_dict)
    intent = req_dict["queryResult"]["intent"]["displayName"]
    print("Intent = {}".format(intent))
    if(intent.lower() == "pm"):
        speech = "pm"
    elif(intent.lower() == "covid"):
        speech = "covid"
    elif(intent.lower() == "lpr_number"):
        lpr_num=req_dict["queryResult"]["queryText"]
        speech = "{}".format(lpr_num)
    else:
         speech = "ผมไม่เข้าใจ คุณต้องการอะไร"
    print("Data={}".format(speech))
    res = makeWebhookResult(speech)

    return res


def makeWebhookResult(speech):
    ans_dict = {
                "fulfillmentMessages": [
                    {
                    "platform": "line",
                    "type": 4,
                    "payload": {
                        "line": {
                            "type": "text",
                            "text": speech
                        }
                    }
                },
                {
                    "platform": "line",
                    "type": 4,
                    "payload": {
                        "line": {
                            "type": "image",
                            "originalContentUrl": "https://1.bp.blogspot.com/-U90M8DyKu7Q/W9EtONMCf6I/AAAAAAAAW_4/7L_jB_Rg9oweu2HKhULNdu9WNefw9zf9wCLcBGAs/s1600/sao-full.jpg",
                            "previewImageUrl": "https://3.bp.blogspot.com/-POLCd-KKazc/W9EtNxsqwpI/AAAAAAAAW_0/c8P1A4Ik3tMsCXZwaI1B2n3eXZqG0ifzwCLcBGAs/s1600/sao-preview.jpg"

                        }
                    }
                }
                ]
            }
    print(ans_dict)
    return ans_dict

if __name__ == '__main__':
    app.run(debug=True, port=50003, host='0.0.0.0', threaded=True)
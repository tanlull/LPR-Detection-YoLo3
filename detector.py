# This code is written at BigVision LLC. It is based on the OpenCV project. It is subject to the license terms in the LICENSE file found in this distribution and at http://opencv.org/license.html

# Usage example:  python3 object_detection_yolo.py --video=run.mp4
#                 python3 object_detection_yolo.py --image=bird.jpg

import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
import params
import utils
import requests
import db_elastics as db
import json


# Initialize the parameters
confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4  #Non-maximum suppression threshold

inpWidth = 416  #608     #Width of network's input image
inpHeight = 416 #608     #Height of network's input image

parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
parser.add_argument('--image', help='Path to image file.')
parser.add_argument('--video', help='Path to video file.')
parser.add_argument('--rtsp', help='Path to video file.')
args = parser.parse_args()

# Load names of classes
classesFile = "classes.names";

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.

modelConfiguration = "darknet-yolov3.cfg";
modelWeights = "lapi.weights";

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    #    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    frame_origin = frame.copy()
    left_new = left - round((right-left)*0.05)
    right_new = right + round((right-left)*0.05)
    bottom_new = bottom + round((bottom-top)*0.2)
    cv.rectangle(frame, (left_new, top), (right_new, bottom_new), (0, 255, 0), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    
    #Confident
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine),    (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 2)
    saveFile(frame_origin,frame,left_new, top, right_new, bottom_new)

def saveFile(frame_origin,frame,left, top, right, bottom):
    folder_name = utils.getDateStr()
    file_name = utils.getDateTime()

    out_folder = os.path.join(folder_out,folder_name)
    utils.createFolder(out_folder) #check if not exist then creategit

    origin_file = os.path.join(out_folder, "{}.jpeg".format(file_name))
    cv.imwrite(origin_file, frame_origin)


    out_file = os.path.join(out_folder, "{}_detect.jpeg".format(file_name))
    cv.imwrite(out_file, frame)

    crop = frame_origin[top:bottom, left:right]
    crop_file = os.path.join(out_folder, "{}_crop.jpeg".format(file_name))
    cv.imwrite(crop_file, crop)

    print("Saved: "+origin_file)
    lpr_ai4thai(origin_file,out_file,crop_file);

def lpr_ai4thai(origin_file,out_file,crop_file):
    url =  params.get('AI4Thai','lpr_url')
    payload = {'crop': '1', 'rotate': '1'}
    files = {'image':open(crop_file, 'rb')}

    apikey = getAPIKey()
    
    headers = {
        'Apikey': apikey,
    }
    response = requests.post( url, files=files, data = payload, headers=headers)
    try:  
        print("AI4Thai LPR = " + response.json()[0]["lpr"])    
        data_dict = {}  
        data_dict["time"] =  utils.getCurrentTime()
        data_dict["lpr"] = response.json()[0]["lpr"]
        data_dict["origin_file"] = origin_file
        data_dict["out_file"] = out_file
        data_dict["crop_file"] = crop_file
        #print(json.dumps(data_dict)) 
        es = db.connect()
        result = db.insert(es,json.dumps(data_dict),indexName = "lpr")
        print("Elastic : Successful = {}\n-----------".format(result["_shards"]["successful"])) 
    except Exception as e: 
        print('LPR error: {}'.format(str(response.json()["message"])))   
    return response

#auto switch if reach rate limit
def getAPIKey():
    apikey = params.get('AI4Thai','Apikey')
    return apikey

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        #print("out.shape : ", out.shape)
        for detection in out:
            #if detection[4]>0.001:
            scores = detection[5:]
            classId = np.argmax(scores)
            #if scores[classId]>confThreshold:
            confidence = scores[classId]
            #if detection[4]>confThreshold:
                #print("LPR Detect with Confident: {}".format(round(confidence,2)))
                #print(detection)
            if confidence > confThreshold:
                print("LPR Detected with Confident: {}".format(round(float(confidence),2)))
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
                

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)


outputFile = "lpr_out_py.avi"
video_source=0
if (args.image):
    # Open the image file
    if not os.path.isfile(args.image):
        print("Input image file ", args.image, " doesn't exist")
        sys.exit(1)
    video_source=args.image
    outputFile = args.image[:-4]+'_yolo_out_py.jpg'
elif (args.video):
    # Open the video file
    if not os.path.isfile(args.video):
        print("Input video file ", args.video, " doesn't exist")
        sys.exit(1)
    video_source=args.video
    outputFile = args.video[:-4]+'_yolo_out_py.avi'
elif (args.rtsp):
    rtsp_stream = params.get('RTSP',args.rtsp)
    video_source=rtsp_stream
    outputFile = args.rtsp+'_yolo_out_py.avi'
else:
    # Webcam input
    video_source=0


cap = cv.VideoCapture(video_source)

# Get the video writer initialized to save the output video
#if (not args.image):
    # vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

skipFrame = int(params.get("RTSP","skip"))# input number of frame to be skipped processing  
frameNo = 0
winName = 'LPR'
cv.namedWindow(winName, cv.WINDOW_NORMAL)
folder_out = "./output"


while cv.waitKey(1) < 0:
    try:
        # get frame from the video
        hasFrame, frame = cap.read()
        if(frameNo%skipFrame == 0) : 


            # Stop the program if reached end of video
            if not hasFrame:
                #print("Done processing !!!")
                #print("Output file is stored as ", outputFile)
                #cv.waitKey(3000)
                cap = cv.VideoCapture(video_source)
                continue

            # Create a 4D blob from a frame.
            blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

            # Sets the input to the network
            net.setInput(blob)

            # Runs the forward pass to get output of the output layers
            outs = net.forward(getOutputsNames(net))
            
            # Remove the bounding boxes with low confidence
            postprocess(frame, outs)

            # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
            t, _ = net.getPerfProfile()
            label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
            #cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

            # Write the frame with the detection boxes
            # if (args.image):
            #     cv.imwrite(outputFile, frame.astype(np.uint8));
            # else:
            #     vid_writer.write(frame.astype(np.uint8))

            cv.imshow(winName, frame)
        frameNo +=1
    except Exception as e: 
        print('Video Error: '+ str(e))   
# Release handle to the webcam
cap.release()
cv.destroyAllWindows()
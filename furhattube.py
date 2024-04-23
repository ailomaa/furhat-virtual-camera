import argparse
import zmq
import cv2
import numpy
import json
import pyvirtualcam


def annotate(img, annot):

    # loop over all detected faces
    for u in annot['users']:
        # get bounding box
        x = u['bbox']['x']
        y = u['bbox']['y']
        w = u['bbox']['w']
        h = u['bbox']['h']

        # draw bounding box
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),1)

        # landmarks are given in a list of the form x1,y1,x2,y2...
        for lx,ly in zip(*[iter(u['landmarks'])]*2):
            # landmark coordinates are normalized [0-1] relative to the bounding box
            # so they have to be un-normalized for plotting
            cv2.circle(img,(int(x+lx*w),int(y+ly*h)),4,(0,255,255),1)

        font = cv2.FONT_HERSHEY_PLAIN

        # show user ID at the top
        cv2.putText(img,'id:' + str(u['id']),(x,y),font,1,(128,255,128),1)
        y+=10

        # show emotion estimates
        for emo,val in u['emotion'].items():
            cv2.putText(img,emo + ':' + str(val),(x,y+30),font,1,(255,255,0),1)
            y+=10


parser = argparse.ArgumentParser(description='Display furhat camerafeed with overlayed annotations (face bounding boxes, user id:s,emotion estimates). Make sure external camera feed is enabled on the robot')
parser.add_argument('addr', help='IP address to furhat robot, excluding port nr')
args=parser.parse_args()

url = 'tcp://{}:3000'.format(args.addr)
# Setup the sockets
context = zmq.Context()
# Input camera feed from furhat using a SUB socket
insocket = context.socket(zmq.SUB)
insocket.setsockopt_string(zmq.SUBSCRIBE, '')
insocket.connect(url)
insocket.setsockopt(zmq.RCVHWM, 1)
insocket.setsockopt(zmq.CONFLATE, 1)  # Only read the last message to avoid lagging behind the stream.

print('listening to {}, entering loop'.format(url))


img = None

with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
    while True:
            string = insocket.recv()
            magicnumber = string[0:3]
            #print(magicnumber)
            # check if we have a JPEG image (starts with ffd8ff
            if magicnumber == b'\xff\xd8\xff':
                buf = numpy.frombuffer(string, dtype=numpy.uint8)
                img = cv2.imdecode(buf, flags=1)
            else:
                annot = json.loads(string.decode())
                #print(annot)
                if isinstance(img, numpy.ndarray):
                    annotate(img, annot)

                    cam.send(img)
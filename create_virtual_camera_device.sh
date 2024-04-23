#!/bin/bash

sudo modprobe v4l2loopback \
        devices=1 exclusive_caps=1 video_nr=20 \
        card_label="v4l2 Virtual camera"\
        max_buffers=2

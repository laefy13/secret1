#!/bin/bash
docker run -it --cap-add=NET_ADMIN --device /dev/net/tun -v /d/docker/twitterVid:/app twitter-vid
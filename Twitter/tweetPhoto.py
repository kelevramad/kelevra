#! /usr/bin/python -u
# -*- coding: utf-8 -*-

SAVEDIR = "/tmp"

import pygame
import pygame.camera
import time
import sys
import os
import twitter
import ConfigParser

configuration = "twitterc"

def TweetPhoto():
	print "Pygame init"
	pygame.init()
	print "Camera init"
	pygame.camera.init()
	cam = pygame.camera.Camera("/dev/video0", (1280, 720))

	print "Camera start"
	cam.start()
	time.sleep(1)
	print "Getting image"
	image = cam.get_image()
	time.sleep(1)
	print "Camera stop"
	cam.stop()

	timestamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
	year = time.strftime("%Y", time.localtime())
	filename = "%s/%s.jpg" % (SAVEDIR, timestamp)
	print "Saving file %s" % filename
	pygame.image.save(image, filename)

	cfg = ConfigParser.ConfigParser()
	print "Reading configuration: %s" % configuration
	if not os.path.exists(configuration):
		print "Failed to find configuration file %s" % configuration
		sys.exit(1)

	cfg.read(configuration)
	cons_key = cfg.get("TWITTER", "CONS_KEY")
	cons_sec = cfg.get("TWITTER", "CONS_SEC")
	acc_key = cfg.get("TWITTER", "ACC_KEY")
	acc_sec = cfg.get("TWITTER", "ACC_SEC")

	print "Autenticating in Twitter"
	tw = twitter.Api(
		consumer_key = cons_key,
		consumer_secret = cons_sec,
		access_token_key = acc_key,
		access_token_secret = acc_sec)

	print "Posting..."

	#tw.PostUpdate("Hi timestamp=%s" %timestamp)
	tw.PostUpdate(status = "Testing python twitter and PostUpdate() for #pyconse timestamp=%s" % timestamp, media = filename)
	
	print "Removing media file %s" % filename
	os.unlink(filename)

if __name__ == '__main__':
    try:
        TweetPhoto()
    except KeyboardInterrupt:
        sys.exit(0)


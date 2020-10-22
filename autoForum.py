#!/usr/bin/python3
#Made by EternalBeats

from creds import USERNAME, PASSWORD, NIM
from binusUtil import login, getCourseData
import requests
import sys
import json

mainUrl = "https://binusmaya.binus.ac.id/"
s = requests.Session()
headers = {
	'Referer':'https://binusmaya.binus.ac.id/NewStudent/'
}

#Change this for your own message
title = '''
Auto generated message
'''
description = '''
This message is made for attendace purpose
'''

#Options
reply = False
printId = False
helpNeeded = False

def help():
	print("This script is made for students at binus to check their forums activity")
	print("Because in some cases replying to a forum is needed for attendace\n")
	print("By the way, here's the options :")
	print("-r\t: Reply automaticly with the title and description to the forum you haven't replied")
	print("-i\t: To print the output just the Thread ID without the forum link")
	print("-h\t: to show this message")
	sys.exit(1)

def checkStatus(threadID):
	hasReplied = False
	replyUrl = mainUrl + "services/ci/index.php/forum/getReply"
	data = {
		"threadid":threadID
	}
	prompt = s.post(replyUrl, json=data, headers=headers)
	replies = json.loads(prompt.json()['rows'])
	for reply in replies:
		if reply['UserID'] == NIM:
			hasReplied = True
			break
	return hasReplied, replies[0]['PostID']

def autoReply(threadID):
	status, PostID = checkStatus(threadID)
	if not status:
		if printId:
			print(f"replying to threadID : {PostID}")
		else:
			print(f"[*] replying to : https://binusmaya.binus.ac.id/NewStudent/#/forum/reader.{threadID}")

		data = {
			"title":title,
			"description":description,
			"action":"add",
			"threadid":threadID,
			"replyto":PostID,
			"file":None
		}
		replyUrl = mainUrl + "services/ci/index.php/forum/saveReply"
		prompt = s.post(replyUrl, json=data, headers=headers)
		if prompt.json()['status'] == "success":
			print("[*] reply successful")
		else:
			if printId:
				print(f"[-] Failed reply at threadID : {threadID}")
			else:
				print(f"[-] Failed reply at : https://binusmaya.binus.ac.id/NewStudent/#/forum/reader.{threadID}")
	else:
		# print("[*] You have replied this forum")
		return


def getThread(courses, sessId):
	forumUrl = mainUrl + "services/ci/index.php/forum/getThread"
	for course in courses:
		data = {
			"forumtypeid":1,
			"acadCareer":course['ACAD_CAREER'],
			"period":course['STRM'],
			"course":course['CRSE_ID'],
			"classid":course['CLASS_NBR'],
			"topic":"",
			"Institution":course['INSTITUTION'],
			"SESSIONIDNUM":""
		}
		prompt = s.post(forumUrl, json=data, headers=headers)
		threads = json.loads(prompt.json()['rows'])
		for thread in threads:
			if thread['ID'] == -1:
				continue
			
			if reply:
				autoReply(thread['ID'])
			else:
				status, _ = checkStatus(thread['ID'])
				if not status:
					if printId:
						print(f"[*] You haven't replied to this threadID : {thread['ID']}")
					else:
						print(f"[*] You haven't replied to this thread : https://binusmaya.binus.ac.id/NewStudent/#/forum/reader.{thread['ID']}")

options = sys.argv[1:]
for option in options:
	if option == "-r":
		reply = True
	elif option == "-i":
		printId = True
	else:
		helpNeeded = True

if helpNeeded:
	help()

s, sessId= login(s, USERNAME, PASSWORD)
if sessId:
	print("[*] Login Successful")
	s, courses = getCourseData(s, sessId)
	getThread(courses, sessId)
	print("[*] Done")
else:
	print("[-] Login Failed")
	sys.exit(1)
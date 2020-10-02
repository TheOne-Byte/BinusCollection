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

title = '''
Auto generated message
'''
description = '''
This message is made for attendace purpose
'''

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
		print(f"replying to threadID : {threadID}")

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
			print("reply successful")
		else:
			print(f"failed reply at threadID : {threadID}")
	else:
		print("you have replied this forum")
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
			autoReply(thread['ID'])

s, sessId= login(s, USERNAME, PASSWORD)
if sessId:
	s, courses = getCourseData(s, sessId)
	getThread(courses, sessId)
	print("Done")
else:
	print("Login Failed")
	sys.exit(1)
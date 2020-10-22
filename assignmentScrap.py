#!/usr/bin/python3
#Made by EternalBeats

from creds import USERNAME, PASSWORD
from binusUtil import login, getCourseData
import requests
import sys
from datetime import datetime
import os

mainUrl = "https://binusmaya.binus.ac.id/"
s = requests.Session()
headers = {
	'Referer': 'https://binusmaya.binus.ac.id/NewStudent/'
}

#Change this
outputFile = "/home/eternalbeats/Desktop/binus/sems5/assignment.txt"
assignmentFilePath = "/home/eternalbeats/Desktop/binus/sems5/Assignment/"

def menu():
	print("This script is made for students at binus to check their assignments")
	print("Download the assignment file and the deadline without opening binusmaya\n")

def downloadAssignment(downloadURI):
	downloadUrl = "https://binusmaya.binus.ac.id/services/ci/index.php/general/downloadDocument/"
	fileName = downloadURI.split('\\')[-1]
	if os.path.exists(assignmentFilePath+fileName):
		return

	downloadFileUrl = downloadUrl+downloadURI.replace('\\', '...').replace(' ', '%20')
	prompt = s.get(downloadFileUrl, headers=headers)

	with open(assignmentFilePath+fileName, 'wb') as f:
		f.write(prompt.content)
		f.close()
	print(f"[*] {fileName} Downloaded")

def scrapAssignment(assginmentURI,className):
	with open(outputFile, 'w') as f:
		f.write(f"Last updated at {datetime.now()}\n\n")
		f.close()
	for index, assignmentIndex in enumerate(assginmentURI):
		with open(outputFile,'a') as f:
			f.write(f"{className[index]} : {assignmentIndex}\n")
			f.write("="*25+"\n")
			f.close()
		assignmentUrl = mainUrl + '/services/ci/index.php/student/classes/assignmentType/' + assignmentIndex + '/01'
		prompt = s.get(assignmentUrl, headers=headers)
		for data in prompt.json():
			fileName = data['assignmentPathLocation'].split('\\')[-1]
			downloadAssignment(data['assignmentPathLocation'])
			with open(outputFile, 'a')as f:
				f.write(f"Title		: {data['Title']}\n")
				f.write(f"Deadline	: {data['deadlineDuration']} {data['deadlineTime']}\n")
				f.write(f"File 		: {fileName}\n\n")
				f.close()
			print(f"[*] {data['Title']} added")

menu()
s, sessId= login(s, USERNAME, PASSWORD)
if sessId:
	print("[*] Login Successful")
	s, courses = getCourseData(s, sessId)
	
	assignmentURI = []
	className = []
	for data in courses:
		assignmentURI.append(f"{data['CRSE_CODE']}/{data['CRSE_ID']}/{data['STRM']}/{data['SSR_COMPONENT']}/{data['CLASS_NBR']}")
		className.append(data['COURSE_TITLE_LONG'])

	scrapAssignment(assignmentURI, className)
	print("[*] Done")
else:
	print("[-] Login Failed")
	sys.exit(1)
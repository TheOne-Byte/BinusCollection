#!/usr/bin/python3
#Made by EternalBeats

import requests
from datetime import datetime
from creds import USERNAME, PASSWORD

s = requests.session()

#Change this
outputFile = "/home/eternalbeats/Desktop/binus/sems5/class.txt"

def menu():
	print("This script is made for students at binus to check their classes schedule")
	print("Check your class and with meeting id and password and the link\n")


def login(username, password):
	loginUrl = "https://myclass.apps.binus.ac.id/Auth/Login"
	data = {
		'Username' : username,
		'Password' : password
	}
	prompt = s.post(loginUrl, data=data)
	
	if prompt.json()['Status'] == True:
		print("[*] Login Success")
		return True
	else:
		print("[-] Login Error")
		print(prompt.json()['Message'])
		'''
		"Invalid username or password!" : "Wrong password"
		"User not found!" : "Wrong Username"
		"Username and password must be filled!" : "Username/Password doesn't get send or empty"
		'''

def scrap():
	indexUrl = "https://myclass.apps.binus.ac.id/Home/GetViconSchedule"
	prompt = s.get(indexUrl)

	with open(outputFile, 'w') as f:
		f.write(f"Last updated at {datetime.now()}\n\n")
		for data in prompt.json():
			f.write(f"{data['ClassCode']}, {data['CourseCode']}, {data['CourseTitleEn']}\n")
			f.write(f"Meeting date 		: {data['DisplayStartDate']} {data['StartTime']}\n")
			f.write(f"Delivery Mode		: {data['DeliveryMode']}\n")
			f.write(f"Meeting id		: {data['MeetingId']}\n")
			f.write(f"Meeting password 	: {data['MeetingPassword']}\n")
			f.write(f"Meeting url 		: {data['MeetingUrl']}\n\n")
		f.close()
	print(f"[*] data stored in {outputFile}")

menu()
if login(USERNAME, PASSWORD):
	print("[*] Trying to scrap your class list")
	scrap()
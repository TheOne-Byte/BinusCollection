from bs4 import BeautifulSoup as bs
def login(session, username, password, path = "login/", mainUrl = "https://binusmaya.binus.ac.id/"):
	loginUrl = mainUrl+path
	try:
		loginPrompt = session.get(loginUrl, timeout=5)
	except requests.exceptions.ReadTimeout:
		print("[-] Can't read login page")
		sys.exit(1)
	usernameVar = bs(loginPrompt.text,'lxml').find_all('input')[0]['name']
	passwordVar = bs(loginPrompt.text,'lxml').find_all('input')[1]['name']
	loginVar = bs(loginPrompt.text,'lxml').find_all('input')[2]['name']
	print("[*] Getting variable done")

	captchaUrl = bs(loginPrompt.text,'lxml').find_all('script')[4]['src']
	try:
		captchaPrompt = session.get(loginUrl + captchaUrl, timeout=5)
	except requests.exceptions.ReadTimeout:
		print("[-] Can't read captcha page")
		sys.exit(1)
	captcha1Var = bs(captchaPrompt.text, 'lxml').find_all('input')[0]['name']
	captcha1Value = bs(captchaPrompt.text, 'lxml').find_all('input')[0]['value']

	captcha2Var = bs(captchaPrompt.text, 'lxml').find_all('input')[1]['name']
	captcha2Value = bs(captchaPrompt.text, 'lxml').find_all('input')[1]['value']
	print("[*] Getting captcha done")

	data = {
		usernameVar:username,
		passwordVar:password,
		loginVar:'Login',
		captcha1Var:captcha1Value,
		captcha2Var:captcha2Value
	}
	session.post(loginUrl+'sys_login.php', data=data)
	return session, session.cookies['PHPSESSID']

def getCourseData(session, sessId):
	headers = {
		'Referer':'https://binusmaya.binus.ac.id/NewStudent/',
		'Cookie':f'PHPSESSID={sessId}'
	}
	prompt = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/student/init/getStudentCourseMenuCourses", headers=headers)
	data = prompt.json()[0][3][0][2:]
	return session, data
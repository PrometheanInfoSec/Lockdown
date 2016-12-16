import time
import smtplib
import imaplib
import sys
import traceback

from splinter import Browser

#Gmail account to listen for panic mail on
mail_user = ""
mail_pass = ""


#Panic subject
panic_subject = "panic"

#panic phrase to listen for in body of email
"""Please Change this"""
panic_phrase = "panic"

#Array of accounts credentials.
##Soon to be generated automatically from an encrypted file
#Just hang in there for that functionality.
creds = {}

##Example creds entry
# creds['google'] = ['mygmail@gmail.com','secretgmailpassword']
# You can add multiple accounts to each service type by building a list
# within a list in the same format as above
# Example is
# creds['google'] = [['mygmail@gmail.com','pass'],['secondgmail@gmail.com','pass2']]
##
creds['twitter'] = None
creds['facebook'] = None
creds['google'] = None

#New password to set all accounts to
"""Please Change this"""
#Or don't, I'm not your boss
#Needs to be complex enough for Facebook to accept it.
new_password = "Emergency!"

#Number of seconds to wait between checks for panic in email
WAIT_SECONDS = 10
#Number of attempts to make 
TRIES = 1

#Lag permit for page loads in seconds
INV=0.5

def poll_for(value, b, attempts=5):
	btn = None
	for i in range(attempts):
		btn = b.find_by_css(value).first
		if btn is not None:
			break
		time.sleep(INV)
	return btn

def poll_fill(name, value, b, attempts=5):
	for i in range(attempts):
		try:
			b.fill(name, value)
			return
		except:
			time.sleep(INV)
			continue

class mail_listener:
	user = ""
	passwd = ""
	panic = ""
	
	def __init__(self, user, passwd, panic):
		self.user = user
		self.passwd = passwd
		self.panic = panic
	
	
	def read(self):
		
		mail = imaplib.IMAP4_SSL('imap.gmail.com')
		mail.login(self.user, self.passwd)
		mail.list()
		mail.select("inbox")
		
		result, data = mail.search(None, "(SUBJECT \"%s\")" % panic_subject)
		
		ids = data[0]
		id_list = ids.split()
		try:
			latest_email_id = id_list[-1]
		except:
			return None
		result, data = mail.fetch(latest_email_id, "(RFC822)")
		raw_email = data[0][1]
		
		
		
		if self.panic in raw_email:
			return raw_email
		
		return None

class google_account:
	login = ""
	panic = ""
	user = ""

	def __init__(self,user, login, panic):
		self.user = user
		self.login = login
		self.panic = panic

	def passwd(self):
		if len(self.login) < 1 or len(self.panic) < 1 or len(self.user) < 1:
			return false
	
		b = Browser()
		b.driver.set_window_size(900,900)
		try:
		    b.visit("https://accounts.google.com/ServiceLogin?service=accountsettings")
		    b.fill('Email',self.user)
		    btn = b.find_by_id("next")
		    btn.click()
		    b.fill('Passwd',self.login)
		    btn = poll_for("#signIn", b)
		    
		    btn.click()
		    
		    b.visit("https://myaccount.google.com/security#signin")
		    btn = b.find_by_css(".vkq40d").first
		    if not btn == None:
			print "not none"
			btn.click()
			poll_fill('Email',self.user, b)
                        btn = b.find_by_id("next")
                        btn.click()
                        poll_fill('Passwd',self.login, b)
                        btn = b.find_by_id("signIn")
                        btn.click()

		    time.sleep(INV)
		    btn = poll_for(".TCRTM", b)
		    btn.click()
		    poll_fill('Passwd',self.login, b)
		    btn = b.find_by_id("signIn")
		    btn.click()
		    p = poll_for(".Hj", b)
		    p.fill(self.panic)
		    p = b.find_by_css(".Hj")[1]
		    p.fill(self.panic)
		    btn = b.find_by_css(".Ya")
		    btn.click()
		    time.sleep(INV*5)
		    b.quit()
		except:
		    traceback.print_exc(file=sys.stdout)
            	    raw_input("Something went wrong...")
		    b.quit()
		
		
		
class facebook_account:
	user = ""
	login = ""
	panic = ""
	
	def __init__(self, user, login, panic):
		self.user = user
		self.login = login
		self.panic = panic
		
	def passwd(self):
		b = Browser()
		b.driver.set_window_size(900,900)
		try:
		    b.visit("https://www.facebook.com")
		    b.fill("email",self.user)
		    b.fill("pass",self.login)
		    btn = b.find_by_value("Log In")
		    btn.click()
		    b.visit("https://www.facebook.com/settings")
		    btn = b.find_by_id("u_0_7")
		    btn.click()
		    b.fill("password_old", self.login)
		    b.fill("password_new", self.panic)
		    b.fill("password_confirm", self.panic)
		    btn = b.find_by_value("Save Changes")
		    btn.click()
		    b.quit()
		except:
            	    b.quit()

class twitter_account:
    user = ""
    login = ""
    panic = ""

    def __init__(self, user, login, panic):
        self.user = user
        self.login = login
        self.panic = panic
		
    def passwd(self):
        b = Browser()
        b.driver.set_window_size(900,900)
	try:
            b.visit("https://twitter.com")
            btn = b.find_by_css(".js-login")
            btn.click()
            b.find_by_name("session[username_or_email]").fill(self.user)
            b.find_by_name("session[password]").fill(self.login)
            btn = b.find_by_value("Log in")
            btn.click()
            b.visit("https://twitter.com/settings/password")
            b.fill("current_password", self.login)
            b.fill("user_password", self.panic)
            b.fill("user_password_confirmation", self.panic)

            btn = b.find_by_text("Save changes")
            btn.click()
            b.quit()
	except:
            b.quit()

#Not Yet Implemented
class microsoft_account:
	#Currently having some weird issues with this.
	#Microsoft is weird about access to this app
	user = ""
	login = ""
	panic = ""
	
	def __init__(self, user, login, panic):
		raise NotImplementedError("Microsoft Account, Module Not Yet Implemented")
	
		self.user = user	
		self.login = login
		self.panic = panic
	
	def passwd(self):
		if len(self.login) < 1 or len(self.panic) < 1 or len(self.user) < 1:
			return false
			
		b = Browser()
		b.visit("https://login.live.com")
		#e = b.find_by_id("idDiv_PWD_UsernameExample")
		b.fill("loginfmt",self.user)
		b.fill("passwd",self.login)
		b.driver.set_window_size(900,900)
		btn = b.find_by_value("Sign in")
		btn.mouse_over()
		btn.double_click()
		b.visit("https://account.live.com/password/change?mkt=en-US")
		b.quit()


def trigger():
	if creds['twitter'] is not None:
		if type(creds['twitter'][0]) == str:
			t = twitter_account(creds['twitter'][0],creds['twitter'][1],new_password)
			t.passwd()
		elif type(creds['twitter'][0]) == list:
			for acc in creds['twitter']:
				t = twitter_account(acc[0],acc[1],new_password)
				t.passwd()
			
	if creds['facebook'] is not None:
		if type(creds['facebook'][0]) == str:
			f = facebook_account(creds['facebook'][0],creds['facebook'][1],new_password)
			f.passwd()
		elif type(creds['facebook'][0]) == list:
			for acc in creds['facebook']:
				f = facebook_account(acc[0],acc[1],new_password)
				f.passwd()
			
	if creds['google'] is not None:
		if type(creds['google'][0]) == str:
			g = google_account(creds['google'][0],creds['google'][1],new_password)
			g.passwd()		
		elif type(creds['google'][0]) == list:
			for acc in creds['google']:
				g = google_account(acc[0],acc[1],new_password)
				g.passwd()
		
if __name__ == "__main__":
	while True:
		l = mail_listener(mail_user, mail_pass, panic_phrase)
		parse = l.read()
	
	### Right here is where I plan to implement cryptographic storage for creds
	##stay tuned.  That will all be coming shortly.  But I have to be up at six am.
	# - Ben
	
		if parse is not None:
			trigger()
			TRIES -= 1
			if TRIES < 1:
				sys.exit(0)
	
		time.sleep(WAIT_SECONDS)
	

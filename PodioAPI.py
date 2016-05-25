'''Client API Push
3/2016 - Original Creation - TEF

'''

import sys, math, re, time
sys.path.append('/scripts/incpy')
from _inc_extvalue import *
from pypodio2 import api
import traceback
import json
import urllib2
import webbrowser

#from client_settings import *


#I never can understand why Royce names his functions 'G', so....
class notNamedG:
	vars = None
	logfile = ""
	
	#log() function to write to the log file
	@staticmethod
	def log ( s ):
		print(s)
		with open(notNamedG.logfile,'a') as f:
			f.write('{}/n'.format(s))

def main():
	#set the log file, extfile and load the CSV file (filename) passed from main
	notNamedG.logfile = sys.argv[2]
	extfile = sys.argv[1]

	
	import re, StringIO, csv	
	notNamedG.log('reading ext data')
	
	#function that pulls data from our proprietary database
	notNamedG.vars = extvalue_import_dat()
	

	#This is setting the results of the query to local variables to push
	#All should be text fields
	full_name = notNamedG.vars['TAS_FROM']
	email = notNamedG.vars['EMAIL']
	phone = notNamedG.vars['PHONE']
	address = notNamedG.vars['ADDRESS_1']+ " " + notNamedG.vars['CITY'] + " " +  notNamedG.vars['STATE'] + " " + notNamedG.vars['ZIP']
	nature = notNamedG.vars['NATURE']
	interest = notNamedG.vars['INTEREST']
	how_heard = notNamedG.vars['HOW_HEARD']
	project = notNamedG.vars['PROJECT']
	occupied = notNamedG.vars['OCCUPIED']
	subject = notNamedG.vars['REASON']

	
	#Making sure no blank fields are put in, they will crash the API push
	if full_name == "":
		full_name = "N/A"
	if email == "":
		email = "N/A"
	if phone == "":
		phone = "N/A"
	if address == "":
		address = "N/A"
	if subject == "":
		subject = "N/A"
	if interest == "":
		interest = "N/A"
	if project == "Z.OTHER":
		project = "OTHER"
	
	#They hava a typo, unfortunately I have to match it.
	if project == "RETAIL":
		project = "RETIAL"
	if how_heard == "Z.OTHER":
		how_heard = "OTHER"
		
	
	#in their coding, the "Advertisement" option has a trailing space, leading to sync errors
	#I add the space here to create a match.
	if how_heard == "ADVERTISEMENT":
		how_heard = "ADVERTISEMENT "
	
	#The following information is given by client, as they set me up in their system.
	client_id = ""
	client_secret = ""
	username=""
	password=""
	app_id = 
	try:


		#Opening up the connection to Podio
		push_API = api.OAuthClient(
			client_id,
			client_secret,
			username,
			password,
		)
		

		#creating a new item with fields
		#If fields change, we can go to Podio and search the app number
		item = {
			"fields":{
				"full-name-2":full_name,
				"description":interest,
				"address":address,
				"email":email,
				"subject":subject,
				"phone":phone,
				"nature-of-inquiry":nature,
				"will-the-project-worksite-be-occupied":occupied,
				"how-did-you-hear-about-us":how_heard,
				"category":project}
		}
		

		#Pushing the item to their Podio App
		push_API.Item.create(app_id, item)
		
		notNamedG.log ("API Push Successful")
		webbrowser.open("http://portal.westparkcom.net/134/goodpage.asp",new=2)
		time.sleep(5)

	except Exception, e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		
		#notNamedG.log ( 'Error: message: ' + order_num )
		notNamedG.log ( '!!!!! Shutting down - uncaught exception:\n{0}'.format (
			'\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback)) ) )
		webbrowser.open("http://portal.westparkcom.net/134/badpage.asp",new=2)
		#notNamedG.log ("Error:")
		return 1
			
	return 7 # Because apparently 7 means it ran just fine

	
	
if __name__=='__main__':
	try:
		print "------------------------"
		print "Client name** - API Push"
		sys.exit(main())
	except Exception as e:
		notNamedG.log ( '!!!!! Shutting down - uncaught exception:\n{0}'.format (
			'\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback)) ) )
		sys.exit(-1)
'''
push_API = api.OAuthClient(
	client_id,
	client_secret,
	username,
	password,
)
'''


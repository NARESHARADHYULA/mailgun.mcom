from flask import Flask, render_template, jsonify, request
# from flask_mysqldb import MySQL
import MySQLdb
import json
import requests
app = Flask(__name__)
# mysql = MySQL()

# #MYSQL configurations

# app.config['MYSQL_DATABASE_USER'] = 'admin'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
# app.config['MYSQL_DATABASE_DB'] = 'Mailgun'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="Mailgun")
cur = db.cursor()


# @app.route("/")
# @app.route("/hello")
# def hello():
#     return "Hello World!"
@app.route("/home")
def home():
	return render_template('homeGun.html')

@app.route("/singleMail")
def singleMail():
	return render_template('singleMail.html')	

@app.route("/singleMailPdate")
def singleMailPdate():
	return render_template('singleMailPdate.html')	

@app.route("/singlecampaign")
def singlecampaign():
	dataget = getCampaignId()
	return render_template('singlecampaign.html',data=dataget)			

	

@app.route("/getunsubscribe")
def getunsubscribe():
	return render_template('getunsubscribe.html')

@app.route("/gotcreatecampaign")
def gotcreatecampaign():
	return render_template('gotcreatecampaign.html')




@app.route("/gotdeletecampaign")
def gotdeletecampaign():
	dataget = getCampaignId()
	return render_template('gotdeletecampaign.html',data = dataget)


@app.route("/analytics")
def analytics():
	
	dataget = getCampaignId()
	
		
	return render_template('analytics.html',data = dataget)
			
@app.route("/analyticsmain",methods=['GET'])
def analyticsmain():

	

	forward_method= request.form['options']
	_campaignId = request.form['campaignId']

	if _campaignId != "select":


		if forward_method == "getstats":
			mg= Mailgun()
			data = mg.getstats()
			return data

		elif forward_method == "getEventHistory":
			mg= Mailgun()
			data= mg.get_events_history(_campaignId)
			return data		

		elif forward_method == "getCampaignstats":
			mg= Mailgun()
			data= mg.get_events_history(_campaignId)
			return data		

		elif forward_method == "getClicks":
			mg= Mailgun()
			data= mg.get_clicks(_campaignId)
			return data	
				
		elif forward_method == "getCampaignStatsDaily":
			mg= Mailgun()
			data= mg.get_campaign_stats_dailyhourly(_campaignId)
			return data	
		elif forward_method == "getCampaignStatsRegion":
			mg= Mailgun()
			data= mg.get_campaign_stats_region(_campaignId)
			return data		

		elif forward_method == "getClicksToplinks":
			mg= Mailgun()
			data= mg.get_clicks_toplinks(_campaignId)
			return data	

		elif forward_method=="getClicksIndividual":
			mg= Mailgun()
			data= mg.get_clicks_individualLinks(_campaignId)
			return data	

		else:
			raise ValueError('select of the Feild is empty')


	else:
			raise ValueError('Please select campaignId')			

	


@app.route("/getCampaignId")
def getCampaignId():

	# conn = mysql.connect()
	# cursor =conn.cursor()
	
	cur.execute("SELECT campaignId from mailgun_details")
	value=[]
	value.append('select')
	for data in cur.fetchall():
		value.append(data[0])
	return value
	# print type(datajson)
	# data = datajson.json()
	# return data
	
	# print type(data)
	# return data


@app.route("/sendEmailWithHtml",methods=['POST'])
def sendEmailWithHtml():
	
	
	_sender = request.form['SenderEmail']
	_recepient = request.form['RecepientEmail']
	_mailSubject = request.form['Subject']
	_html = request.form['htmlData']



	if _sender and _recepient and _mailSubject and _html:

		mg = Mailgun()
		data= mg.sendEmailWithHtml(_sender,_recepient,_mailSubject,_html)
		print data

		if data == 200:
			result={'status':200, 'message':"sucess!!!"}
			return json.dumps(result)
		else:
			result={'status':data, 'message':"Some thing went wrong"}
			return json.dumps(result)
			

	else:
		raise ValueError('Some of the Feilds are empty')

	# self.validateInput(data)
@app.route("/sendEmailWithHtmlPDate",methods=['POST'])
def sendEmailWithHtmlPDate():

	
	_sender = request.form['SenderEmail']
	_recepient = request.form['RecepientEmail']
	_mailSubject = request.form['Subject']
	_html = request.form['htmlData']
	_time = request.form['time']

	if _sender and _recepient and _mailSubject and _html and time:

		mg = Mailgun()
		data= mg.sendEmailWithParticularDate(_sender,_recepient,_mailSubject,_html,_time)
		if data == 200:
			result={'status':200, 'message':"sucess!!!"}
			return json.dumps(result)
		else:
			result={'status':data, 'message':"Some thing went wrong"}
			return json.dumps(result)

	else:
		raise ValueError('Some of the Feilds are empty')

@app.route("/sendCampWithHtml",methods=['POST'])
def sendCampWithHtml():

	print "i am here"
	_sender = request.form['SenderEmail']
	_recepient = request.form['RecepientEmail']
	_mailSubject = request.form['Subject']
	_html = request.form['htmlData']
	_campaignId = request.form['campaignId']

	try:
		query="UPDATE mailgun_details SET recepeient=%s WHERE campaignId=%s "
		print query
		cur.execute( query, (_recepient, _campaignId,))
		db.commit()
		print "i am inside try"

		if _sender and _recepient and _mailSubject and _html:

			if _campaignId != "select":
				mg = Mailgun()
				data= mg.sendCampaignWithHtml(_sender,_recepient,_mailSubject,_html,_campaignId)
				print data
				if data == 200:
					result={'status':200, 'message':"sucess!!!"}
					return json.dumps(result)
				else:
					result={'status':data, 'message':"Some thing went wrong"}
					return json.dumps(result)

		else:
			raise ValueError('Some of the Feilds are empty')
	except Exception as e:

		return str(e)		


@app.route("/sendCampWithHtmlPDate",methods=['POST'])
def sendCampWithHtmlPDate():

	
	_sender = request.form['SenderEmail']
	_recepient = request.form['RecepientEmail']
	_mailSubject = request.form['Subject']
	_html = request.form['htmlData']
	_time = request.form['time']
	_campaignId = request.form['campaignId']

	try:
		query="UPDATE mailgun_details SET recepeient=%s, sendTime=%s WHERE campaignId=%s "
		cur.execute( query, (_recepient, _time, _campaignId,))
		db.commit()

		if _sender and _recepient and _mailSubject and _html and time:
			if _campaignId != "select":
				mg = Mailgun()
				data= mg.sendCampaignWithHtml(_sender,_recepient,_mailSubject,_html,_time,_campaignId)
				if data == 200:
					result={'status':200, 'message':"sucess!!!"}
					return json.dumps(result)
				else:
					result={'status':data, 'message':"Some thing went wrong"}
					return json.dumps(result)

		else:
			raise ValueError('Some of the Feilds are empty')

	except Exception as e:

		return str(e)


@app.route("/createCampaign",methods=['POST'])
def createCampaign():

	
	_campainName = request.form['campaignName']
	_campaignId = request.form['campaignId']
	

	try:
		
		# return data



		if _campainName and _campaignId:

			mg = Mailgun()
			data= mg.create_campaign(_campainName,_campaignId)
			print str(data)+ " in create campaign test"
			if data == 200:
				cur.execute("INSERT into mailgun_details(campaignName,campaignId) values (%s,%s) ",(_campainName,_campaignId))
				db.commit()
				print "registered"
				result={'status':200, 'message':"sucess!!!"}
				return json.dumps(result)
			else:
				result={'status':data, 'message':"Some thing went wrong"}
				return json.dumps(result)

		else:
			raise ValueError('Some of the Feilds are empty')
	except Exception as e:

		return str(e)
			

@app.route("/deleteCampaign",methods=['POST'])
def deleteCampaign():

	_campaignId = request.form['campaignId']
	try:
		
		
		

		if _campaignId:

			mg = Mailgun()
			data= mg.delete_campaign(_campaignId)
			if data == 200:
				delstatmt = "DELETE FROM mailgun_details WHERE campaignId = %s"
				print delstatmt
				cur.execute(delstatmt,(_campaignId,))
				db.commit()
				result={'status':200, 'message':"sucess!!!"}
				return json.dumps(result)
			else:
				result={'status':data, 'message':"Some thing went wrong"}
				return json.dumps(result)	

		else:
			raise ValueError('Some of the Feilds are empty')
	except Exception as e:

		return render_template('result.html',data="failed")


@app.route("/getCampaign",methods=['GET'])
def getCampaign():

	mg = Mailgun()
	data = mg.get_campaigns()
	return render_template('result.html',data=data)



@app.route("/getListMembers",methods=['GET'])
def getListMembers():

	mg = Mailgun()
	return mg.list_members()

@app.route("/getUnsubscribers",methods=['GET'])
def getUnsubscribers():

	mg = Mailgun()
	data= mg.get_unsubscribes()
	# if data == "400":
	# 	result = {}
	# 	return "Some thing went wrong while Retrieving Data"
	# else:
	return data	

@app.route("/getStats",methods=['GET'])
def getStats():

	mg = Mailgun()
	data= mg.get_stats()
	return data	

@app.route("/unsubscribe",methods=['POST'])
def unsubscribe():


	_emailAddress = request.form['emailAddress']

	if _emailAddress:

		mg = Mailgun()
		data= mg.unsubscribe(_emailAddress)
		if data == 200:
			result={'status':200, 'message':"sucess!!!"}
			return json.dumps(result)
		else:
			result={'status':data, 'message':"Some thing went wrong"}
			return json.dumps(result)

	else:
		raise ValueError('Some of the Feilds are empty')

class Mailgun:

	api = "key-6c4b51a59737c41b7993df473b6a9a90"
	mainurl="https://api.mailgun.net/v3/sandboxa9488fa3f550449a8ec780ec9c57794d.mailgun.org"



	def sendEmailWithHtml(self, sender, to, subject, html):
		print "even i am entered here"
		url=self.mainurl+"/messages"
		diction = {"from": sender,
				  "to": to,
				  "subject": subject,
				  "html": html,
				  "o:tracking": True}
		data = self.get_post(url,diction)
		print data
		return data			  


		# requests.post(url,
		# 			auth=("api", self.api),
					
		# 			data={"from": sender,
		# 				  "to": to,
		# 				  "subject": subject,
		# 				  "html": html,
		# 				  "o:tracking": True})
		# print "success"
		# return "Sucess!"				   

	
	def sendEmailWithParticularDate(self, sender, to, subject, html, time):
		url= self.mainurl+"/messages"
		diction = {"from": sender,
				  "to": to,
				  "subject": subject,
				  "html": html,
				  "o:tracking": True,
				  "o:deliverytime": time}
		data = self.get_post(url,diction)
		return data		  

		# requests.post(url,
		# 			auth=("api", self.api),
					
		# 			data={"from": sender,
		# 				  "to": to,
		# 				  "subject": subject,
		# 				  "html": html,
		# 				  "o:tracking": True,
		# 				  "o:deliverytime": time})
		# return "sucess!"

	def sendCampaignWithHtml(self, sender, to, subject, html,campaignId):

		url =self.mainurl+"/messages"
		diction={"from": sender,
				  "to": to,
				  "subject": subject,
				  "html": html,
				  "o:tracking": True,
				  "o:campaign" : campaignId}
		data = self.get_post(url,diction)
		return data			  

		# requests.post(url,
		# 			auth=("api", self.api),
					
		# 			data={"from": sender,
		# 				  "to": to,
		# 				  "subject": subject,
		# 				  "html": html,
		# 				  "o:tracking": True,
		# 				  "o:campaign" : campaignId
						  
		# 				  }) 
		# return "sucess!"

	
	def sendcampaignWithParticularDate(self, sender, to, subject, html, time,campaignId):

		url =self.mainurl+"/messages"
		diction ={"from": sender,
				  "to": to,
				  "subject": subject,
				  "html": html,
				  "o:tracking": True,						  
				  "o:deliverytime": time,
				  "o:campaign": campaignId }
		data = self.get_post(url,diction)
		return data		  
		# requests.post(url,
		# 			auth=("api", self.api),
					
		# 			data={"from": sender,
		# 				  "to": to,
		# 				  "subject": subject,
		# 				  "html": html,
		# 				  "o:tracking": True,						  
		# 				  "o:deliverytime": time,
		# 				  "o:campaign": campaignId
		# 				   })
		# return "sucess!"				   	


	# this methods is optional 
	# def create_mailing_list(self, yourDomainAddress, description):

	# 	return requests.post(
	# 		"https://api.mailgun.net/v3/lists",
	# 		auth=('api', self.api),
	# 		data={'address': yourDomainAddress,
	# 			  'description': description})


	def create_campaign(self, name, cid):


		url = self.mainurl+"/campaigns"
		print url
		print name,cid
		diction = {'name':name,
				  'id':cid}
		data = self.get_post(url,diction)
		print str(data)+" what is going on"
		return data
		# data=requests.post(
		# 	url,
		# 	auth=('api', self.api),
		# 	data={'name':name,
		# 		  'id':cid})
		# return data.status_code		  		
		
	def delete_campaign(self, cid):

		url= self.mainurl+"/campaigns/"+cid
		data=requests.delete(
			url,
			auth=('api', self.api))
		return data.status_code	
			
	


	def get_campaigns(self):

		url=self.mainurl+"/campaigns"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api))    


	def get_events_history(self, campaignId):

		url=self.mainurl+"/campaigns/"+campaignId+"/events?limit=2"
		data = self.get_requests(url)
		return data
		# return requests.get(url,
		# 	auth=('api', self.api))


	def get_campaign_stats(self,campaignId):
		
		url=self.mainurl+"/campaigns/"+campaignId+"/stats"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api))

	def get_clicks(self, campaignId):
		
		url=self.mainurl+"/campaigns/"+campaignId+"/clicks?groupby=recipient&limit=2"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api)) 

	def get_campaign_stats_dailyhourly(self, campaignId):
		
		url=self.mainurl+"/campaigns/"+campaignId+"/stats?groupby=daily_hour"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api))    

	def get_campaign_stats_city(self, campaignId):
		
		url=self.mainurl+"/campaigns/"+campaignId+"/stats?groupby=city"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api))    

	def get_campaign_stats_region(self, campaignId):
		
		url=self.mainurl+"/campaigns/"+campaignId+"/stats?groupby=region"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api))    
	

	def get_clicks_toplinks(self, campaignId):
		
		url=self.mainurl+"/campaigns/"+campaignId+"/clicks?groupby=link"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api)) 

	def get_clicks_individualLinks(self, campaignId):
		
		url=self.mainurl+"/campaigns/"+campaignId+"/clicks?groupby=link&groupby=recipient"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api)) 

	def list_members(self):

		url="https://api.mailgun.net/v3/lists/pages"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=('api', self.api))
	

	def get_unsubscribes(self):

		url=self.mainurl+"/unsubscribes"
		data = self.get_requests(url)
		return data
		# return requests.get(
		# 	url,
		# 	auth=("api", self.api))


	def unsubscribe(self, address):

		url=self.mainurl+"/unsubscribes"
		diction = {'address': address, 'tag': '*'}
		
		data = self.get_post(url,diction)
		return data
		# requests.post(
		# 	url,
		# 	auth=("api", self.api),
		# 	data={'address': address, 'tag': '*'})
		# return "sucess!"
	

	def get_stats(self):

		url=self.mainurl+"/stats/total"
		data= requests.get(
			url,
			auth=("api", self.api),
			params={"event": ["accepted", "delivered", "failed"],
					"duration": "1m"}) 
		if data==200:
			return data.text
		else:
			return data.status_code	


	def get_requests(self,url):

		data = requests.get(url,
			auth=('api', self.api))

		if data.status_code==200:
			result={'status':data.status_code,'message':data.text}
			return json.dumps(result)
		else:
			result={'status':data.status_code,'message':"Some thing went wrong"}
			return json.dumps(result)

	def get_post(self,url,diction):

		print "i am in get_post"
		data= requests.post(
			url,
			auth=("api",self.api),
			data=diction)
		print data.status_code
		# if data.status_code==200:
		# 	print "what happened"
		# 	return data.status_code
		# else:
		return data.status_code
		
			
			




	
if __name__ == "__main__":
	app.debug = True
	app.run(port = 5000)

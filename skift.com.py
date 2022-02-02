# -*- coding: utf-8 -*-
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
import sys
import time
import re
reload(sys)
sys.setdefaultencoding('utf-8')
conn = MySQLdb.connect('localhost', 'root', 'Huawei_2018', 'News',charset='utf8', use_unicode=True)
cursor = conn.cursor()
#cursor.execute("SELECT max(`number`) FROM News WHERE `author` = 'otzyv.ru'")
#f = cursor.fetchone()
#outfile = open('out.csv','w')
#infile = open('out.csv','r')
sys.setdefaultencoding('utf-8')
i=1
while i<=1 :
	link =  'https://skift.com/news/page/'+str(i)+'/'
	print link	 
	req = urllib2.Request(link, headers={'User-Agent': "Magic BROESER"})
	website = urllib2.urlopen(req)
	html = website.read()
	soup = BeautifulSoup(html, 'html.parser')
	soup.originalEncoding
	try:
		for content in soup.find_all('div', class_="story"):
			#print content						
			if content.name != None:
				headler=content.h2.text
				if headler != None:
					headler=headler.replace('"','\"')
					headler=headler.replace("'","\\\'")
					headler=headler.replace("-","\-")
					headler=headler.replace("$","\$")
					headler=headler.replace("*","\*")
					headler=headler.replace(".","\.")
					headler=headler.strip()
					print headler				
				try:
					img1=content.img['src']
					print img1
				except:
					img1=''
					print "err img"
				try:
					link1=content.a['href']
					print link1
				except:
					print "err link"
				req = urllib2.Request(link1, headers={'User-Agent': "Magic BROESER"})
				website = urllib2.urlopen(req)
				html = website.read()
				soup = BeautifulSoup(html, 'html.parser')
				try:
					notes=soup.find('div', class_="post-copy").text.strip()
					if notes != None : 
						if len (notes)>200 :
							notes = (notes[:200] + '...') 
							notes=notes.strip()
							notes=notes.replace('"','\"')
							notes=notes.replace("'","\\\'")
							notes=notes.replace("-","\-")
							notes=notes.replace("$","\$")
							notes=notes.replace("*","\*")
							notes=notes.replace(".","\.")
							print notes
				except:		
					notes=""
					print "err notes"
				try:		
					content=soup.find('div', class_="post-copy")
					art=''
					if content != None:
						con=str(content).replace('"','\"')
						con=con.replace("'","\\\'")
						con=con.replace("-","\-")
						con=con.replace("$","\$")
						con=con.replace("*","\*")
						con=con.replace(".","\.")				
						print con
					else:
						con=""
					art += "<"+str(content.name)+">" + con + "</"+str(content.name)+">"	
				except:
					art=""
					print "err art"
				source=unicode(art, errors='replace')+ '<p>Source :<a href="' + link1 + '"> Skift.com</a></p>'
				try:
					stamp=soup.find('div', class_="post-date").text
					stamp.strip()
					stamp=stamp.replace(' - ', '')
					#stamp=stamp.replace(' ', '')
					# - Dec 28, 2018 2:30 am
					d = int(time.mktime(time.strptime(stamp,'%b %d, %Y %I:%M %p')))
					date = time.strftime("%d.%m.%Y %H:%M", time.localtime(d))
					print stamp
					print date
					print d
				except:
					d=""
					date=""
					print "err date"				
				if (headler!="") or (art!=""):
					cursor.execute("SELECT max(`number`) FROM News WHERE `author` = 'skift.com' and `headler`='"+headler+"'")
					f = cursor.fetchone()
					print str(f)
					if f[0] == None:
						print "no"
						cursor.execute("INSERT INTO News (`timestamp`,`date`,`author`,`country`,`language`,`headler`,`notes`,`article`, `map`, `picture`, `video`, `views`, `status`, `number`, `tag`) VALUES ('"+str(d)+"','"+str(date)+"', 'skift.com','', 'en','"+headler+"','"+str(notes)+"','"+source+"', '', '"+img1+"' ,'', '','ok', '"+str(i)+"','' )")	
						conn.commit()
	except urllib2.HTTPError, e:
	  print('HTTPError ='+ str(e.code))
	except urllib2.URLError, e:
	  print('URLError ='+ str(e.reason))
	i+=1
conn.close()
#!/home/mraz/anaconda3/bin/python3
#########################
#
#  i just read from mysql
#  transform, filter
#  and plot data 
#
##########################
import sys  # arguments
import os
from os.path import expanduser   #home dir
import time  #sleep
import datetime
from datetime import date
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  #  DISPLAY=:0  not necessary BEFORE pyplot imported!!!
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # to plot date intervals

import mysql.connector


debugsleep=0.1

def unglitch(li):
	for i in range( len(li)-2):
		#print(i)
		delta=abs(li[i]-li[i+2])
		if  abs(li[i]-li[i+1])>3*delta and abs(li[i+1]-li[i+2])>3*delta:
			li[i+1]=(li[i]+li[i+2])/2
	#li=li
	return li



####################
#
# graphs :  tempin  tempout  humid  dew 
#
####################
fpath   ='/tmp/'
ftempin =fpath+'tempin.jpg'
ftempout=fpath+'tempout.jpg'
fhumid  =fpath+'humid.jpg'
fdew    =fpath+'dew.jpg'
frain   =fpath+'rain.jpg'
#################################################
#
#  DATES  and interval :  week
#
#################################################




today = datetime.datetime.now()
INTERACTIVE=0
#print('Number of arguments:', len(sys.argv), 'arguments.')
print( 'Argument List:', str(sys.argv))
one_day = datetime.timedelta(hours=24)
one_dayp = datetime.timedelta(hours=48)
if (len(sys.argv)>1):
	if ( sys.argv[1] == 'twoweeks'):
		one_day = datetime.timedelta(hours=168*2)	
		one_dayp=datetime.timedelta(hours=168*2+24)
		INTERACTIVE=1
	if ( sys.argv[1] == 'week'):
		one_day = datetime.timedelta(hours=168)
		one_dayp = datetime.timedelta(hours=168+24)
		INTERACTIVE=1
	if ( sys.argv[1] == 'day'):
		one_day = datetime.timedelta(hours=24)
		one_dayp = datetime.timedelta(hours=48)
		INTERACTIVE=1


print('i... Interval =  :', one_day)
week = today - one_day
weekp= today-one_dayp

realweek = today - datetime.timedelta(hours=168)
yesterday=today - one_day
tommorow=today + one_day
print('i... from',week,' till ',today )

home = expanduser("~")
print('home ok')
time.sleep( debugsleep )

#print('ctime:', today.ctime() , home)
#exit(0)
##########################
#
#  MYSQL
#
##########################
dbase='test'  ## TEST dbase feat
table='db'
with open(home+'/.'+table+'.mysql', 'r') as content:
    allf = content.read().split('\n')
print('mysql db=',allf[0])
config = {
  'user': allf[1],  'password': allf[2],  'host': allf[0],
  'database': dbase,  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
query =("SELECT * FROM "+table+" WHERE t > '"+str(week)+"' ORDER BY t DESC")
print(query)
cursor.execute(query)

print('1st query ok')
time.sleep( debugsleep )

listx=np.array( list([i for i in cursor]) )
print( 'mysql curson=',listx )
#listx[:,1]=unglitch(listx[:,1])  # red T
#listx[:,2]=unglitch(listx[:,2])  #  red H
#listx[:,3]=unglitch(listx[:,3])   # black T
#listx[:,4]=unglitch(listx[:,4])   # black H
listx[:,5]=unglitch(  list(listx[:,5]) )   # cyan T   glitchin
listx[:,6]=unglitch( list(listx[:,6]) )   # cyan H
listx[:,2]=0.9*listx[:,2] ## COMPENSATION FOR HUMIDITY 110%

print('going to do DEW')
time.sleep( debugsleep )

#######################
#print( 'test', np.log( list(listx[:,6]) ) )
DEWP56=243.04*(np.log( list(listx[:,6]/100.0) )+((17.625*listx[:,5])/(243.04+listx[:,5])))/(17.625-np.log( list(listx[:,6]/100.0))-((17.625*listx[:,5])/(243.04+listx[:,5])))
DEWP12=243.04*(np.log( list(listx[:,2]/100.0) )+((17.625*listx[:,1])/(243.04+listx[:,1])))/(17.625-np.log( list(listx[:,2]/100.0))-((17.625*listx[:,1])/(243.04+listx[:,1])))
DEWP34=243.04*(np.log( list(listx[:,4]/100.0) )+((17.625*listx[:,3])/(243.04+listx[:,3])))/(17.625-np.log( list(listx[:,4]/100.0))-((17.625*listx[:,3])/(243.04+listx[:,3])))
df=pd.DataFrame( listx  , columns=cursor.column_names )
#print(df)
#######################################################END OF MYSQL 1
#week=today -  datetime.timedelta(hours=168)



table='forecast'
print( table ,'============================')
with open(home+'/.'+table+'.mysql', 'r') as content:
    allf = content.read().split('\n')
print(allf[0])
config = {
  'user': allf[1],  'password': allf[2],  'host': allf[0],
  'database': dbase,  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
#query =("SELECT * FROM "+table+"  ORDER BY t DESC LIMIT 1")
query=("SELECT * FROM "+table+" WHERE t > '"+str(weekp)+"'  ORDER BY t DESC")

print(query)
cursor.execute(query)
listf=np.array( list([i for i in cursor]) )
dff=pd.DataFrame( listf, columns=cursor.column_names )
print(dff)





table='rain3'
print( table ,'============================')
with open(home+'/.'+table+'.mysql', 'r') as content:
    allf = content.read().split('\n')
print(allf[0])
config = {
  'user': allf[1],  'password': allf[2],  'host': allf[0],
  'database': dbase,  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
query =("SELECT * FROM "+table+" WHERE t > '"+str(week)+"' ORDER BY t DESC")
print(query)
cursor.execute(query)
listy=np.array( list([i for i in cursor]) )
dfr=pd.DataFrame( listy, columns=cursor.column_names )
print(dfr)





table='ping8'
print( table ,'============================')
with open(home+'/.'+table+'.mysql', 'r') as content:
    allf = content.read().split('\n')
print(allf[0])
config = {
  'user': allf[1],  'password': allf[2],  'host': allf[0],
  'database': dbase,  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
query =("SELECT * FROM "+table+" WHERE t > '"+str(realweek)+"' ORDER BY t DESC")
print(query)
cursor.execute(query)
listp=np.array( list([i for i in cursor]) )
dfp=pd.DataFrame( listp, columns=cursor.column_names )
print(dfp)



#exit(0)
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.dates import MONDAY
# every 3rd month
#mondays = WeekdayLocator(MONDAY)
#months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
#fig = plt.figure(figsize=(4, 3), dpi=100 )
########################
#
#     OUT dewpoint ..... temp
#
###########################
monthsFmt = DateFormatter("%H:%M(%d)")
fig, ax = plt.subplots( figsize=(6, 5), dpi=100 )
#####ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)#nice diagonal format
####ax.xaxis.set_minor_locator(mondays)
#####ax.autoscale_view()
####ax.grid(True)
####fig.autofmt_xdate()
plt.plot( df.t, df.a ,'r.-')
plt.plot( df.t, DEWP12 ,'r--', linewidth=2)
########plt.plot( df.t, df.b ,'r.-')
#plt.plot( df.t, df.c ,'k.-')
plt.plot( df.t, DEWP34 ,'k--', linewidth=2)
#plt.plot( df.t, df.d ,'k.-')
#plt.plot( df.t, df.e ,'c.-')
#plt.plot( df.t, DEWP56 ,'c--', linewidth=2)
#plt.plot( df.t, df.f ,'c.-')
#plt.plot( df.t, df.g ,'m.-', label='topeni')
plt.plot( df.t, df.h ,'g.-')

############ my way to span datetimes :
xmin, xmax = plt.gca().get_xlim()

#dffrepl=dff.t[0].replace(hour=5, minute=30)  #not necessary
#x1=datetime.datetime.strptime(dffrepl.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S' ).toordinal()+(3600*5)/24/3600
# .timestamp() IS unix seconds....
#x2=datetime.datetime.strptime(dffrepl.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S' ).toordinal()+3600*23.9/24/3600

import matplotlib.dates as dt

for i in range(0, len(dff.index) ):
	qqq= pd.to_datetime( dff.t[i] )
#	qqq= dff.t[i].to_pydatetime()
	x1= dt.date2num(  qqq  )
	x2= x1+0.99
	print(i,'x1,x2',x1,x2)
	x1,x2=([x1,x2]-xmin)/(xmax-xmin)
	p = plt.axhspan( dff.b[i], dff.a[i], xmin=x1,xmax=x2, facecolor='r', alpha=0.1)
	#p = plt.axhspan( dff.b[0], dff.c[0], xmin=x1+1,xmax=x2, facecolor='r', alpha=0.1)
	plt.axhline(y=dff.a[i], xmin=x1,xmax=x2, linewidth=1, color='r')
	plt.axhline(y=dff.b[i], xmin=x1,xmax=x2, linewidth=1, color='r')

#print(xmin, ' -  ',x1,x2, '  -  ',xmax,' time=', dff.t[0],'replaced:',dffrepl)
#x1,x2=([x1,x2]-xmin)/(xmax-xmin)
#print(xmin, ' -  ',x1,x2, '  -  ',xmax,' time=', dff.t[0],'replaced:',dffrepl)
#time.sleep( debugsleep )

#p = plt.axhspan( dff.b[0], dff.a[0], xmin=x1,xmax=x2, facecolor='r', alpha=0.1)
#p = plt.axhspan( dff.b[0], dff.c[0], xmin=x1+1,xmax=x2+1, facecolor='r', alpha=0.1)
#plt.axhline(y=dff.a[0], xmin=x1, linewidth=1, color='r')
#plt.axhline(y=dff.b[0], xmin=x1, linewidth=1, color='r')
##print('df + FORECAST==============================:')
##print(df)
##time.sleep(5)

plt.grid(True)
plt.gcf().autofmt_xdate()
plt.savefig( fdew , bbox_inches='tight')


#############################
#
#   IN
#
############################
fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
#ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
#ax.xaxis.set_minor_locator(mondays)
#ax.autoscale_view()
#ax.grid(True)
#fig.autofmt_xdate()
#plt.plot( df.t, df.a ,'r.-')
#plt.plot( df.t, df.b ,'r.-')  #HUMI
plt.plot( df.t, df.c ,'k.-')
plt.plot( df.t, DEWP34 ,'k--', linewidth=2, label='kuchyne')
#plt.plot( df.t, df.d ,'k.-')   #HUMI
plt.plot( df.t, df.e ,'c.-')
plt.plot( df.t, DEWP56 ,'c--', linewidth=2, label='koupelna')
#plt.plot( df.t, df.f ,'c.-')     #HUMI
plt.plot( df.t, df.g ,'m.-' , label='topeni')
#plt.plot( df.t, df.h ,'g.-')

flow= (abs(df.c-df.a) + (df.c-df.a))/2  
flowavg=sum( list(flow) )/float(len(  list(flow)) )

#df['flowavg']=flowavg  # I Create new pandas column like this
print('FLOW...avg = %.2f W/m2/const' %   flowavg )

##### YELLOW DTEMP
#plt.plot( df.t, flow ,'y.-')
####plt.plot( df.t, df.flowavg ,'y:', linewidth=5  )
#### YELLOW LINE
#p = plt.axhspan( 0, flowavg , facecolor='y', alpha=0.1)
p = plt.axhline(y=flowavg,  linewidth=2, color='y')


plt.grid(True)
plt.gcf().autofmt_xdate()
plt.savefig(  ftempin  , bbox_inches='tight')

#####################################
#
#    HUMIDITY
#
#######################################
fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
#ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
#ax.xaxis.set_minor_locator(mondays)
#ax.autoscale_view()
#ax.grid(True)
#fig.autofmt_xdate()
#plt.plot( df.t, df.a ,'r.-')
#I DOIT EARLIER df.b = df.b*0.9 # KOREKCE 110% vlhkosti obcas
plt.plot( df.t, df.b ,'r.-') 
#plt.plot( df.t, df.c ,'k.-')
plt.plot( df.t, df.d ,'k.-')
#plt.plot( df.t, df.e ,'c.-')
plt.plot( df.t, df.f ,'c.-')
#plt.plot( df.t, df.g ,'m.-')
#plt.plot( df.t, df.h ,'g.-')
plt.grid(True)
plt.gcf().autofmt_xdate()
plt.savefig( fhumid , bbox_inches='tight')


##############################################
#
#  RAIN
#
#
########################

print('i... going to plot', frain )
fig, ax = plt.subplots(figsize=(6,5), dpi=100)
#ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.set_ylim( 0, 1.02*max( [0.1,  max(listy[:,1]) ,max(listy[:,2]) ] ) )
#week wid=0.01
wid=0.02
plt.bar( listy[:,0] , listy[:,2] , width=wid ,color='magenta', edgecolor="none",linewidth=0 )
plt.bar( listy[:,0] , listy[:,1] , width=wid/2 , alpha=0.7 , 
				color='cyan',edgecolor="none",linewidth=0  )
#plt.bar( listy[:,0]+wid , listy[:,2] , width=wid )
#print( listy )
plt.grid(True)
#plt.yscale( 'log' , nonposy='clip')
plt.gcf().autofmt_xdate()
plt.savefig(  frain  , bbox_inches='tight')
print('i... fig saved ', frain )

#plt.show()
#import Image
#Image.open('testplot.png').save('testplot.jpg','JPEG')



if (INTERACTIVE==0):
	
	#########################################################
	#
	#
	#   PLOT GRAPHS   WITH  --- -  PING
	#
	#
	###########################################################
	print('------------------ PREPARING PINGS')
	from random import randint
	hosts=['pi','pi3','pib','phid05','phid04','pim', 'pi4', 'pix1']
	#print(dfp)
	for i in range(len(hosts)-1):
	#for i in range(1):
		#i=0
	#	fig, ax = plt.subplots(figsize=(120,240), dpi=1)  # width 24 
		fig, ax = plt.subplots( )  # width 24 
		img = np.zeros([12,24,4],dtype=np.uint8)
		img[:,:,3]= 0
		h,w = len(img), len(img[0])
		ye=[25,55,25]
		print('i=',  i , hosts[i] ,'===========================')
		#for j in range(8):
			#print('list:',  j,int(dfp.iloc[:,[i+1]].ix[j]) )
		#print( 'len=' , len(dfp) )
		cell=0
		a=datetime.datetime.now()
	
		for j in range( len(dfp) ):
			#delt = datetime.timedelta(hours=0.5*cell)
			#a2=a-delt
			ptdt=dfp.iloc[:,[0]].ix[j].dt #.strftime('%Y-%m-%d %H:%M:%S') 
			dstr='%4d-%02d-%02d %d:%02d:%02d' % (int(ptdt.year),int(ptdt.month),int(ptdt.day),int(ptdt.hour),int(ptdt.minute),int(ptdt.second)  ) 
			dpanda=datetime.datetime.strptime( dstr, '%Y-%m-%d %H:%M:%S')
			diff= (dpanda-a).total_seconds()
			y= int( abs(diff)/1800)
			x= int( y % w )
			y= int( y / w )
			#print(x,y,diff)
			if (( x<w)and(y<h)):
				#print(x,y)
				if ( int( dfp.iloc[:,[i+1]].ix[j] )>=0 ):
					#if ( int( dfp.iloc[:,[i+1]].ix[x+y*h] )==1):
					gree=[ 255-50+randint(0,50), randint(0,70), randint(0,70) , 255 ]
					#print(x,y,gree)
					img[y,x] = gree
				if ( int( dfp.iloc[:,[i+1]].ix[j] )>=1 ):
					#if ( int( dfp.iloc[:,[i+1]].ix[x+y*h] )==1):
					#gree=[ 44-50+randint(0,50), 255-50+randint(0,50) , 0 , 255  ]
					#gree=[ 255-30+randint(0,30), 255-30+randint(0,30),  randint(0,180) , 255 ]
					#print(x,y,gree)
					img[y,x][1] =  255-30+randint(0,30)
				if ( int( dfp.iloc[:,[i+1]].ix[j] )>=99 ):
					#if ( int( dfp.iloc[:,[i+1]].ix[x+y*h] )==1):
					gree=[ randint(0,80), 255-40+randint(0,40) , randint(0,80) , 255  ]
					#gree=[ 255-50+randint(0,50), 255-50+randint(0,50) , 0 , 255  ]
					#print(x,y,gree)
					#img[y,x][2] =  255-30+randint(0,30)
					img[y,x][0] =  randint(0,30)
	
		#plt.imshow(img, interpolation='lanczos') 
		plt.imshow(img, interpolation='None'  ) 
		plt.axis('off')
		print( 'saving /tmp/'+hosts[i]+'B.png' )
	#	plt.savefig( '/tmp/'+hosts[i]+'B.png' , bbox_inches='tight' , transparent=True)
		fig.set_size_inches(w,h)
		fig.savefig( '/tmp/'+hosts[i]+'B.png' , dpi=4, transparent=True, bbox_inches='tight', pad_inches=0)
	










##############################################
#
#   COMPOSE argumented /day/week/ PLOT - no delays
#
#   + ELEKTROMERY
########################


if (INTERACTIVE==0):
	print(' echo sleeping 900 sec for the next frame ....')
	time.sleep(900)
else:
	print('join',ftempin,fdew,fhumid,frain)
	CMD='montage '+ftempin+' '+fdew+' '+fhumid+' '+frain+' -geometry 500x500>+0+0 -tile 2x2 /tmp/final.jpg'
	print('Monntage...:',CMD)
	if (os.system( CMD )!=0):
		print('error with '+CMD)
		exit(1)

	table='elektromery'
	with open(home+'/.'+table+'.mysql', 'r') as content:
	    allf = content.read().split('\n')
	print(allf[0])
	config = {
  	'user': allf[1],  'password': allf[2],  'host': allf[0],
  	'database': dbase,  'raise_on_warnings': True,
	}
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query =("SELECT * FROM "+table+" ORDER BY t DESC LIMIT 2;")
	print(query)
	cursor.execute(query)
	liste=np.array( list([i for i in cursor]) )
	dfe=pd.DataFrame( liste, columns=cursor.column_names )
	print(dfe)

	dte=(dfe.t[0]-dfe.t[1]).total_seconds()
	da=(dfe.a[0]-dfe.a[1])/dte*24*3600
	db=(dfe.b[0]-dfe.b[1])/dte*24*3600
	dc=(dfe.c[0]-dfe.c[1])/dte*24*3600
	dd=(dfe.d[0]-dfe.d[1])/dte*24*3600

	datt=(dfe.a[0]-dfe.a[1])
	dbtt=(dfe.b[0]-dfe.b[1])
	dctt=(dfe.c[0]-dfe.c[1])
	ddtt=(dfe.d[0]-dfe.d[1])

#	flowss='Avg T_diff=%5.1f ' % (flowavg)
	deltas='DELTAS: %.0f days;  %.0f highT %.0f lowT  %.0f HPump %.0f Water... Flow %5.1f deg' % (dte/3600/24, datt, dbtt, dctt, ddtt, flowavg)
	deltas2='DELTAS: %.0f seconds; perDAY: %.1f highT %.1f lowT  %.1f HPump %.1f Water' % (dte, da, db, dc, dd)
	annot='ELEKTROMERY= '+'  '.join( map( str,liste[0] ) )
	annot2='ELEKTROMERY= '+'  '.join( map( str,liste[1] ) )
	annot=annot+'\n\n'+deltas+'\n\n'+deltas2
	CMD='convert /tmp/final.jpg -fill black -gravity west -font Courier -pointsize 20  -undercolor \'#00000100\'  -annotate  +10+10 "'+annot+'" /tmp/finala.jpg'
	print('FNAME...',CMD)
	if (os.system( CMD )!=0):
		print('error with '+CMD)
		exit(1)

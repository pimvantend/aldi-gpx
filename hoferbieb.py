#!/usr/bin/env python

#from aldihu import verwerkpostcodech
#from aldihu import maakgpx
import re,mechanize,time,cPickle,glob,htmllib

def unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()


def verwerkpostcodech(postcode,land1):
    if land1=='ch':
	mapaanvraag='https://www.aldi-suisse.ch/filialen/de-ch/Search?SingleSlotGeo='
	gewenst='ALDI'
	nietgewenst='Hofer'
    elif land1=='at':
	mapaanvraag='https://www.hofer.at/filialen/de-at/Search?SingleSlotGeo='
	gewenst='Hofer'
	nietgewenst='ALDI'
    elif land1=='si':
	mapaanvraag='https://www.hofer.si/poslovalnice/sl-si/Search?SingleSlotGeo='
	gewenst='Hofer'
	nietgewenst='ALDI'
    elif land1=='hu':
	mapaanvraag='https://www.aldi.hu/uzletek/hu-hu/Search?SingleSlotGeo='
	gewenst='ALDI'
	nietgewenst='Hofer'
#    time.sleep(3)
    mapaanvraag1=mapaanvraag+postcode
    print mapaanvraag1
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders =  [('User-agent', 'Firefox')]
    bestand=br.open(mapaanvraag1)
#bestand=open('Search?SingleSlotGeo=9430','r')
    tekst=bestand.read()
# postcode eenduidigheid
    reguliere=re.compile(r'<b>(.*?)</b>')
    tussenstaplijst=reguliere.findall(tekst)
    print tussenstaplijst
    if len(tussenstaplijst)>0:
	postcodevoorstel=tussenstaplijst[0]
	reguliere=re.compile(r'</b> (.*?)\r')
	plaatsnamenlijst=reguliere.findall(tekst)
	print plaatsnamenlijst
	plaatsnaamvoorstel=plaatsnamenlijst[0]
	mapaanvraag1=mapaanvraag+plaatsnaamvoorstel+','+postcodevoorstel
	print mapaanvraag1.replace(' ',r'%20')
	if ' ' not in mapaanvraag1:
	    bestand=br.open(mapaanvraag1)
	    tekst=bestand.read()
    reguliere=re.compile(r'==&quot;,&quot;locX&quot;:&quot;(.*?)&quot;,&quot;locY&quot;:&quot;')
    xlijst=reguliere.findall(tekst)
#print xlijst
    reguliere=re.compile(r'&quot;,&quot;locY&quot;:&quot;(.*?)&quot;,&quot;bcInformation')
    ylijst=reguliere.findall(tekst)
#print ylijst
    reguliere=re.compile(r'div itemprop="streetAddress" class="resultItem-Street"\>(.*?)<\/div>')
    straatlijst=reguliere.findall(tekst)
#print straatlijst
    reguliere=re.compile(r'">([1-9][0-9][0-9][0-9] .*?)<\/div>')
    plaatslijst=reguliere.findall(tekst)
#print plaatslijst
    reguliere=re.compile(r'<strong class="resultItem-CompanyName" itemprop="name">(.*?)<\/strong>')
    winkellijst=reguliere.findall(tekst)
#print winkellijst
    regellijst=[]
    for (lon,lat,winkel) in zip(xlijst,ylijst,winkellijst):
	if winkel==gewenst:
#	print winkel
	    plaats=plaatslijst.pop(0)
	    straat=straatlijst.pop(0)
	    regel=lon+' '+lat+' '+winkel+' '+straat+', '+plaats
	    if land1=='at' or land1=='ch':
		reguliere=re.compile('&#(.*?);')
		speciaal=reguliere.findall(regel)
#		print speciaal
		for getal in speciaal:
		    regel=regel.replace('&#'+getal+';',unichr(int(getal)))
		print regel
		regel=regel.replace('&#39;',"'")
		regel=regel.replace('&#220;','Ue')
		regel=regel.replace('&#223;','ss') # ringeles
		regel=regel.replace('&#226;','a')
		regel=regel.replace('&#228;','ae')
		regel=regel.replace('&#232;','e')
		regel=regel.replace('&#233;','e')
		regel=regel.replace('&#234;','e') # dakje
		regel=regel.replace('&#246;','oe')
		regel=regel.replace('&#252;','ue')
	    else:
		regel=unescape(regel)
#	print regel
	    regellijst+=[regel]
	elif winkel==nietgewenst:
#	print winkel
	    plaats=plaatslijst.pop(0)
	    straat=straatlijst.pop(0)
#	regel=lon+' '+lat+' '+winkel+' '+straat+' '+plaats
#	print regel
	else:
#	print winkel
	    straat=straatlijst.pop(0)
    print len(xlijst),len(ylijst),len(winkellijst),len(straatlijst),len(plaatslijst)
    return regellijst

def maakgpx(regellijst,land,*args):
    import codecs
    if land=='F':
	land1='fr'
    elif land=='B':
	land1='be'
    elif land=='D':
	land1='de'+args[0]
    else:
	land1=land.lower()
    doelbestand='aldi-'+land1+'.gpx'
    if land in ['at','ch']:
	doelbestand=codecs.open(doelbestand,encoding='utf-8',mode='w')
    else:
	doelbestand=open(doelbestand,'w')
    doelbestand.write( u'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    doelbestand.write( u'<gpx version="1.1" creator="Locus Android"\n')
    doelbestand.write( u' xmlns="http://www.topografix.com/GPX/1/1"\n')
    doelbestand.write( u' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    doelbestand.write( u' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"\n')
    doelbestand.write( u' xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"\n')
    doelbestand.write( u' xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"\n')
    doelbestand.write( u' xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"\n')
    doelbestand.write( u' xmlns:locus="http://www.locusmap.eu">\n')
    for regel in regellijst:
	[lon,lat,adres]=regel.split(' ',2)
	try:
	    doelbestand.write(u'<wpt lat="'+lat+u'" lon="'+lon+u'">\n')
	    if land1=='ch' or land1=='at':
		doelbestand.write(u'  <name>'+adres+u' '+u'</name>\n')
	    else:
		doelbestand.write('  <name>'+adres+' '+'</name>\n')
	except UnicodeDecodeError:
	    print adres
	doelbestand.write(u'</wpt>\n')
    doelbestand.write(u'</gpx>\n')
    return

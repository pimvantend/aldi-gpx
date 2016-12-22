#!/usr/bin/env python
import re,mechanize,time,cPickle

def verwerkpostcodech(postcode,land1):
    if land1=='ch':
	mapaanvraag='https://www.aldi-suisse.ch/filialen/de-ch/Search?SingleSlotGeo='+postcode
	gewenst='ALDI'
	nietgewenst='Hofer'
    elif land1=='at':
	mapaanvraag='https://www.hofer.at/filialen/de-at/Search?SingleSlotGeo='+postcode
	gewenst='Hofer'
	nietgewenst='ALDI'
    time.sleep(3)
    print mapaanvraag
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders =  [('User-agent', 'Firefox')]
    bestand=br.open(mapaanvraag)
#bestand=open('Search?SingleSlotGeo=9430','r')
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
    if land=='F':
	land1='fr'
    elif land=='B':
	land1='be'
    elif land=='D':
	land1='de'+args[0]
    else:
	land1=land.lower()
    doelbestand='aldi-'+land1+'.gpx'
    doelbestand=open(doelbestand,'w')
    doelbestand.write( '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
    doelbestand.write( '<gpx version="1.1" creator="Locus Android"\n')
    doelbestand.write( ' xmlns="http://www.topografix.com/GPX/1/1"\n')
    doelbestand.write( ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    doelbestand.write( ' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"\n')
    doelbestand.write( ' xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"\n')
    doelbestand.write( ' xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"\n')
    doelbestand.write( ' xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"\n')
    doelbestand.write( ' xmlns:locus="http://www.locusmap.eu">\n')
    for regel in regellijst:
	[lon,lat,adres]=regel.split(' ',2)
	doelbestand.write('<wpt lat="'+lat+'" lon="'+lon+'">\n')
	if land1=='ch' or land1=='si' or land1=='at':
	    doelbestand.write('  <name>'+adres+' '+'</name>\n')
	else:
	    doelbestand.write('  <name>'+'aldi '+adres+' '+'</name>\n')
	doelbestand.write('</wpt>\n')
    doelbestand.write('</gpx>\n')
    return

land1='at'
postcodelijst=range(3330,9999,10)
postcodelijst=[str(ding) for ding in postcodelijst]
if False:
    regellijst1=[]
else:
    picklebestand=open('hoferat.pickle','r')
    regellijst1=cPickle.load(picklebestand)
    picklebestand.close()
for postcode1 in postcodelijst:
    regellijst1+=verwerkpostcodech(postcode1,land1)
    regelset1=set(regellijst1)
    regellijst1=list(regelset1)
    picklebestand=open('hoferat.pickle','w')
    cPickle.dump(regellijst1,picklebestand)
    picklebestand.close()
    print len(regellijst1)
maakgpx(regellijst1,land1)

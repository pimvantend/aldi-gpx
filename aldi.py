#!/usr/bin/python
import mechanize,re,math
import matplotlib.pyplot as plt

def adresmaken(response):
    reguliere=re.compile(r'<address>(.*?)<br/>')
    straatlijst=reguliere.findall(response)
    reguliere=re.compile(r'<br/>(.*?)\r')
    plaatslijst=reguliere.findall(response)
#plaatslijst=[ding for ding in plaatslijst if '<strong>' not in ding]
    plaatslijst=[ding for ding in plaatslijst if '<strong>' not in ding and '<b>' not in ding]
    plaatslijst=[ding for ding in plaatslijst if '</p></div>' not in ding ]
    reguliere=re.compile(r'>(.*?) km</span')
    afstandenlijst=reguliere.findall(response)
    afstandenlijst=[ding.replace(',','.') for ding in afstandenlijst]
    return straatlijst,plaatslijst,afstandenlijst

def coordinatenlijstmaken(br9):
    coordinatenlijst=[]
    for link in br9.links():
	if link.text=='Lageplan':
	    lon,lat=lonlat(link)
	    coordinatenlijst.append((lon,lat))
    return coordinatenlijst

def lonlat(link1):
    aardstraal=6371000.0
#	print link.url
    br2 = mechanize.Browser()
#br2.set_all_readonly(False)    # allow everything to be written to
    br2.set_handle_robots(False)   # ignore robots
    br2.set_handle_refresh(False)  # can sometimes hang without this
    br2.addheaders =  [('User-agent', 'Firefox')]
#print yellowmapaanvraag
    response2=br2.open(link1.url)
    kaarttekst=response2.read()      # the text of the page
    reguliere=re.compile(r'mx:(.*?),')
    mxlijst=reguliere.findall(kaarttekst)
    mxlijst=map(int,mxlijst)
#	print mxlijst[1]
    reguliere=re.compile(r'my:(.*?),')
    mylijst=reguliere.findall(kaarttekst)
    mylijst=map(int,mylijst)
#	print mylijst[1]
    lon1=(float(mxlijst[1])/aardstraal)*(180.0/math.pi)
    lat1=2.0*math.atan(math.exp(float(mylijst[1])/aardstraal))-math.pi*0.5
    lat1=lat1*180.0/math.pi
    return lon1,lat1

def maakregellijst(br9,response9):
    adreslijst9=[]
    coordinatenlijst1=coordinatenlijstmaken(br9)
    straatlijst1,plaatslijst1,afstandenlijst1=adresmaken(response9)
#    print len(coordinatenlijst1),len(straatlijst1),len(plaatslijst1),len(afstandenlijst1)
#    print plaatslijst1
    for ((lon,lat),straat,plaats,afstand) in zip(coordinatenlijst1,straatlijst1,plaatslijst1,afstandenlijst1):
	adreslijst9.append(str(lon)+' '+str(lat)+' '+afstand+' '+straat+' '+plaats)
    return adreslijst9

def bepaallaatstepagina(br9):
    laatstepagina0=1
    for link in br9.links():
	if link.text=='>>':
#	print link.url
	    reguliere=re.compile(r'Page=(.*?)&')
	    laatstepaginalijst=reguliere.findall(link.url)
	    laatstepagina0=int(laatstepaginalijst[0])
    return laatstepagina0

def bepaalvolgendelink(br9):
    for link in br9.links():
	if link.text=='>':
	    reguliere=re.compile(r'Page=(.*?)&')
	    volgendepaginalijst=reguliere.findall(link.url)
	    volgendepagina=int(volgendepaginalijst[0])
	    volgendelink=link.url
    return volgendelink

def zoekzipcode(land,zipcode1,totnutoe):
    radius=50000
    radius=str(radius)
    adreslijst=[]
    stad=''
    yellowmapaanvraag='http://www.yellowmap.de/Partners/AldiNord/Search.aspx?Radius='+radius+'&BC=ALDI|ALDN&Search=1&Country='+land+'&Zip='+zipcode1+'&Town='+stad
    br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders =  [('User-agent', 'Firefox')]
    response1=br.open(yellowmapaanvraag)
    response1=response1.read()
    if land=='D':
	reguliere=re.compile(r'\|D\|(.*?)\|\|\|\|\|')
#    reguliere=re.compile(zipcode1+r'\|(.*?)\|\|\|\|\|\|')
	plaatsenlijst=reguliere.findall(response1)
#	print plaatsenlijst
	if len(plaatsenlijst)>0:
	    plaatsenlijstgesplitst=plaatsenlijst[0].split('|')
	    stad=plaatsenlijstgesplitst[-1]
	    zipcode2=plaatsenlijstgesplitst[0]
	    print zipcode2,stad
	    yellowmapaanvraag='http://www.yellowmap.de/Partners/AldiNord/Search.aspx?Radius='+radius+'&BC=ALDI|ALDN&Search=1&Country='+land+'&Zip='+zipcode2+'&Town='+stad
	    response1=br.open(yellowmapaanvraag)
	    response1=response1.read()
    else:
	reguliere=re.compile(zipcode1+r'\|(.*?)\|\|\|\|\|\|')
	plaatsenlijst=reguliere.findall(response1)
	zipcode2=zipcode1
	if len(plaatsenlijst)>0:
	    stad=plaatsenlijst[0]
	    print zipcode2,stad
	    yellowmapaanvraag='http://www.yellowmap.de/Partners/AldiNord/Search.aspx?Radius='+radius+'&BC=ALDI|ALDN&Search=1&Country='+land+'&Zip='+zipcode2+'&Town='+stad
	    response1=br.open(yellowmapaanvraag)
	    response1=response1.read()
    laatstepagina=bepaallaatstepagina(br)
    adreslijst+=maakregellijst(br,response1)
    paginaverwerkt=1
    print paginaverwerkt,laatstepagina
    while paginaverwerkt<laatstepagina:
	volgendelink=bepaalvolgendelink(br)
	response2=br.open(volgendelink)
	response2=response2.read()
	adreslijst+=maakregellijst(br,response2)
	paginaverwerkt+=1
	print paginaverwerkt,laatstepagina
    afstandenlijst=[]
    lonlijst=[]
    latlijst=[]
    adreslijst1=[]
    for adres in adreslijst:
#    print adres
	adresgesplitst=adres.split(' ',3)
	print adresgesplitst
	lonlijst.append(adresgesplitst[0])
	latlijst.append(adresgesplitst[1])
	afstandenlijst.append(float(adresgesplitst[2]))
	adreslijst1.append(adresgesplitst[3])
    print len(adreslijst)
    print afstandenlijst
#    kwadraatafstandenlijst=[ding*ding for ding in afstandenlijst]
#    plt.plot(kwadraatafstandenlijst,'ro')
#    plt.show()
#    plt.plot(lonlijst,latlijst,'ro')
#    plt.plot(lonlijst,latlijst,'g-')
#    plt.show()
    regellijst=[]
    for (lon,lat,adres) in zip(lonlijst,latlijst,adreslijst1):
	regel=lon+' '+lat+' '+adres
	regellijst.append(regel)
    regellijst=totnutoe+regellijst
    regelset=set(regellijst)
    regellijst=list(regelset)
    lonlijstfloat=map(float,lonlijst)
    latlijstfloat=map(float,latlijst)
    if len(lonlijstfloat)>0:
	lonmax=max(lonlijstfloat)
        latmax=max(latlijstfloat)
	lonmin=min(lonlijstfloat)
	latmin=min(latlijstfloat)
	vierkantx=[lonmin,lonmax,lonmax,lonmin,lonmin]
	vierkanty=[latmax,latmax,latmin,latmin,latmax]
	plt.plot(vierkantx,vierkanty,'b-')
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
	doelbestand.write('  <name>'+'aldi '+adres+' '+'</name>\n')
	doelbestand.write('</wpt>\n')
    doelbestand.write('</gpx>\n')
    return

land1='D'
voorvoegsel='3'
# 622 filialen in postcodegebied 4
#voorvoegsel='0'
# 296 filialen in postcodegebied 0
#zipcodelijst=range(1000,9999,50)
zipcodelijst=range(0,9999,100)
regellijst1=[]
for zipcode in zipcodelijst:
    zipcode=str(zipcode)
    while len(zipcode)<4:
	zipcode='0'+zipcode
    zipcode=voorvoegsel+zipcode
    print zipcode
    regellijst1=zoekzipcode(land1,zipcode,regellijst1)
# verwijder viercijferige postcodes:
    reguliere=re.compile(r' '+voorvoegsel+r'[0-9][0-9][0-9][0-9] ')
    regellijst1=[ding for ding in regellijst1 if len(reguliere.findall(ding))>0]
    print len(regellijst1)
plt.show()
maakgpx(regellijst1,land1,voorvoegsel)
exit()

land1='F'
zipcodelijst=['0'+str(getal)+'120' for getal in range(1,10)]
zipcodelijst+=[str(getal)+'120' for getal in range(10,96)]
zipcodelijst+=['59140']
zipcodelijst+=['02200']
zipcodelijst+=['51100']
zipcodelijst+=['16500','22950','24110','25480','25660','29770','31150','34000','35260','35400','37540','37000','44110','49600','50400','52100','54700','54200','54410']
zipcodelijst+=['56700','57100','57160','57200','57290','57310','57350']
zipcodelijst+=['57510','57600','57620','57740','57800','57950']
zipcodelijst+=['01420','60200','62000','62450','66200','66000']
zipcodelijst+=['67150','68180','69380','69170','70000','72140']
zipcodelijst+=['77100','77130','79300','83190','84100','87300']
zipcodelijst+=['88400','88200','89100','95260']
print zipcodelijst
regellijst1=[]
for zipcode in zipcodelijst:
    zipcode=str(zipcode)
    regellijst1=zoekzipcode(land1,zipcode,regellijst1)
print regellijst1
plt.show()
maakgpx(regellijst1,land1)
exit()

land1='DK'
# 222 filialen
zipcodelijst=range(1000,9999,50)
regellijst1=[]
for zipcode in zipcodelijst:
    zipcode=str(zipcode)
    regellijst1=zoekzipcode(land1,zipcode,regellijst1)
    reguliere=re.compile(r' [0-9][0-9][0-9][0-9] ')
    regellijst1=[ding for ding in regellijst1 if len(reguliere.findall(ding))>0]
    print len(regellijst1)
plt.show()
maakgpx(regellijst1,land1)
exit()

land1='NL'
zipcodelijst=[
4338, #middelburg
3449, #woerden
1827, #alkmaar
6871, #renkum
1211, #hilversum
2957, #lekkerkerk
4691, #tholen
4815, #breda
5571, #bergeijk
6131, #sittard
6462, #kerkrade
5935, #tegelen
7009, #doetinchem
7451, #holten
8263, #kampen
7991, #dwingeloo
9645, #veendam
9861, #grootegast
8531] #lemmer
regellijst1=[]
for zipcode in zipcodelijst:
    zipcode=str(zipcode)
    regellijst1=zoekzipcode(land1,zipcode,regellijst1)
# kies nederlandse postcodes met spatie:
    reguliere=re.compile(r' [1-9][0-9][0-9][0-9] [A-Z][A-Z] ')
    regellijst2=[ding for ding in regellijst1 if len(reguliere.findall(ding))>0]
# kies nederlandse postcodes zonder spatie:
    reguliere=re.compile(r' [1-9][0-9][0-9][0-9][A-Z][A-Z] ')
    regellijst2+=[ding for ding in regellijst1 if len(reguliere.findall(ding))>0]
    regellijst1=regellijst2
    print len(regellijst1)
plt.show()
maakgpx(regellijst1,land1)
exit()

land1='B' # en luxemburg
# 456 filialen
zipcodelijst=range(1000,9999,50)
regellijst1=[]
for zipcode in zipcodelijst:
    zipcode=str(zipcode)
    regellijst1=zoekzipcode(land1,zipcode,regellijst1)
# verwijder duitse en franse postcodes:
    reguliere=re.compile(r' [0-9][0-9][0-9][0-9][0-9] ')
    regellijst1=[ding for ding in regellijst1 if len(reguliere.findall(ding))==0]
# verwijder nederlandse postcodes met spatie:
    reguliere=re.compile(r' [1-9][0-9][0-9][0-9] [A-Z][A-Z] ')
    regellijst1=[ding for ding in regellijst1 if len(reguliere.findall(ding))==0]
# verwijder nederlandse postcodes zonder spatie:
    reguliere=re.compile(r' [1-9][0-9][0-9][0-9][A-Z][A-Z] ')
    regellijst1=[ding for ding in regellijst1 if len(reguliere.findall(ding))==0]
    print len(regellijst1)
plt.show()
maakgpx(regellijst1,land1)
exit()

land1='CH'
#  filialen
zipcodelijst=range(1000,9999,50)
regellijst1=[]
for zipcode in zipcodelijst:
    zipcode=str(zipcode)
    regellijst1=zoekzipcode(land1,zipcode,regellijst1)
    reguliere=re.compile(r' [0-9][0-9][0-9][0-9] ')
    regellijst1=[ding for ding in regellijst1 if len(reguliere.findall(ding))>0]
    print len(regellijst1)
plt.show()
maakgpx(regellijst1,land1)
exit()


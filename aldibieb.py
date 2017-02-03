import mechanize,re,math
#import matplotlib.pyplot as plt

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
#	plt.plot(vierkantx,vierkanty,'b-')
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

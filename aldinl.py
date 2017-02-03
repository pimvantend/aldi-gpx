#!/usr/bin/python
import mechanize,re,math
import matplotlib.pyplot as plt
from aldibieb import zoekzipcode
from aldibieb import maakgpx


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
#plt.show()
maakgpx(regellijst1,land1)
exit()

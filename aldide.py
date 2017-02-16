#!/usr/bin/python
from aldibieb import zoekzipcode
from aldibieb import maakgpx
import re

land1='D'
voorvoegsel=raw_input('plz-zone [0-9]:')
#voorvoegsel='9'
# 621 filialen in postcodegebied 4
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
#plt.show()
maakgpx(regellijst1,land1,voorvoegsel)
exit()

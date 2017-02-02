#!/usr/bin/python
import mechanize,re,math
import matplotlib.pyplot as plt
from aldibieb import zoekzipcode
from aldibieb import maakgpx


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

#!/usr/bin/python
from aldibieb import zoekzipcode
from aldibieb import maakgpx

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
#plt.show()
maakgpx(regellijst1,land1)
exit()

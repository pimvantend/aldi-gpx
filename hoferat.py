#!/usr/bin/env python
import hoferbieb
import cPickle,glob
land1='at'
picklebestandsnaam='hoferat.pickle'
if len(glob.glob(picklebestandsnaam))==0:
    regellijst1=[]
    postcodelijst=range(1000,9999,10)
    postcodelijst=[str(ding) for ding in postcodelijst]
else:
    picklebestand=open(picklebestandsnaam,'r')
    (postcodelijst,regellijst1)=cPickle.load(picklebestand)
    picklebestand.close()
while len(postcodelijst)>0:
    postcode1=postcodelijst.pop(0)
    regellijst1+=hoferbieb.verwerkpostcodech(postcode1,land1)
    regelset1=set(regellijst1)
    regellijst1=list(regelset1)
    picklebestand=open(picklebestandsnaam,'w')
    cPickle.dump(([postcode1]+postcodelijst,regellijst1),picklebestand)
    picklebestand.close()
    print len(regellijst1)
hoferbieb.maakgpx(regellijst1,land1)

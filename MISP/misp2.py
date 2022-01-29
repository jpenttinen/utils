#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from email import header
from tkinter import EventType
import pandas as pd
import csv
from pymisp import ExpandedPyMISP
import urllib3
from keys import misp_url, misp_key, misp_verifycert
from io import StringIO
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

 
pymisp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert, debug=True)


# print(type(response = pymisp.search(eventinfo='%Lazarus%', limit=1, EventType='url')))
#response = pymisp.search(return_format='csv',limit=10, threat_level_id=2, category='Network activity')
#df=pd.read_csv(pymisp.search(return_format='csv',limit=10, category='Network activity'))
response=StringIO(pymisp.search(return_format='csv', limit=100, category='Network activity'))
print(response.text)
df=pd.read_json(StringIO(pymisp.search(limit=100, category='Network activity', EventType='url')))
for col in df.columns:
    print(col)

# drop unneeded columns
drop_list = ['uuid', 'event_id', 'comment', 'to_ids', 'object_relation','object_uuid','object_name', 'object_meta_category', 'attribute_tag']
df=df.drop(drop_list, axis=1)
# filter out all other types than url
df=df[df.type=='url']
# reorder columns
df=df[['value','type','category','date']]
# remove, index, header and quoting
df.to_csv('out2.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", header=None,index=None,escapechar='')

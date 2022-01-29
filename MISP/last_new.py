#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import ExpandedPyMISP
from keys import misp_url, misp_key, misp_verifycert, misp_client_cert
import argparse
import os
import pandas as pd
import numpy as np
import csv
import urllib3
from io import StringIO
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Usage for pipe masters: ./last.py -l 5h | jq .
# Usage in case of large data set and pivoting page by page: python3 last.py  -l 48h  -m 10 -p 2  | jq .[].Event.info
def make_logpoint_csv(df):
    # Filter only IP address information to DataFrame
    ip_df=df[(df['type']=='ip-src') | (df['type']=='ip-dst')]
    ip_df.rename(columns={"value":"ip"}, inplace = True)
    print(ip_df.head(5))

    # Filter only hash value information to DataFrame
    hash_df=df[(df['type']=='md5') | (df['type']=='sha1') | (df['type']=='sha256')]
    hash_df.rename(columns={"value":"file_hash"}, inplace = True)
    print(hash_df.head(5))
    
    # Filter only domain value information to DataFrame
    domain_df=df[(df['type']=='domain')]
    domain_df.rename(columns={"value":"domain"}, inplace = True)
    print(domain_df.head(5))
    
    # Filter only domain value information to DataFrame
    hostname_df=df[(df['type']=='hostname')]
    hostname_df.rename(columns={"value":"domain"}, inplace = True)
    print(hostname_df.head(5))
    
    # Filter only URL value information to DataFrame
    url_df=df[(df['type']=='url')]
    url_df.rename(columns={"value":"url"}, inplace = True)
    print(url_df.head(5))
    

    df.insert(1,"domain", np.nan)
    df.insert(1,"score", np.nan)
    df.insert(1,"first_seen", np.nan)
    df.insert(1,"last_seen", np.nan)
    df.insert(1,"ip", np.nan)
    df.insert(1,"url", np.nan)
    #df.insert(1,"type", np.nan)
    df.insert(1,"file_hash", np.nan)
    #df = df.reset_index()  # make sure indexes pair with number of rows
    """     for index, row in df.iterrows():
        if row['type']=='ip-src':
            print('teppo\n')
            row['ip']=row['value'] 
    """
    print(ip_df.head(5))
    ip_df.to_csv('logpoint_misp_ip.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", index=None,escapechar=' ')
    hash_df.to_csv('logpoint_misp_hash.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", index=None,escapechar=' ')
    domain_df.to_csv('logpoint_misp_domain.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", index=None,escapechar=' ')
    hostname_df.to_csv('logpoint_misp_hostname.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", index=None,escapechar=' ')
    url_df.to_csv('logpoint_misp_url.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", index=None,escapechar=' ')
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download latest events from a MISP instance.')
    parser.add_argument("-l", "--last", required=True, help="can be defined in days, hours, minutes (for example 5d or 12h or 30m).")
    parser.add_argument("-m", "--limit", required=False, default="10", help="Add the limit of records to get (by default, the limit is set to 10)")
    parser.add_argument("-p", "--page", required=False, default="1", help="Add the page to request to paginate over large dataset (by default page is set to 1)")
    parser.add_argument("-o", "--output", help="Output file")

    args = parser.parse_args()

    if args.output is not None and os.path.exists(args.output):
        print('Output file already exists, aborted.')
        exit(0)

    if misp_client_cert == '':
        misp_client_cert = None
    else:
        misp_client_cert = (misp_client_cert)

    proxies={'http': None, 'https': None}

    misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert, cert=misp_client_cert, proxies=proxies)
    result = StringIO(misp.search(publish_timestamp=args.last, limit=args.limit, page=args.page, return_format='csv'))



    if not result:
        print('No results for that time period')
        exit(0)

    #print(len(result))
    #result = pd.json_normalize(result)
    #print(type(result))
    df=pd.read_csv(result)
    #print(df.columns)
    
    # for col in df.columns:
    #    print(col)
    
    #print(df.head(10))
    #print(df.loc[df['category'].isin(['Network activity','Payload delivery', 'Payload installation'])])
    #df.to_csv('output2.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", header=None,index=None,escapechar='')
    
    # filter out all other category types than 'Network activity'
    # df=df[df.category=='Network activity']
    # Drop unneeded columns
    drop_list = ['uuid', 'comment', 'to_ids', 'object_relation','object_uuid','object_name', 'object_meta_category', 'attribute_tag']
    df=df.drop(drop_list, axis=1)
    #print(df)

    for col in df.columns:
        print(col)
    
    make_logpoint_csv(df)
    
    #print(df)

    #df.to_csv('output2.csv',sep=",", quoting=csv.QUOTE_NONE, quotechar="", index=None,escapechar=' ')
"""     if args.output:
        with open(args.output, 'w') as f:
            for r in result:
                f.write(r.to_json() + '\n')
    else:
        for r in result:
            print(r.to_json())
 """
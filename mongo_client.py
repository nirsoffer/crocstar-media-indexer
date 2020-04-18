#!/usr/local/bin/python3
from pymongo import MongoClient
import subprocess
import sys, getopt
import json

DB_HOST='localhost'
DB_PORT=27017
DB_USERNAME="test"
DB_PASSWORD="123"
DB_AUTHSOURCE="db"

# testfile="/Volumes/Dropbox/Juval UG Dropbox/Nir S/Stand up Sets/Cosmics/2018/S3930005.MP4"
mc=MongoClient(DB_HOST,DB_PORT,username=DB_USERNAME,password=DB_PASSWORD, authSource=DB_AUTHSOURCE);

def exif_parse(filename):
    # output=subprocess.Popen(['exiftool',filename],stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    output=subprocess.check_output(['exiftool',"-j", filename], stderr=subprocess.STDOUT,universal_newlines=True)

    print(filename);
    # stdout, stderr=output.communicate()
    dict=json.loads(output)

    # for i in iter(output.splitlines()):
    #     line=i.split(':');
    #     field=line[0].rstrip().lstrip();
    #     val=line[1].rstrip().lstrip();
    #     dict[field]=val
    print(dict)
    return dict

def md5sum(filename):
    output=subprocess.check_output(['md5sum','-q',filename],stderr=subprocess.STDOUT,universal_newlines=True)
    return output.rstrip().lstrip()

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "");
    if len(args) == 0:
        print("no filename");
        exit(1);
    filename=args[0];
    print(opts,args);
    dict=exif_parse(filename)
    md5=md5sum(filename);
    db=mc['database_nir'];
    coll=db['videos']
    # print(md5sum(filename));
    coll.replace_one({"_id" : filename},
                    { "exiftool": dict,
                      "md5sum" : md5

                    } ,upsert=True);
# print(coll)
# print(mc.list_databases())

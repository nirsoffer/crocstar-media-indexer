#!/usr/local/bin/python3
from pymongo import MongoClient
import subprocess
import sys, getopt
import json
import os
import tempfile

DB_HOST='localhost'
DB_PORT=27017
DB_USERNAME="test"
DB_PASSWORD="123"
DB_AUTHSOURCE="db"

extensions=["mp4", "mov", "avi", "mpeg"]

# testfile="/Volumes/Dropbox/Juval UG Dropbox/Nir S/Stand up Sets/Cosmics/2018/S3930005.MP4"
mc=MongoClient(DB_HOST,DB_PORT,username=DB_USERNAME,password=DB_PASSWORD, authSource=DB_AUTHSOURCE);

def exif_parse(filename):
    # output=subprocess.Popen(['exiftool',filename],stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    try:
        output=subprocess.check_output(['exiftool',"-j", filename], stderr=subprocess.STDOUT,universal_newlines=True)

    except:
        print("Exiftool exception!")
        exit(1)
    dict=json.loads(output)
    return dict

def md5sum(filename):
    try:
        output=subprocess.check_output(['md5sum','-q',filename],stderr=subprocess.STDOUT,universal_newlines=True)
        return output.rstrip().lstrip()
    except:
        return None

def autosub(filename):
    print("autosubbing")
    concur="8"
    (hand,tmpfile) = tempfile.mkstemp()
    # try:
    suboutput=subprocess.check_output(['autosub',"-C", concur, "-F","json","-o", tmpfile, filename],
                universal_newlines=True)
    print(tmpfile,hand)
    with os.fdopen(hand,"r") as f:
        # print(f.readlines())
        for line in f:
            print(line)
            print("x")
            output=json.loads(line)
    
    # except:
    #     print("autosub exception!")
    #     exit(1)
    # print("autosubbing completed")
    print(output)
    dict=output
    print(dict)
    return dict

    
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "");
    if len(args) == 0:
        print("no directory")
        exit(1)
    directory=args[0];
    for root, dirs, files in os.walk(directory, topdown=False):
        # for name in files:
        #     print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))
        
        for filename in files:
            ext=filename.split('.')[-1].lower()
            if not ext in extensions:
                print(f'skipping extenstion {ext}')
                continue
            filename=directory+filename
            dict=exif_parse(filename)
            md5= md5sum(filename)
            autos=autosub(filename)
            db=mc['database_nir']
            coll=db['videos']
            # print(md5sum(filename));
            coll.replace_one({"_id" : filename},
                    { "exiftool": dict,
                      "md5sum" : md5,
                      "transcription" : autos

                    } ,upsert=True);
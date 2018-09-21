try:
    import json
    import sys
    import requests
    import zipfile
    import base64
    import os
except ImportError:
    print("Could not import libraries")
    print("Make sure your install isn't broken, and you've installed Requests.")
    exit()

def download(url:str, name:str=""):
    if name=="": #auto-name
        name = url.split('/')[len(url.split('/'))-1]
        print(name)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(name, 'wb') as handle:
        for block in r.iter_content(1024):
            handle.write(block)
    return name

version = 1
print('== AdvRVD v'+str(version)+": Advanced Roblox Version Downloader ==")
print('ScottBeebiWan 2018')
print()

try:
    jsf = open(sys.argv[1], 'r')
except Exception as e:
    print("Could not open input file:")
    print(e)
    exit()
jss = jsf.readlines(); jss = "\r".join(jss)
jsf.close()
try:
    jso = json.loads(jss)
except Exception as e:
    print("Could not convert input file to dict:")
    print(e)
    exit()
if not jso['rvdp-version']==version:
    print('Version mismatch')
    print('File designed for v'+str(jso['rvdp-version']))
print('Downloading files...')
for i in jso['dl-table']:
    _from = i
    _to = jso['dl-table'][i]
    ver = jso['version']
    webroot = jso['webroot']
    try:
        uz = download(webroot+ver+'-'+_from)
    except Exception as e:
        print('Couldn\'t download:')
        print(e)
        print('Skipping.')
        continue
    if uz.split('.')[len(uz.split('.'))-1]=="zip":
        zip_ref = zipfile.ZipFile(uz, 'r')
        zip_ref.extractall(ver+_to)
        zip_ref.close()
        os.remove(uz)
    else:
        try:
            os.rename(uz, ver+_to+uz[len(ver)+1:])
        except Exception as e:
            print('Couldn\'t move:')
            print(e)
            os.remove(uz)
print()
print('Processing undownloadable files...')
for i in jso['undownloadable']:
    info = jso['undownloadable'][i]
    print(info[0]+i)
    handle = open(ver+info[0]+i, 'wb')
    handle.write(base64.b64decode(info[1]))
    handle.close()

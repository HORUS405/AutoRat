from requests import get 
from bs4 import BeautifulSoup
from sys import argv
import re
import os 
import subprocess
from termcolor import colored

print(colored('''
           ,ggg,                                ,ggggggggggg,                       
          dP""8I                 I8            dP"""88""""""Y8,                I8   
         dP   88                 I8            Yb,  88      `8b                I8   
        dP    88              88888888          `"  88      ,8P             88888888
       ,8'    88                 I8                 88aaaad8P"                 I8   
       d88888888   gg      gg    I8      ,ggggg,    88""""Yb,      ,gggg,gg    I8   
 __   ,8"     88   I8      8I    I8     dP"  "Y8ggg 88     "8b    dP"  "Y8I    I8   
dP"  ,8P      Y8   I8,    ,8I   ,I8,   i8'    ,8I   88      `8i  i8'    ,8I   ,I8,  
Yb,_,dP       `8b,,d8b,  ,d8b, ,d88b, ,d8,   ,d8'   88       Yb,,d8,   ,d8b, ,d88b, 
 "Y8P"         `Y88P'"Y88P"`Y888P""Y88P"Y8888P"     88        Y8P"Y8888P"`Y888P""Y88
                                    Author: Horus-405
                                                                                    
''','red'))
if len(argv) < 2: 
    print(f"Usage: {argv[0]} <Site>\n\rExample: {argv[0]} sony.com")

org = argv[1].strip()
dir = org.split('.')[0]
os.mkdir(dir)


def asn_cidr_enum():
    site = org.split('.')[0]
    url = f'https://bgp.he.net/search?search%5Bsearch%5D={dir}&commit=Search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    }
    Cookie={
        'Cookie': '__utma=83743493.1381466975.1632164615.1632164615.1632196205.2; __utmz=83743493.1632164615.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=83743493.2.10.1632196205; __utmc=83743493; __utmt=1; c=BAgiEzE1Ni4xOTQuMjA1Ljgx--f653b1027ca57b446869aba02b9d3d802b708659; _bgp_session=BAh7BjoPc2Vzc2lvbl9pZEkiJWVjNzcxMGQ2MGZlY2U2OGNhM2I4NDU3MjI0YjQ3NjEyBjoGRUY%3D--886fdd0b6210327384328315f7c347e1cac4dcaf'

    }
    req = get(url,headers=headers,cookies=Cookie)
    soup = BeautifulSoup(req.text,features="lxml")
    scraper = soup.find_all('a')[21:]
    res = ''
    for link in scraper:
        res +=link.contents[0]+'\n'
        
    with open(f"{dir}/ASN_CIDR.txt",'w') as f :
        f.write(res)




def waybackurls():
    url = f'https://web.archive.org/cdx/search?url=*.{org}/*&output=text&fl=original&collapse=urlkey'
    request = get(url)
    with open(f"{dir}/Waybackurls.txt",'w') as f : 
       f.write(request.text)

    x = re.findall(".*\.js", request.text)
    result = ''
    for link in x :
        result+=link+'\n'
    with open(f"{dir}/Js_Endpoints.txt","w") as f : 
        f.write(result)


def crt():
    request = get(f"https://crt.sh/?dNSName={org}&output=json").json()
    result = ''
    for link in request:
        result += link['name_value']+'\n'
    with open(f"{dir}/Crt.txt", 'w') as f : 
        f.write(result)




def enumeration():
    subprocess.run(f"subfinder -d {org} -o {dir}/Subfinder_output.txt", shell=True)
    subprocess.run(f"amass enum -d {org} -o {dir}/Amass_output.txt", shell=True)
    subprocess.run(f"cat Amass_output.txt Subfinder_output.txt | httprobe | tee Alive.txt", shell=True)
    subprocess.run(f"cat Alive.txt | aquatone -out Screenshots", shell=True)
    subprocess.run(f"cat Alive.txt | httprobe -p http:81 -p http:3000 -p https:3000 -p http:3001 -p https:3001 -p http:8000 -p http:8080 -p https:8443 -p https:10000 -p http:9000 -p https:9443 -c 50 | tee Unique_Endpoints.txt", shell=True)
    



asn_cidr_enum()
waybackurls()
crt()
enumeration()
print()

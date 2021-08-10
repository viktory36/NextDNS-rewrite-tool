import requests
import subprocess
import json
import socket
from sys import exit

# Configurations for your nextDNS account
nextDNSId = 'change_this'
nCookies = {'sid': 'change_this' }
# Configurations for DNS rewrite options
nextDNSDomain = 'change_this'
nextDNSAnsIp = '{localIp}' #change this and modify createRewriteId() if you want to save a different ip

myWifiName = 'change_this' #The program executes only if you are connected to this particular network. If no such requirement is necessary, you may remove this and the associated checks in main()
nUrlSet = "https://api.nextdns.io/configurations/{nextDNSId}/settings/rewrites"
nUrlDel = "https://api.nextdns.io/configurations/{nextDNSId}/settings/rewrites/{rId}"
nUrlCheck = "https://api.nextdns.io/configurations/{nextDNSId}/setup"
nHeaders = {'Origin': 'https://my.nextdns.io'}

## Returns local ip
## https://stackoverflow.com/a/28950776
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.255.255.25', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

## Checks if nextdns session is valid, and if a nextdns rewrite is already created by this program
def checkRewriteId():
    r = requests.get(nUrlCheck.format(nextDNSId=nextDNSId), cookies=nCookies, headers=nHeaders)
    if r.status_code == 403:
        print("Error: received status code 403. Please check if cookies are valid")
        exit(1)
    rwId = filesHandle()
    return rwId if rwId else False

## If an old rewrite created through this program is found in 'nextDns_rewriteID.txt', delete it from NextDNS to create a new rewrite proper domain and ip,
## Currently there is no update API for already created dns rewrites on NextDNS. When available, utilizing that would be a better procedure than the current check-delete-recreate cycle.
def deleteRewriteId(rwId):
    reqDel = requests.delete(nUrlDel.format(nextDNSId=nextDNSId,rId=rwId), cookies=nCookies, headers=nHeaders)
    return True


## Handles the creation, and re-creation of the dns rewrite on NextDNS
def createRewriteId():
    reqCreate = requests.post(nUrlSet.format(nextDNSId=nextDNSId), cookies=nCookies, json={"name": nextDNSDomain, "answer": nextDNSAnsIp.format(localIp=get_ip())}, headers=nHeaders) # change the answer key if you'd like a different ip rule
    results = reqCreate.json()
    print(results)
    if 'errors' in results.keys():
        print("Error: "+ str(results))
        return False
    rwId = results["id"]
    filesHandle(rwId)
    return True

## Performs file functions to read and write dns rewrite ids on 'nextDns_rewriteID.txt'
def filesHandle(rwId=None):
    with open("nextDns_rewriteID.txt", "a+") as rwIdFile:
        if(rwId):
            # If a rewrite id is passed to this function, update the tracker file with the newly created dns rewrite id
            rwIdFile.seek(0)
            rwIdFile.truncate()
            writeFile = rwIdFile.write(str(rwId))
            return False
        else:
            # If no arguments are passed to this function, read the ID from the file.
            rwIdFile.seek(0)
            readFile = rwIdFile.read().replace('\n', '')
            return readFile


def main():
    ## Only execute this program if we are connected to a particular wi-fi network. You may remove this check if you have no such requirements.
    wifiName = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
    wifiName = wifiName.decode('utf-8')
    if myWifiName in wifiName:
        rwId = checkRewriteId()
        if(rwId):
            deleteRewriteId(rwId)
        createRewriteId()
    else:
        print("Error: not connected to specified network " + myWifiName)
        exit(1)




if __name__ == "__main__":
    main()

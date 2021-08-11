import requests
import subprocess
import socket

# Configurations for your nextDNS account
nextDNSId = 'change_this'
nextDNSCreds = {
    "email": "change_this",
    "password": "change-this"
}
# Configurations for DNS rewrite options
nextDNSDomain = 'change_this'
nextDNSAnsIp = '{localIp}' #change this and modify createRewriteId() if you want to save a different ip

myWifiName = 'change_this' #The program executes only if you are connected to this particular network. If no such requirement is necessary, you may remove this and the associated checks in main()
nUrlSet = "https://api.nextdns.io/configurations/{nextDNSId}/settings/rewrites"
nUrlDel = "https://api.nextdns.io/configurations/{nextDNSId}/settings/rewrites/{rId}"
nUrlLogin = "https://api.nextdns.io/accounts/@login"
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


def checkLogin():
    reqLogin = session.post(nUrlLogin, json=nextDNSCreds, headers=nHeaders)
    if 'errors' in reqLogin.text:
        print("Error: " + reqLogin.text)
        return False
    return True


## Checks if a nextdns rewrite is already created by this program, as tracked by 'nextDns_rewriteID.txt'
def checkRewriteId():
    rwId = filesHandle()
    return rwId if rwId else False

## If an old rewrite created through this program is found in 'nextDns_rewriteID.txt', delete it from NextDNS to create a new rewrite with proper domain and ip.
## Currently there is no update API for already created dns rewrites on NextDNS. When available, utilizing that would be a better procedure than the current check-delete-recreate cycle
def deleteRewriteId(rwId):
    reqDel = session.delete(nUrlDel.format(nextDNSId=nextDNSId,rId=rwId), headers=nHeaders)
    return True

## Handles the creation of the dns rewrite on NextDNS
def createRewriteId():
    reqCreate = session.post(nUrlSet.format(nextDNSId=nextDNSId), json={"name": nextDNSDomain, "answer": nextDNSAnsIp.format(localIp=get_ip())}, headers=nHeaders)
    results = reqCreate.json()
    print(reqCreate.text)
    if 'errors' in reqCreate.text:
        print("Error: " + reqCreate.text)
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
        if(checkLogin()):
            rwId = checkRewriteId()
            if(rwId):
                deleteRewriteId(rwId)
            createRewriteId()
    else:
        print("Not connected to specified network " + myWifiName)


if __name__ == "__main__":
    session = requests.Session() # The persistent session used for all of the requests to NextDNS
    main()

<<<<<<< HEAD

import urllib.request, re, time, os, string, sys
from urllib.request import urlopen
=======
##### pip install lxml
# pip install requests
# http://docs.python-guide.org/en/latest/scenarios/scrape/
#from lxml import html
#import requests
#page = requests.get('http://https://license.aspera.us/evals')
#tree = html.fromstring(page.content)
#print(page)
#print(tree)
#import urllib.request
#page = urllib.request.urlopen('http://hiscore.runescape.com/index_lite.ws?player=zezima')
#print(page.read())
import urllib, re, time, os
>>>>>>> parent of a3e95fc... annnn
homeDir="/Users/andy"

sock = urllib.request.urlopen('https://license.aspera.us/evals')
htmlSource = sock.read()
sock.close()
arrayOfLines = htmlSource.split()
print(len(htmlSource))
for line in arrayOfLines:
    print(line)
n = arrayOfLines.index(b'<strong>Username</strong>') + 2
passWord = arrayOfLines[n].decode("utf-8")
passWord = re.sub('<[^<]+?>', '', passWord)
print(passWord)
n = arrayOfLines.index(b'<strong>Password</strong>') + 2
userName = arrayOfLines[n].decode("utf-8")
userName = re.sub('<[^<]+?>', '', userName)
print(userName)

month = time.strftime("%m")
year = time.strftime("%Y")
if not os.path.exists(homeDir + '/licenses'):
    print("it doesn't exist")
    os.mkdir(homeDir + '/licenses', 0o700)
urllib.request.urlretrieve("https://license.aspera.us/evals/" + year + "/" + month + ".zip", homeDir + "/licenses/licenses.zip")
unzipCommand = 'unzip -o ' + homeDir + '/licenses/licenses.zip -d ' + homeDir + '/licenses'
os.system(unzipCommand)

exit()

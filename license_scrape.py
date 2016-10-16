####### pip install lxml
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
import urllib.request, re, time, os, string, sys
from urllib.request import urlopen
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


#testfile = urllib.URLopener()
#testfile.retrieve("https://license.aspera.us/evals/" + year + "/" + month + ".zip", homeDir + "/licenses/licenses.zip")
unzipCommand = 'unzip -o ' + homeDir + '/licenses/licenses.zip -d ' + homeDir + '/licenses'
os.system(unzipCommand)

exit()

#userCount, passCount = -1, -1
#for line in htmlSource.split():
#    print(line)
#    passCount = passCount - 1
#    userCount = userCount - 1
#    if passCount == 0:
#        passWord = line
#    if userCount == 0:
#        userName = line
#    if line == '<strong>Username</strong>':
#        userCount = 2
#    elif line == '<strong>Password</strong>':
#        passCount = 2
#print('The password is ' + passWord)
#print('The username is ' + userName)

#print htmlSource

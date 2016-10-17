
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
unzipCommand = 'unzip -o ' + homeDir + '/licenses/licenses.zip -d ' + homeDir + '/licenses'
os.system(unzipCommand)

exit()

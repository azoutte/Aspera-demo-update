
import urllib, re, time, os
homeDir = "/Users/andy"
licFiles = homeDir + "/licenses"
downloads = homeDir + "/downloads"

def findDownload(stringMatch, URL):
    sock = urllib.urlopen(URL)
    htmlSource = sock.read()
    sock.close()
    arrayOfLines = htmlSource.split()
    for line in arrayOfLines:
        line =  str(line)
        if re.match(stringMatch, line) is not None:
            line = line[7:len(line)-9]
            break
    return line


sock = urllib.urlopen('https://license.aspera.us/evals')
htmlSource = sock.read()
sock.close()
arrayOfLines = htmlSource.split()
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
if not os.path.exists(licFiles):
    print("it doesn't exist")
    os.mkdir(licFiles, 0o700)
urllib.urlretrieve("https://license.aspera.us/evals/" + year + "/" + month + ".zip", homeDir + "/licenses/licenses.zip")
unzipCommand = 'unzip -o ' + homeDir + '/licenses/licenses.zip -d ' + homeDir + '/licenses'
os.system(unzipCommand)

EntSrvDownload = findDownload('(.+?)/download/sw/entsrv(.+?)-linux-64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/1')
SharesDownload = findDownload('(.+?)/download/sw/shares/(.+?).x86_64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/34')
FaspexDownload = findDownload('(.+?)/download/sw/faspex/(.+?).x86_64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/6')
ConsoleDownload = findDownload('(.+?)/download/sw/console/(.+?).x86_64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/3')

print EntSrvDownload
print SharesDownload
print FaspexDownload
print ConsoleDownload

exit()

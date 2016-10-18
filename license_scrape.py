
import urllib, re, time, os, string
homeDir = "/Users/andy"
licFiles = homeDir + "/licenses"
downloads = homeDir + "/dloads"

if not os.path.exists(downloads):
    print("Downloads doesn't exist.  Creating.")
    os.mkdir(downloads, 0o700)

def find_download(stringMatch, URL):
    sock = urllib.urlopen(URL)
    htmlSource = sock.read()
    sock.close()
    arrayOfLines = htmlSource.split()
    for line in arrayOfLines:
        line =  str(line)
        if re.match(stringMatch, line) is not None:
            line = line[7:len(line)-9]
            break
    fileName = os.path.basename(line)
    print fileName
    if not os.path.exists(downloads + '/' + fileName):
        print("Downloading " + downloads + "/" + fileName + " from " + line)
        line = string.replace(line, 'http://', "http://" + userName + ":" + passWord + "@")
        Stat = urllib.urlretrieve(line, downloads + "/" + fileName)
        print("Status: " + str(Stat))
        print("downloaded complete.")
        # delete old ones
        osCommand = "rpm -K " + downloads + "/" + fileName
        osReturn = os.system(osCommand)
        print("RPM Status: " + str(osReturn))
        if osReturn >= 1:
            print("Downloaded file is corrupt ot incomplete.  Removing it.")
            os.remove(downloads + "/" + fileName)
    else:
        print("file already downloaded")
    return line


sock = urllib.urlopen('https://license.aspera.us/evals')
htmlSource = sock.read()
sock.close()
arrayOfLines = htmlSource.split()
n = arrayOfLines.index(b'<strong>Username</strong>') + 2
userName = arrayOfLines[n].decode("utf-8")
userName = re.sub('<[^<]+?>', '', userName)
print("username=" + userName)
n = arrayOfLines.index(b'<strong>Password</strong>') + 2
passWord = arrayOfLines[n].decode("utf-8")
passWord = re.sub('<[^<]+?>', '', passWord)
print("password=" + passWord)

month = time.strftime("%m")
year = time.strftime("%Y")
if not os.path.exists(licFiles):
    print("License path doesn't exist.  Creating.")
    os.mkdir(licFiles, 0o700)
urllib.urlretrieve("https://license.aspera.us/evals/" + year + "/" + month + ".zip", homeDir + "/licenses/licenses.zip")
unzipCommand = 'unzip -o ' + homeDir + '/licenses/licenses.zip -d ' + homeDir + '/licenses'
os.system(unzipCommand)

EntSrvDownload = find_download('(.+?)/download/sw/entsrv(.+?)-linux-64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/1')
#SharesDownload = find_download('(.+?)/download/sw/shares/(.+?).x86_64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/34')
#FaspexDownload = find_download('(.+?)/download/sw/faspex/(.+?).x86_64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/6')
#ConsoleDownload = find_download('(.+?)/download/sw/console/(.+?).x86_64.rpm(.+?)', 'http://downloads.asperasoft.com/en/downloads/3')

print EntSrvDownload
#print SharesDownload
#print FaspexDownload
#print ConsoleDownload

exit()

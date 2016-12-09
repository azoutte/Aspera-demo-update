
import urllib, re, time, os, string, glob
homeDir = os.path.expanduser("~")
licDir = homeDir + "/asperalicenses"
dloadDir = homeDir + "/asperadownloads"

# Make the downloads directory if it doesn't already exist
if not os.path.exists(dloadDir):
    print("Downloads doesn't exist.  Creating.")
    os.mkdir(dloadDir, 0o700)

# Function to find and download the proper package.
# Inputs are the unique string to find the version and the URL.
def find_download(stringMatch, URL, actionToTake):
#   Load the file
    sock = urllib.urlopen(URL)
    htmlSource = sock.read()
    sock.close()
#   Store that in a list and search for the pattern that was passed to the function.
    arrayOfLines = htmlSource.split()
    for line in arrayOfLines:
        line =  str(line)
        if re.match(stringMatch, line) is not None:
            line = line[7:len(line)-9]
            break
    fileName = os.path.basename(line)
#   If the download file already exists, delete it if the file is incomplete.
#   Download it if it does not esist useing the username and password discovered
#   in the main program.
    if actionToTake == "printcommand":
        line = "  wget --user=" + userName + " --password=" + passWord + " " + line
        print(line)
        return
    line = string.replace(line, "http://", "http://" + userName + ":" + passWord + "@")
    if not os.path.exists(dloadDir + "/" + fileName):
        print("   Downloading " + dloadDir + "/" + fileName + " to " + dloadDir)
        Stat = urllib.urlretrieve(line, dloadDir + "/" + fileName)
#        print("   Status: " + str(Stat))
        # add functionality to delete old packages
        osCommand = "rpm -K " + dloadDir + "/" + fileName + "> /dev/null"
        osReturn = os.system(osCommand)
        print("   Download complete.  RPM validation exit code (0 is good): " + str(osReturn))
        if osReturn >= 1:
            print("  Downloaded file is corrupt or incomplete.  Removing it.")
            os.remove(dloadDir + "/" + fileName)
    else:
        print("   Skipping requested download of " + fileName + ".  It already exists in " + dloadDir)
    return line

# Pull the temporary username/password for downloading packages from the license website
sock = urllib.urlopen("https://license.aspera.us/evals")
htmlSource = sock.read()
sock.close()
arrayOfLines = htmlSource.split()
n = arrayOfLines.index(b"<strong>Username</strong>") + 2
userName = re.sub("<[^<]+?>", "", arrayOfLines[n].decode("utf-8"))
n = arrayOfLines.index(b"<strong>Password</strong>") + 2
passWord = re.sub("<[^<]+?>", "", arrayOfLines[n].decode("utf-8"))
print("username=" + userName + "  password=" + passWord)
print
month = time.strftime("%m")
year = time.strftime("%Y")

# Make a directory for the licenses if one does not already exist.  If it already exists, delete the old contents.
if not os.path.exists(licDir):
    print("License path doesn't exist.  Creating.")
    os.mkdir(licDir, 0o700)
else:
    map(os.remove, glob.glob(homeDir + "/licenses/*eval*license"))

# Download the license file and unzip it.
urllib.urlretrieve("https://license.aspera.us/evals/" + year + "/" + month + ".zip", licDir + "/licenses.zip")
unzipCommand = "unzip -o " + licDir + "/licenses.zip -d " + licDir + "> /dev/null"
os.system(unzipCommand)
print("The current eval licenses have been downloaded to: " + licDir)
print

# Using the specific string for the pacckage, download the latest version
print("Aspera Client - Linux")
EntSrvDownload = find_download("(.+?)/download/sw/client(.+?)-linux-64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/2", "printcommand")
EntSrvDownload = find_download("(.+?)/download/sw/client(.+?)-linux-64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/2", "download")
print("Point to Point - Linux")
EntSrvDownload = find_download("(.+?)/download/sw/p2p(.+?)-linux-64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/7", "printcommand")
print("Enterprise Server - Linux")
EntSrvDownload = find_download("(.+?)/download/sw/entsrv(.+?)-linux-64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/1", "printcommand")
print("Shares - Linux")
SharesDownload = find_download("(.+?)/download/sw/shares/(.+?).x86_64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/34", "printcommand")
print("Faspex - Linux")
FaspexDownload = find_download("(.+?)/download/sw/faspex/(.+?).x86_64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/6", "printcommand")
FaspexDownload = find_download("(.+?)/download/sw/common/1.1(.+?).x86_64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/6", "printcommand")
print("Console - Linux")
ConsoleDownload = find_download("(.+?)/download/sw/console/(.+?).x86_64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/3", "printcommand")
ConsoleDownload = find_download("(.+?)/download/sw/common/1.2(.+?).x86_64.rpm(.+?)", "http://downloads.asperasoft.com/en/downloads/3", "printcommand")

exit()

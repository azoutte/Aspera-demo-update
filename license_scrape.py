#!/usr/bin/python
import urllib, shutil, re, time, os, string, glob

# CUSTOM: Edit these variables for your environement.  Especially the ssh key.
homeDir = os.path.expanduser("~")
licDir = homeDir + "/asperalicenses"
dloadDir = homeDir + "/asperadownloads"
sshKey = homeDir + "/.ssh/id_rsa"

# Make the downloads directory if it doesn't already exist
if not os.path.exists(dloadDir):
    print("Downloads doesn't exist.  Creating.")
    os.mkdir(dloadDir, 0o700)

# Function to find and download the proper package.
# Inputs are the unique string to find the version and the URL.
def download(stringMatch, URL, actionToTake):
# Add some command strings to the passed variables
    stringMatch= "(.+?)/download/sw/" + stringMatch 
    URL =  "http://downloads.asperasoft.com/en/downloads/" + URL
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
    if actionToTake == "print":
        line = "  wget --user=" + userName + " --password=" + passWord + " " + line
        outFile.write(line + "\n")
        return
    line = string.replace(line, "http://", "http://" + userName + ":" + passWord + "@")
    if not os.path.exists(dloadDir + "/" + fileName):
        print("Downloading " + dloadDir + "/" + fileName + " to " + dloadDir)
        Stat = urllib.urlretrieve(line, dloadDir + "/" + fileName)
#        print("Status: " + str(Stat))
        # add functionality to delete old packages
        osCommand = "rpm -K " + dloadDir + "/" + fileName + "> /dev/null"
        osReturn = os.system(osCommand)
        print("Download complete.  RPM validation exit code: " + str(osReturn))
        if osReturn >= 1:
            print("  Downloaded file is corrupt or incomplete.  Removing it.")
            os.remove(dloadDir + "/" + fileName)
    else:
        print("Skipping requested download of " + fileName + ".  It already exists in " + dloadDir)
    return line

# This fuction builds the scp command from the passed parameters and either runs the command or just prints
# is so that the user can run it manually.
def license(license, server, action):
   osCommand = "scp -q -i " + sshKey + " " + licDir + "/" + license + " root@" + server + ":/opt/aspera/etc/aspera-license"
   if action == "push":
      print("Running " + osCommand)
      osReturn = os.system(osCommand)
      print("   Scp complete.  Exit code: " + str(osReturn))
   else:
      print("You can manually run: " + command)


# Pull the temporary username/password for downloading packages from the license website
sock = urllib.urlopen("https://license.aspera.us/evals")
htmlSource = sock.read()
sock.close()
arrayOfLines = htmlSource.split()
n = arrayOfLines.index(b"<strong>Username</strong>") + 2
userName = re.sub("<[^<]+?>", "", arrayOfLines[n].decode("utf-8"))
n = arrayOfLines.index(b"<strong>Password</strong>") + 2
passWord = re.sub("<[^<]+?>", "", arrayOfLines[n].decode("utf-8"))
month = time.strftime("%m")
year = time.strftime("%Y")

# Make a directory for the licenses if one does not already exist.  If it already exists, delete the old contents.
if not os.path.exists(licDir):
    print("License path doesn't exist.  Creating.")
    os.mkdir(licDir, 0o700)
else:
    map(os.remove, glob.glob(licDir + "/*eval*license"))

# Download the license file and unzip it.
urllib.urlretrieve("https://license.aspera.us/evals/" + year + "/" + month + ".zip", licDir + "/licenses.zip")
unzipCommand = "unzip -o " + licDir + "/licenses.zip -d " + licDir + "> /dev/null"
os.system(unzipCommand)
print("The current eval licenses have been downloaded to: " + licDir)
print

# Make copies of the license files  predictable names (EntSrv-unlim is needed to differentiate it from EntSrv-Faspex
for licenseType in ["ConnectSrv", "Faspex-Users", "EntSrv-unlim", "Client", "EntSrv-Faspex", "P2P", "Shares", "Console"]:
   filenames = glob.glob(licDir + "/*" + licenseType + "*license")
   count = 1
   for file in filenames:
      shutil.copy2(file, licDir + "/" + licenseType + str(count))
      count += 1

# Using the specific string for the package, download the latest version.  This section is optional.
# You can add products here and set the last parameter to download and you will have an
# automatic repository of the builds.  You can set the last parameter to print and it will simply
# print the wget commands for you to manually use.
print("Writing the list of wget commands to " + licDir + "/wget_commands")
print
# CUSTOM: Not requires, but you can add or remove from this list as needed.  But
# you will have to visit the website for the exact formating as it is not consistent.
outFile = open(licDir + "/wget_commands", "w")
outFile.write("Aspera Client - Linux \n")
download("client(.+?)-linux-64.rpm", "2", "print")
outFile.write("Point to Point - Linux \n")
download("p2p(.+?)-linux-64.rpm", "7", "print")
outFile.write("Enterprise Server - Linux \n")
download("entsrv(.+?)-linux-64.rpm", "1", "print")
outFile.write("Shares - Linux \n")
download("shares/(.+?).x86_64.rpm", "34", "print")
outFile.write("Faspex - Linux \n")
download("faspex/(.+?).x86_64.rpm", "6", "print")
download("common/1.1(.+?).x86_64.rpm", "6", "print")
outFile.write("Console - Linux \n")
download("console/(.+?).x86_64.rpm", "3", "print")
download("common/1.2(.+?).x86_64.rpm", "3", "print")
outFile.write("Proxy - Linux \n")
download("proxy/(.+?)-linux-64-release.rpm", "42", "print")
outFile.write("Faspstream - Linux \n")
download("faspstream/(.+?)-linux-64.rpm", "60", "print")
outFile.write
outFile.close()

# CUSTOM: Remove this sample line if you don't want to maintain a GA release respository and
# add extra lines if you want to download more GA builds
download("client(.+?)-linux-64.rpm", "2", "download")

# This section prints or pushes out the license files.  If the last parameter of the function to print, then
# the scp line is printed so that it can be run manually.  If the last parameter is push, then the license
# is pushed to the destination.      
print
# CUSTOM: Use this function to scp licenses out to your servers.
license("ConnectSrv1", "miniserver1", "push")
license("ConnectSrv2", "miniserver2", "push")
license("ConnectSrv3", "minifaspex", "push")
exit()

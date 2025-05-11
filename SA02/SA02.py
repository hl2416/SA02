import re
import os

userInfo = []
UN = [""]
userName = ""
app = 0

# opens file Lab02_Users.csv for reading and reads the first line without doing anything to it (ignores it) then reads the second line onwards and place each comma-separated element in a list for use later
f = open("Lab02_Users.csv", "r")
f.readline()
line = f.readline().strip()
li = line.split(',')

while line:
	userInfo.append(li)
	line = f.readline().strip()
	li = line.split(',')

# iterates through the list with user info from the csv file and makes sure that some fields have at least a letter or number while ignoring special chars
# if it does not have whatever is required it prints out a BAD RECORD and does nothing with the current user info
# if the requirements are met it follows the commands used in the example and pulls info from the list when needed
for i in range(0, len(userInfo)):
	userName = ""
	fName = re.sub("[^a-zA-Z]", "", userInfo[i][2])
	lName = re.sub("[^a-zA-Z]", "", userInfo[i][1])
	dep = re.sub("[^a-zA-Z]", "", userInfo[i][5])
	grp = re.sub("[^a-zA-Z]", "", userInfo[i][6])
	empID = re.sub("[^0-9]", "", userInfo[i][0])
	if fName == "" or lName == "" or empID == "" or dep == "" or grp == "":
		print("BAD RECORD: EmployeeID = " + userInfo[i][0])
	else:
		os.system("groupadd -f " + userInfo[i][5])
		userName = (fName[0:1] + lName).lower()
		for j in range(0, len(UN)):
			if UN[j] == (fName[0:1] + lName).lower():
				userName = UN[j] + "1"
				UN.append(userName)
				app = 1
		if app == 1:
			app = 0
		else:
			UN.append(userName)
			app = 0
		if not os.path.exists("/home/" + userInfo[i][5]):
			os.system("mkdir /home/" + userInfo[i][5])
		if userInfo[i][6] == "office":
			os.system("useradd -m -d /home/" + userInfo[i][5] + "/" + userName + " -s /bin/csh -g " + userInfo[i][5] + " -c " + "\"" + userInfo[i][2] + " " + 
			userInfo[i][1] + "\"" + " " + userName)
		else:
			os.system("useradd -m -d /home/" + userInfo[i][5] + "/" + userName + " -s /bin/bash -g " + userInfo[i][5] + " -c " + "\"" + userInfo[i][2] + " " 				+ userInfo[i][1] + "\"" + " " + userName)
		password = "".join(reversed(userName))
		os.system("echo \"" + password + "\" | passwd --stdin " + userName)
		os.system("passwd -e " + userName)

f.close()

#!/usr/bin/python
import os
import re
import sys

def main():
    for line in sys.stdin:
        match = re.match(r'^#', line)

        fields = line.strip().split(':') #strip any whitespace and split into an array

        if match or len(fields) != 5: #This will check if the line begins with # or doesnt have exactly
            continue                  # 5 fields, If it doesnt, it will skip and go to the next iteration
                                      #I would say this code ignores the # because typically # is used for notes/comments for admins. It also skips 5 lines
                                      #to make sure that it is properly structured so there wont be problems later on.
        username = fields[0]
        password = fields[1]

        gecos = "%s %s,,," % (fields[3],fields[2])
        groups = fields[4].split(',') #This will split the last field into a list based on ','
        #to handle several group assignments
        print "==> Creating account for %s..." % (username)
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        #print cmd
        os.system(cmd) #Executes the command in the shell
        print "==> Setting the password for %s..." % (username)
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        #print cmd
        os.system(cmd)

        for group in groups: #This is a for floop tat will iterate through each of the items in groups list checks and skips over the place holders such as '-', its also used to assign the user to several groups
            if group != '-':
                print "==> Assigning %s to the %s group..." % (username, group)
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                #print cmd
                os.system(cmd)
if __name__ == '__main__':
    main()

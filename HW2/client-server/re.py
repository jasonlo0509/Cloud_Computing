import re

pattern = re.compile(r'([a-z]+) ([a-z]+)', re.I)
matchObj = pattern.match('/home/yunchen/Courses/Cloud_Computing/HW2/client-server/client/hello.c')

if matchObj:
    print "matchObj.group() : ", matchObj.group()
    print "matchObj.group(1) : ", matchObj.group(1)
    print "matchObj.group(2) : ", matchObj.group(2)
else:
    print "No match!!"
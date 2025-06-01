print("\033c\033[43;30m\ngive me a file to input? ")
filevarin=""
filevarout=""
var1=[]
var2=[]
start1=0
start2=0
i=0
filesin=input()
print("\033[43;30m\ngive me a file to output? ")
filesout=input()
print("\033[43;30m\ngive me a a number to max value? ")
t=int(input())
f1=open(filesin,"r")
filevarin=f1.read()
f1.close()
var1=filevarin.split("\n")
for n in var1:
    if start1!=0:
        filevarout=filevarout+"\n"
    start1=start1+1
    start2=0
    var2=n.split(",")
    for m in var2:
        m=m.strip()
        i=int(m)
        if start2!=0:
            filevarout=filevarout+","
        start2=start2+1
        filevarout=filevarout+str(float(float(i)/t))
f2=open(filesout,"w")
f2.write(filevarout)
f2.close()
        
from sys import exit
import pandas as pd
import idna
import subprocess

state=""
cmdreserved=""
hoursUntilBidding=""
hoursUntilReveal=""
hoursUntilClose=""
daysUntilExpire=""
status="Status"

filename=input("Enter Input File name :")
outputfile: str=input("Enter Output File Name :")

data =[]
with open(filename) as f:
    data = f.readlines()[1:]

data=[x.strip() for x in data]
if data==[]:
    print ("Input File is Empty!")
    exit()

translated={}
done={}
templst=[]
for x in data:
    try:
        translate =idna.decode(x)
        translate=translate.split(",")[0]
        state=subprocess.getoutput(f"hsd-cli --api-key=81cd9577-0415-4219-9726-cdff1ebb2039 rpc getnameinfo {x}|jq .info.state")
        reserved=subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .start.reserved")
        hoursUntilBidding = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding")
        hoursUntilReveal = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilReveal")
        hoursUntilClose = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilClose")
        daysUntilExpire = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x} |jq .info.stats.daysUntilExpire")
        if x[:4] != "xn--":
            templst.append("NA")
            templst.append(state)
            templst.append(reserved)
            templst.append(hoursUntilBidding)
            templst.append(hoursUntilReveal)
            templst.append(hoursUntilClose)
            templst.append(daysUntilExpire)
            translated[x]=templst
            templst=[]
        else:
            templst.append(translate)
            templst.append(state)
            templst.append(reserved)
            templst.append(hoursUntilBidding)
            templst.append(hoursUntilReveal)
            templst.append(hoursUntilClose)
            templst.append(daysUntilExpire)
            translated[x]=templst
            templst=[]
    except idna.InvalidCodepoint as e:
        elements=e.args
        translate=elements[0].split("\'")[1]
        templst.append(translate)
        state=subprocess.getoutput(f"hsd-cli --api-key=81cd9577-0415-4219-9726-cdff1ebb2039 rpc getnameinfo {x}|jq .info.state")
        reserved=subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .start.reserved")
        hoursUntilBidding = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding")
        hoursUntilReveal = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilReveal")
        hoursUntilClose = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilClose")
        daysUntilExpire = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x} |jq .info.stats.daysUntilExpire")
        templst.append(state)
        templst.append(reserved)
        templst.append(hoursUntilBidding)
        templst.append(hoursUntilReveal)
        templst.append(hoursUntilClose)
        templst.append(daysUntilExpire)
        translated[x]=templst
        templst=[]
    except Exception as e:
        state=subprocess.getoutput(f"hsd-cli --api-key=81cd9577-0415-4219-9726-cdff1ebb2039 rpc getnameinfo {x}|jq .info.state")
        reserved=subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .start.reserved")
        hoursUntilBidding = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilBidding")
        hoursUntilReveal = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .stats.hoursUntilReveal")
        hoursUntilClose = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x}|jq .info.stats.hoursUntilClose")
        daysUntilExpire = subprocess.getoutput(f"hsd-cli rpc getnameinfo {x} |jq .info.stats.daysUntilExpire")
        templst.append("Invalid")
        templst.append(state)
        templst.append(reserved)
        templst.append(hoursUntilBidding)
        templst.append(hoursUntilReveal)
        templst.append(hoursUntilClose)
        templst.append(daysUntilExpire)
        translated[x]=templst
        templst=[]

translated={"name":translated.keys()
            ,"decoded_punycode":[a[0] for a in translated.values()]
            ,"status":[a[1] for a in translated.values()]
            ,"reserved":[a[2] for a in translated.values()]
            ,"hoursUntilBidding":[a[3] for a in translated.values()]
            ,"hoursUntilReveal":[a[4] for a in translated.values()]
            ,"hoursUntilClose":[a[5] for a in translated.values()]
            ,"daysUntilExpire":[a[6] for a in translated.values()]}
nlst=[]

for key, value in translated.items():
    for i in value:
        nlst.append(i)
    done[key]=nlst
    nlst=[]

df =pd.DataFrame(done)
df.to_csv(outputfile,index=None,encoding ="utf-16",sep=",")
print ("Done!")

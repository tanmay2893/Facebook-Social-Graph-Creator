import urllib2,json,time
import ast
t=raw_input('Enter the facebook API token.\nIt should be less than 1 hour old.\nIts necessary that you select version v1.0\n\n')
number=int(raw_input('Enter the number of friends you would like to have in your graph.\nRemember, more you enter the number of people, more will be the time taken.\n:P That was obvious.\n'))
token='access_token='+t
base='https://graph.facebook.com/v1.0/'
param='me?fields=friends.limit('+str(number)+'){picture,name}&'
website=base+param+token
param_my_id='me?fields=id,name,picture&'
my_web=base+param_my_id+token
my_basic=urllib2.urlopen(my_web).read().replace('false','False')
my_basic=ast.literal_eval(my_basic)
my_id=my_basic['id']
my_name=my_basic['name']
my_picture=my_basic['picture']['data']['url']
f = urllib2.urlopen(website)
d=f.read()
d=d.replace('false','False')
d=d.replace('true','True')
d=ast.literal_eval(d)
d=d['friends']['data']
ID=[]
NAME=[]
pictures=[]
ID_dict={}
ID_dict['673791392696057']=0
c=1
node=[]
node=[{"name":my_name,"picture":my_picture}]
time.sleep(20)
for i in d:
    p=i['picture']['data']['url']
    temp={}
    n=i['name']
    temp["name"]=n
    k=i['id']
    temp["picture"]=p
    ID+=[int(k)]
    NAME+=[n]
    pictures+=[p]
    ID_dict[k]=c
    c+=1
    node+=[temp]
k=[]
node_dict={}
node_dict["nodes"]=node
#print node_dict
l=len(ID)
c=1
for i in ID:
    mutual=base+'me/mutualfriends/'+str(i)+'?limit='+str(number)+'&'+token
    print str(c)+'th friend\n' 
    f=urllib2.urlopen(mutual)
    d=f.read()
    d=ast.literal_eval(d)
    d=d['data']
    c+=1
    #print d
    if len(d)>0 and int(d[0]['id'])>ID[-1]:
        d=[]
    #print d
    #print '********'
    k+=[d]
final=[]
for i in k:
    e=[]
    for j in i:
        t=j['id']
        try:
            l=ID_dict[t]
            #print l
            e+=[l]
        except:
            #print '##########'
            break
    final+=[e]
l=len(final)
#print final
links=[]
l=(l//2)+1
for j in range(l):
    for k in final[j]:
        if k==[]:
            continue
        else:
            temp={}
            temp['source']=j+1
            temp['target']=k
            links+=[temp]
for i in range(1,number+1):
    temp={}
    temp['source']=0
    temp['target']=i
    links+=[temp]
node_dict['links']=links
node_dict=json.dumps(node_dict)
print 'Creating required facebook.html file\n'
with open('facebook.html','r') as file:
    data=file.readlines()
data[45]='json='+str(node_dict)+';\n'
with open('facebook.html','w') as file:
    file.writelines(data)

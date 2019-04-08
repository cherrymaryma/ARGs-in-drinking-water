import os
import time, sys
from Bio import SeqIO

print 'Function: this python shell is designed for Filtering, Classified and Summarizing blast-output (a text file) agaisnt a self-made database! Put i)blast.txt, 2)database 3)this script under the same directory before running!'

while True:
    Parameters=raw_input("Enter parameters: names of [blast-output],[db_directory],[similarity_range](%)(e.g. 90-100),[align_num] sepeated by Space: ")
    try:
        filename=Parameters.split(' ')[0]
        database=Parameters.split(' ')[1]
        similarity_range=Parameters.split(' ')[2]
        align_num=Parameters.split(' ')[3]

        s_min=similarity_range.split('-')[0]
        s_max=similarity_range.split('-')[1]

        if not os.path.exists(filename):
            print 'errors: [blast-output] not found in the working directory!'
            continue
        
        if not os.path.exists(database):
            print 'errors: [db_directory] not found in the working directory!'
            continue
        
        break
    
    except:
        print 'errors: invalid input format or not enough input !'
        continue
    
#(1)Filtering

start=time.time()
wrerr=sys.stderr.write

file1=open(filename,'r')
filename1=filename.replace('.txt','')

if os.path.exists('Results_'+filename1+'_'+similarity_range):
    for root, dirs, files in os.walk('Results_'+filename1+'_'+similarity_range):
        for name in files:
            os.remove(os.path.join(root,name))        
else:
    os.mkdir('Results_'+filename1+'_'+similarity_range) 

output1=open('Results_'+filename1+'_'+similarity_range+'\\'+'Filtered_'+filename, 'w')

count=0
seq=0
c=[]
for line in file1:
    seq+=1
    try:
        A=float(line.split('\t')[2])
        B=int(line.split('\t')[3])
    except:
        print '\n'+'Errors: line ',seq,'of the file',filename,'is not complete, pls check it!'+'\n'
        continue
    if A>=float(s_min) and A<=float(s_max) and B>=int(align_num) and c.count(line.split('\t')[0])==0:
        output1.write(line.strip()+'\n')
        count+=1
        c.append(line.split('\t')[0])
    if seq%100000==0:
        print 'More than'+' '+str(seq)+' '+'query ids are Filtered in '+filename

print str(count)+' '+'query ids left after Filtering at similarity of '+str(similarity_range)+'% and align_num of '+ str(align_num)
end=time.time()
wrerr("OK, (1)Filtering finished finished in %3.2f secs\n" % (end-start))

#(2)Classified

start=time.time()
wrerr = sys.stderr.write

a={}
b=[]

if not os.path.exists(database+'_ids.txt'):
    for root,dirs,files in os.walk(database):
        for file in files:
            for record in SeqIO.parse(os.path.join(root, file), 'fasta'):
                b.append(record.id)
            a[os.path.join(root, file).split('\\')[-2]+'-'+os.path.join(root, file).split('\\')[-1]]=b
            b=[]
        output2=open(database+'_ids.txt','w')
        output2.write('Categories_in_database'+'\t'+'Corresponding_ids'+'\n')
        for key in sorted(a.keys()):
            output2.write(str(key)+'\t'+str(a[key])+'\n')
            
else:
    for line in open(database+'_ids.txt','r'):
        a[line.split('\t')[0]]=line.split('\t')[1]
        b=[]

if os.path.exists('Results_'+filename1+'_'+similarity_range+'\\'+'Classified_'+filename1):
    for root, dirs, files in os.walk('Results_'+filename1+'_'+similarity_range+'\\'+'Classified_'+filename1):
        for name in files:
            os.remove(os.path.join(root,name))
else:
    os.mkdir('Results_'+filename1+'_'+similarity_range+'\\'+'Classified_'+filename1)

file1.close()
output1.close()

file2=open('Results_'+filename1+'_'+similarity_range+'\\'+'Filtered_'+filename,'r')
output3=open('Results_'+filename1+'_'+similarity_range+'\\'+'ID_Categories_'+filename1+'.txt','w')

f={}
for line in file2:
    num=0
    for key in a.keys():
        if line.split('\t')[1] in a[key]:
            num+=1
            output3.write(line.split('\t')[0]+'\t'+line.split('\t')[1]+'\t'+key+'\n')
            output4=open('Results_'+filename1+'_'+similarity_range+'\\'+'Classified_'+filename1+'\\'+key+'.txt','a')
            output4.write(line.strip()+'\n')
            f[line.split('\t')[1]]=key
        else:
            continue
    if num==0:
        output5=open('Results_'+filename1+'_'+similarity_range+'\\'+'Query_id_abnormal.txt','a')
        output5.write(line.split('\t')[0]+'\t'+line.split('\t')[1]+'\t'+'Not Found in '+database+'\n')
    if num>=2:
        output5=open('Results_'+filename1+'_'+similarity_range+'\\'+'Query_id_abnormal.txt','a')
        output5.write(line.split('\t')[0]+'\t'+line.split('\t')[1]+'\t'+'Have '+str(num)+ ' categories in database'+'\n')
    if len(line)==0:
        break
             
end=time.time()        
wrerr("OK, (2)Classifying finished in %3.2f secs\n" % (end-start))

output3.close()

#(3)Summarizing
print 'Summarizing information...'

start=time.time()
wrerr = sys.stderr.write

output6=open('Results_'+filename1+'_'+similarity_range+'\\'+'Table_'+filename1+'.xls','w')
output7=open('Results_'+filename1+'_'+similarity_range+'\\'+'Summarzing_'+filename1+'.xls','w')

output6.write('Categories_in_database'+'\t'+'Query_id_num'+'\n')
output7.write('Subject_id_list'+'\t'+'Num'+'\t'+'Category_in_database'+'\t'+'min_s'+'\t'+'max_s'+'\t'+'min(align_num)'+'\t'+'max(align_num)'+'\n')

ID_collection=[]
Folder_collection=[]
for line in open('Results_'+filename1+'_'+similarity_range+'\\'+'ID_Categories_'+filename1+'.txt','r'):
    ID_collection.append(line.split('\t')[1])
    Folder_collection.append(line.split('\t')[-1].strip())

y1=list(set(Folder_collection))
for item in y1:
    output6.write(item+'\t'+str(Folder_collection.count(item))+'\n')
        
d1=list(set(ID_collection))
d2={}
for item in d1:
    d2[item]=str(ID_collection.count(item))

for item in d2.keys():
    k1=[]
    k2=[]
    for line in open('Results_'+filename1+'_'+similarity_range+'\\'+'Filtered_'+filename,'r'):
        if line.split('\t')[1]==item:
            k1.append(float(line.split('\t')[2]))
            k2.append(line.split('\t')[3])
    output7.write(item+'\t'+d2[item]+'\t'+f[item]+'\t'+str(min(k1))+'\t'+str(max(k1))+'\t'+str(min(k2))+'\t'+str(max(k2))+'\n')
    
end=time.time()        
wrerr("OK, (3)Summarizing finished in %3.2f secs\n" % (end-start))

output6.close()
output7.close()

print 'OK, all work finished!'
raw_input("Press <Enter> to close this window: ")




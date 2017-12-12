file_name1=raw_input("Enter the full name of id.txt: ")
file_name2=raw_input("Enter the full name of the database fasta: ") 

from Bio import SeqIO 
fileinput =open(file_name1,'r')
fileoutput=open('Extracted_sequences_'+file_name1,'w')

print 'The Python script is running... Pls wait!'

a=[]
for line in open(file_name1,'r'):
    a.append(str(line).strip())
    
b=list(set(a))
print len(a),'ids in '+file_name1
print len(b),'unique ids in '+file_name1

Num=0
for record in SeqIO.parse(file_name2,'fasta'):
    Num+=1    
    if str(record.id).strip() in b:
        fileoutput.write('>'+str(record.id).strip()+'\n')
        fileoutput.write(str(record.seq).strip()+'\n')
        b.remove(str(record.id).strip())
    if Num%100000==0:
        print Num, 'sequences have been searched!'

print len(b),'ids in',file_name1,'are not found in',file_name2
if len(b)!=0:
    fileoutput1=open('ID_Not_Found_'+file_name1,'w')
    for item in b:
        fileoutput1.write(item+'\n')     
print 'OK, Finished!'
raw_input("Press <Enter> to close this window: ")

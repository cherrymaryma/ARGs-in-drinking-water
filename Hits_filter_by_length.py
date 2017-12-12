###Author:Ju Feng, Environmental Biotechnology Lab, The University of Hong Kong
###Contact:Richieju520@gmail.com
###This script is a draft and the author is not responsible for its misuse.

print 'This script is written for extracting filtering blast hits using reads length and alignment_length coverage!'
import os
import time, sys
from Bio import SeqIO

while True:
    Parameters=raw_input("Enter parameters 1.[blast.txt], 2.[fasta],3.[min_length] and 4.[length_coverage](default: 0)sepeated by Space: ")
    try:
        X1=Parameters.strip().split(' ')[0]
        X2=Parameters.strip().split(' ')[1]
        X3=int(Parameters.strip().split(' ')[2])
        X4=float(Parameters.strip().split(' ')[3])
        break
    except:
         print 'errors: invalid input format or not enough input !'
         continue

f=open(str(X1)+'_'+str(X3)+'_'+str(X4)+'.blast','w')
a={}
i=0
m=0
for record in SeqIO.parse(X2,'fasta'):
    i+=1
    if i%1000000==0:
        print i,'sequences have been processed!'
    a[str(record.id)]=len(str(record.seq))
    if len(record.seq)< X3:
        m+=1

print m,'out of',i,'sequences with length less than',X3

j,k=0,0
for line in open(X1,'r'):
    k+=1
    if k%100000==0:
        print k,'hits have been processed!'
    lis=line.split('\t')
    if a[lis[0]]>=X3 and (float(lis[3])/a[lis[0]])>=X4:
        f.write(line)
    else:
        j+=1

print j,'out of',k,'hits were discarded by filtering!'
    
print 'OK, Finished!'
raw_input('Press <Enter> to close this window!')





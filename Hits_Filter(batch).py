###Author:Ju Feng, Environmental Biotechnology Lab, The University of Hong Kong
###Contact:Richieju520@gmail.com
###This script is a draft and the author is not responsible for its misuse.

import os
import time, sys
from Bio import SeqIO

print 'Function: this python shell is designed for Filtering blast-txts (in a folder) at a given cutoff!'
while True:
    Parameters=raw_input("Enter parameters: [foldername],[similarity]%,[align_num] cutoff and [evalue] cutoff sepeated by Space: ")
    try:
        foldername=Parameters.split(' ')[0]
        similarity=Parameters.split(' ')[1]
        align_num=Parameters.split(' ')[2]
        evalue=Parameters.split(' ')[3]
        if not os.path.exists(foldername):
            print 'errors: [foldername] not found in the working directory!'
            continue
        break
    
    except:
        print 'errors: invalid input format or not enough input !'
        continue
    
#(1)Filtering

if os.path.exists(foldername+'_'+similarity+'_'+align_num+'_'+evalue):
    for root, dirs, files in os.walk(foldername+'_'+similarity+'_'+align_num+'_'+evalue):
        for name in files:
            os.remove(os.path.join(root,name))        
else:
    os.mkdir(foldername+'_'+similarity+'_'+align_num+'_'+evalue) 

for root,dirs,files in os.walk(foldername):
    for file in files:
               
        start=time.time()
        wrerr=sys.stderr.write

        print '------','Processing',file,'in prograss','------'
        count, seq = 0, 0

        output=open(foldername+'_'+similarity+'_'+align_num+'_'+evalue+'/'+file+'.filtered.blast', 'w')
        
        for line in open(os.path.join(root, file), 'r'):

            seq+=1
            lis = line.strip().split('\t')
            A=int(lis[3])
            B=float(lis[10])
            C=float(lis[2])
            
            if A>=int(align_num) and B<=float(evalue) and C>=float(similarity) :
                output.write(line.strip()+'\n')
                count+=1
         
            if seq%100000==0:
                print 'More than'+' '+str(seq)+' '+'hits have been Filtered in '+foldername

        print seq,'hits in total!'
        print str(count)+' '+'query ids left after Filtering at evlue cutoff of '+str(evalue)+', similarity of '+ str(similarity)+' and align_num of '+ str(align_num)
        end=time.time()
        wrerr("OK, (1)Filtering finished finished in %3.2f secs\n" % (end-start))

print 'OK, all work finished!'
raw_input("Press <Enter> to close this window: ")




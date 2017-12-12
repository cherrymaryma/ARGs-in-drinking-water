###Author:Ju Feng, Environmental Biotechnology Lab, The University of Hong Kong
###Contact:Richieju520@gmail.com
###This script is a draft and the author is not responsible for its misuse.

print 'Function: this python script is written for screening and extracting those sequnces with bp_number over [Num] from a fasta file!'
import time, sys
from Bio import SeqIO

Paras=raw_input("Pls enter 2 parameters: [fasta_name],[Num] sepeated by <Space>: ")
while True:
    try:
        filename=Paras.split(' ')[0]
        N=Paras.split(' ')[1]
        f=open(filename,'r')
        f1=open(N+'bp+_'+filename,'w')

        for record in SeqIO.parse(filename,'fasta'):
            if len(record.seq)>=int(N):
                f1.write('>'+str(record.id)+'\n')
                f1.write(str(record.seq)+'\n')
            else:
                continue
        break
    except:
        print 'Notice: invalid input format for parameter [fasta_name] or [Num]' 
        Paras=raw_input("Pls enter 2 parameters: [fasta_name],[Num] sepeated by Space: ")
        
f1.close()
f.close()
print 'OK, Finished!'
raw_input('Press <Enter> to close this window: ')

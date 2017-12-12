import os
import math
import time, sys
from Bio import SeqIO
from Bio.Seq import reverse_complement

print 'This script is written for counting each reads length!'

Fasta_name =raw_input("Enter [Fasta_name]: ")
  
start=time.time()
wrerr = sys.stderr.write


f=open('log_'+Fasta_name.replace('.fasta','.txt'),'w')
num = 0

for record in SeqIO.parse(Fasta_name, 'fasta'):
    num+=1
    if num%20000 ==0:
        print num,'sequences have been processed!'
    f.write(str(record.id)+'\t'+str(len(record.seq))+'\n')

end=time.time()
wrerr("OK, Overlaping Finished in %3.2f secs\n" % (end-start))

f.close()

raw_input('Press <Enter> to close this window!')

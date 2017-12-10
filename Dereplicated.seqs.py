from Bio import SeqIO

print 'This script is used to delete repeated seqs and their correponding ids in a fasta file! The first seq and the corresponding id are preseved! '
filename1=raw_input("Enter the name of the fasta file: ")

f1=open('Unique_seqs.fasta','w')
f2=open('Repeated_seqs.txt','w')
a1={}
i1=0
j1=0
for record in SeqIO.parse(filename1,'fasta'):
    i1 += 1
    if i1%100000==0:
        print i1,'sequences have been processed!'
            
    a1[str(record.seq)]=i1
    
    if len(a1)+j1==i1:
        f1.write('>'+str(record.description)+'\n')
        f1.write(str(record.seq)+'\n')
        continue
    else:
        j1+=1
        f2.write('>'+str(record.description)+'\n')
        f2.write(str(record.seq)+'\n')

print i1,'sequences in total!'
print j1,'sequences are deleted!'
print 'OK, finished!'

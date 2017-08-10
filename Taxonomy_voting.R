grep -v "#" 1000bp_contig_ORF_130814.052232.32717.MetaGeneMark.txt | sed '/^$/d' | cut -f 1 > tmp1
grep -v "#" 1000bp_contig_ORF_130814.052232.32717.MetaGeneMark.txt | sed '/^$/d' | cut -f 9 | cut -d "," -f 1 | tr -s '= ' '_' > tmp2
paste tmp1 tmp2 > scaffold.rename.gff.modified
gff<-read.table("scaffold.rename.gff.modified",sep="\t") #scaffolds and gene relationship
colnames(gff)<-c("scaffold.name","gene_id")
genus<-read.table("1_Proteobacteria.orf.aa_withNR_-2_50(PhylumLevel).txt",sep="\t")
colnames(genus)<-c("gene_id","genus")
d.MYP<-merge(gff,genus,by="gene_id",all=T) # merge together gff and genus annotation
# replace <NA> with "Unclassified"
d.MYP$genus<-as.character(d.MYP$genus)
d.MYP$genus[is.na(d.MYP$genus)]<-c("Unclassified")
d.MYP$genus<-as.factor(d.MYP$genus)

tmp<-unique(d.MYP$scaffold.name)
length(tmp) #number of scaffolds
m<-length(unique(d.MYP$genus)) # num of genus 

x<-tapply(d.MYP$genus,d.MYP$scaffold.name,table)
phylum.MYP<-matrix(ncol=m,nrow=length(tmp))
for (i in 1:length(x)){
  phylum.MYP[i,]<-x[[i]]
}

colnames(phylum.MYP)<-names(x[[1]])
rownames(phylum.MYP)<-tmp


# test<-phylum.MYP[grep("239_Average_coverage_112.73",rownames(phylum.MYP)),]
# 
# grep("239_Average_coverage_112.73",tmp) #1434
# x[[1434]]
# grep("239_Average_coverage_112.73",rownames(phylum.MYP))
# phylum.MYP<-phylum.MYP[order(rownames(phylum.MYP)),]
# cbind(test,x[[1434]],table(d.MYP[grep("239_Average_coverage_112.73",d.MYP$scaffold.name),][,3]))


#transform into percentage
phylum.MYP<-cbind(phylum.MYP,apply(phylum.MYP,1,sum))
phylum.MYP<-phylum.MYP[,1:m]/phylum.MYP[,m+1] 

find<-function(x){
  y<-names(x[which.max(x)])
  z<-x[which.max(x)]
  return(c(y,z))}
phylum.MYP.v<-apply(phylum.MYP,1,find) # find the maximum phylum and corresponding percentage
phylum.MYP.v<-data.frame(t(phylum.MYP.v))
phylum.MYP.v$scaffold.name<-unique(d.MYP$scaffold.name)
colnames(phylum.MYP.v)<-c("phylum.MYP.v","phylum.MYP.v.per","scaffold.name")
phylum.MYP.v$phylum.MYP.v<-as.character(phylum.MYP.v$phylum.MYP.v)
phylum.MYP.v$phylum.MYP.v.per<-as.numeric(as.character(phylum.MYP.v$phylum.MYP.v.per))

# this is for checking the distribution of phylum percentage
tmp<-phylum.MYP.v[which(phylum.MYP.v$phylum.MYP.v!="Unclassified"),] # result in 40071 have phylum level annotation
tmp$phylum.MYP.v.per<-as.numeric(as.character(tmp$phylum.MYP.v.per))
hist(tmp$phylum.MYP.v.per) # check out the distribution

phylum.MYP.v[which(phylum.MYP.v$phylum.MYP.v.per<0.5),1]<-c("Unclassified") #here we use 0.5 as phylum voting cutoff from the nature communication paper
1-length(which(phylum.MYP.v$phylum.MYP.v=="Unclassified"))/nrow(phylum.MYP.v) 
0.56 # 56% ORF could be classified at genus 
d.MYP<-merge(d.MYP,phylum.MYP.v,by="scaffold.name",all=T)
write.csv(phylum.MYP.v,file="1_Proteobacteria_PhylumLevel_output.csv")

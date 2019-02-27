import os

#reads in sample data
data=[]
handle=open('sample.txt').readlines()
for i in handle:
	data.append(i)

#creates folder and sets cwd
path=input('Enter path: ')
cmd='mkdir '+path
os.system(cmd)
os.chdir(path)

#creates new file called OptionA.log
log=open('OptionA.log', 'a')

#1 cmd gets single-end reads of E coli K-12 strain from NCBI
cmd='wget '+data[0]
os.system(cmd)

#2 cmd extracts .fastq file from .sra file
cmd='fastq-dump -I --split-files SRR8185310.sra'
os.system(cmd)

#runs spades and outputs to the folder OptionA_Brian_Ho
cmd='spades -k 55,77,99,127 -t 2 --only-assembler -s SRR8185310_1.fastq -o '+path
log.write(cmd+'\n')
os.system(cmd)

#3 and 4
from Bio import SeqIO

#reads in contigs.fasta and stores each contig into contigs list
contigs=[]
handle=open('contigs.fasta')
for record in SeqIO.parse(handle, 'fasta'):
	contigs.append(record)
handle.close()

count=0
length=0
processed=[]
for contig in contigs:
	if len(contig.seq) > 1000: #if the length of the sequence > 1000, it keeps count of it and it adds the length to keep track of the total length of the assembly
			count+=1
			length+=len(contig.seq)
			processed.append(contig)
	else:
		continue

#writes to log
log.write('There are '+str(count)+' contigs > 1000 in the assembly.\n') 
log.write('There are '+str(length)+' bp in the assembly.\n') 

#replaces all contigs in contigs.fasta with only contigs > 1000
handle=open('contigs.fasta', 'w')
for contig in processed:
    handle.write('>'+str(contig.id)+'\n')
    handle.write(str(contig.seq)+'\n')
handle.close()

#5 cmd runs prokka with updated contigs.fasta and outputs into OptionA_Brian_Ho folder
cmd='prokka --cpus 2 --genus E --species coli --strain K12 --outdir SRR8185310_prokka --prefix SRR8185310_prokka contigs.fasta'
log.write(cmd+'\n')
os.system(cmd)

#6 writes the contents of SRR8185310_prokka.txt into log
handle=open('SRR8185310_prokka/SRR8185310_prokka.txt').readlines()

log.write(''.join(handle))

#7 checks for any descrepancy in number of CDS and tRNA
CDS=handle[4][5:] #number of CDS
trna=handle[3][6:] #number of tRNA

if int(CDS) < 4140:
	a=str(4140-int(CDS))+' less CDS'
elif int(CDS) > 4140:
	a=str(int(CDS)-4140)+' additional CDS'
else:
	a='the same number of CDS'

if int(trna) < 89:
	b=str(89-int(trna))+' less tRNA'
elif int(CDS) > 4140:
	b=str(int(trna)-89)+' additional tRNA'
else:
	b='the same number of tRNA'

if int(CDS) == 4140 and int(trna) == 89:
	log.write('Prokka found the same number of CDS and tRNA.\n') 
else:
	log.write('Prokka found '+a+' and  '+b+' than the RefSeq.\n')

log.close()

#8 cmd gets single-end reads of a differrent E coli K-12 strain from NCBI
cmd='wget '+data[1]
os.system(cmd)

#cmd extracts .fastq file from .sra file
cmd='fastq-dump -I --split-files SRR1411276.sra'
os.system(cmd)

#cmd gets complete genome of E coli K-12 from NCBI
cmd='wget '+data[2]
os.system(cmd)

#cmd uses bowtie2 to create an index of reference
cmd='bowtie2-build NC_000913.fna NC_000913_ref'
os.system(cmd)

#cmd runs tophat2
cmd='tophat2 -p 2 --no-novel-juncs -o SRR1411276_tophat2 NC_000913_ref SRR1411276_1.fastq' 
os.system(cmd)

#cmd runs cufflinks
cmd='cufflinks -p 2 -o SRR1411276_cufflinks SRR1411276_tophat2/accepted_hits.bam'
os.system(cmd)

#9 writes specific information from transcripts.gtf to Option1.fpkm
import csv
fpkm=open('Option1.fpkm', 'w')
writer = csv.writer(fpkm, delimiter=',')

writer.writerow(['seqname', 'start', 'end', 'strand', 'FPKM'])

handle=open('SRR1411276_cufflinks/transcripts.gtf')
for row in csv.reader(handle, delimiter='\t'):
    a=row[8].find('FPKM')
    b=row[8].find('frac')
    writer.writerow([row[0], row[3], row[4], row[6], row[8][a+6:b-3]])

handle.close()
fpkm.close()

print('Finished.')
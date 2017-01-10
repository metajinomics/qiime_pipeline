# qiime_pipeline
QIIME pipeline

#STEP 1: Demultiplex and merge sequence
## Demultiplex option1: make individual file
### demultiplex using jin’s code

### merge by pandaseq
```
for x in jin_new/*.R1.fastq.gz;do echo "pandaseq -f $x -r ${x%R1*}R2.fastq.gz -u ${x%R1*}unmerged.fa 2> ${x%R1*}pandastat.txt 1> ${x%R1*}fasta";done > command.panda.sh
cat command.panda.sh |parallel
```

### prepare mapping file
awk '{print $0 "\t" $1 ".fasta"}' jin_mapping.new.txt > jin_mapping.new.filename.txt
use emacs change last column InputFileName

### combine
add_qiime_labels.py -i small64/ -m  small64_mapping.txt -c InputFileName


## Demultiplex option2: merge without demultiplex
### Merge paired-end reads
join_paired_ends.py -f Undetermined_S0_L001_R1_001.fastq.gz -r Undetermined_S0_L001_R2_001.fastq.gz -o fastq-join_joined -b Undetermined_S0_L001_I1_001.fastq.gz

### Demultiplex
split_libraries_fastq.py -i fastqjoin.join.fastq -b fastqjoin.join_barcodes.fastq -o out_q20/ -m ../mapping.txt -q 19 --rev_comp_mapping_barcodes --store_demultiplexed_fastq

#STEP 2: Chimera detection
Install usearch
```
curl -O https://raw.githubusercontent.com/edamame-course/2015-tutorials/master/QIIME_files/usearch5.2.236_i86linux32
sudo cp usearch5.2.236_i86linux32 /usr/local/bin/usearch
sudo chmod +x /usr/local/bin/usearch
```
Install vsearch
```
wget https://github.com/torognes/vsearch/archive/v2.3.3.tar.gz
tar xzf v2.3.3.tar.gz
cd vsearch-2.3.3
./autogen.sh
./configure
make
make install
ln -s /usr/local/bin/vsearch /usr/local/bin/usearch61
```

chimera detection
```
wget http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/Caporaso_Reference_OTUs/gg_otus_4feb2011.tgz
tar -xvzf gg_otus_4feb2011.tgz
identify_chimeric_seqs.py -i combined_seqs.fna -m usearch61 -o usearch_checked_chimeras/ -r gg_otus_4feb2011/rep_set/gg_97_otus_4feb2011.fasta 
filter_fasta.py -f seqs.fna -o seqs_chimeras_filtered.fna -s usearch_checked_chimeras/chimeras.txt -n
```

#STEP 3: OTU picking
Run QIIME
```
pick_open_reference_otus.py -i seqs_chimeras_filtered.fna -o uclust_openref/
```
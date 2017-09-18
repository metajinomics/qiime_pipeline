# qiime pipeline
This is the QIIME pipeline for Eva

## move all fastq file into one folder
```
for x in ../../*.fastq.gz;do cp $x .;done
```

## merge paired end
```
mkdir merged
for x in *_R1_001.fastq.gz;do echo "../program/pandaseq/pandaseq -f $x -r ${x%_R1*}_R2_001.fastq.gz -u ${x%_R1*}unmerged.fa 2> ${x%_R1*}pandastat.txt 1> merged/${x%_R1*}.fasta";done > command.panda.sh
cat command.panda.sh | parallel
```

## make mapping file
```
git clone https://github.com/metajinomics/qiime_tools.git
python qiime_tools/make_mapping_file.py merged > mapping.file.txt
```

## download database for chimera removal
```
wget http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/Caporaso_Reference_OTUs/gg_otus_4feb2011.tgz
tar -xvzf gg_otus_4feb2011.tgz
```

## load module
```
module load bioinfo-tools
module load Qiime
```

## combine sequences
```
add_qiime_labels.py -i merged/ -m  mapping.txt -c InputFileName
```

## install vsearch
```
wget https://github.com/torognes/vsearch/archive/v2.3.3.tar.gz
tar xzf v2.3.3.tar.gz
cd vsearch-2.3.3
./autogen.sh
./configure
make
cd bin
mv vesarch usearch61
```
## set path, you need to set path everytime you log in
```
PATH=$PATH:/proj/~~~~
export PATH
```

## remove chimera
```
identify_chimeric_seqs.py -i combined_seqs.fna -m usearch61 -o usearch_checked_chimeras/ -r gg_otus_4feb2011/rep_set/gg_97_otus_4feb2011.fasta 
filter_fasta.py -f combined_seqs.fna -o seqs_chimeras_filtered.fna -s usearch_checked_chimeras/chimeras.txt -n
```

## run qiime pipeline
```
pick_open_reference_otus.py -i seqs_chimeras_filtered.fna -o uclust_openref/
```

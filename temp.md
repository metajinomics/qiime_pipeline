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


# Here first try


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
## note that it might be a faster process to first perform the chimera check of each sample, filter away the chimeras, and then combine the samples. After which the qiime pipeline can be launched.

## load module
```
module load bioinfo-tools
module load Qiime
```

## combine sequences
```
add_qiime_labels.py -i merged/ -m  mapping.file.txt -c InputFileName
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
mv vsearch usearch61
```
## set path, you need to set path everytime you log in
```
PATH=$PATH:/proj/b2016430/nobackup/projects/16S18S/vsearch-2.3.3/bin
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


# Here second try: If you want to run 16S/18S together
## download database
```
wget https://www.arb-silva.de/fileadmin/silva_databases/qiime/Silva_128_release.tgz
```

## run vsearch to remove chimera
### Assume, you already have vsearch installed. then set path, you need to set path everytime you log in
```
PATH=$PATH:/proj/b2016430/nobackup/projects/16S18S/vsearch-2.3.3/bin
export PATH
```
### run vsearch
```
vsearch -uchime_ref YOUR.fasta -db SILVA_128_QIIME_release/rep_set/rep_set_all/97/97_otus.fasta -strand plus -nonchimeras nochimera.fna -threads 10
```
### let's make it faster
```
for x in merged/*.fastq;do echo "vsearch -uchime_ref $x -db SILVA_128_QIIME_release/rep_set/rep_set_all/97/97_otus.fasta -strand plus -nonchimeras $x.nochimera.fna -threads 10";done > command.chimera.sh
cat command.chimera.sh | parallel
```
## make mapping file

## combine sequences

## run qiime pipeline
### first, you need to make file param.txt
```
pick_otus:enable_rev_strand_match True
assign_taxonomy:assignment_method blast
assign_taxonomy:id_to_taxonomy_fp SILVA_128_QIIME_release/taxonomy/taxonomy_all/97/consensus_taxonomy_all_levels.txt
assign_taxonomy:reference_seqs_fp SILVA_128_QIIME_release/rep_set/rep_set_all/97/97_otus.fasta
```

### then run qiime
```
module load bioinfo-tools
module load blast/2.2.26

pick_open_reference_otus.py -i COMBINED.fasta -r SILVA_128_QIIME_release/rep_set/rep_set_all/97/97_otus.fasta -o qiime_output -p params.txt --suppress_align_and_tree
```


# If you want to run 18S along


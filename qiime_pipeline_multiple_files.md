# This pipeline run Qiime when you have demultiplexed file

### merge by pandaseq
This stop merge forward and reverse read into one
```
mkdir merged
module load pandaseq
for x in *_R1_*;do echo "pandaseq -f $x -r ${x%_R1*}_R2_001.fastq.gz > merged/${x%_R1*}.fasta";done > command.merge.sh
bash command.merge.sh
```

### make mapping file
mapping file is needed in qiime software, tell sample ID and filename 
```
python /mnt/home/choiji22/git/qiime_tools/make_mapping_file.py merged > mapping.txt
```

### start qiime1
using miniconda3, start virtual environment for qiime 
```
source /mnt/home/choiji22/miniconda3/bin/activate qiime1
```

### combine
This step will combine many files into one file
```
add_qiime_labels.py -i merged -m  mapping.txt -c InputFileName
```
This command will generate file "combined_seqs.fna"

### Chimera detection
#### Download database
```
wget http://greengenes.lbl.gov/Download/Sequence_Data/Fasta_data_files/Caporaso_Reference_OTUs/gg_otus_4feb2011.tgz
tar -xvzf gg_otus_4feb2011.tgz
```

#### detect and remove chimera
```
export PATH=$PATH:/mnt/home/choiji22/vsearch-2.3.3/bin
identify_chimeric_seqs.py -i combined_seqs.fna -m usearch61 -o usearch_checked_chimeras/ -r gg_otus_4feb2011/rep_set/gg_97_otus_4feb2011.fasta 
filter_fasta.py -f combined_seqs.fna -o combined_seqs_chimeras_filtered.fna -s usearch_checked_chimeras/chimeras.txt -n
```

### run qiime
```
pick_open_reference_otus.py -i combined_seqs_chimeras_filtered.fna -o uclust_openref/
```

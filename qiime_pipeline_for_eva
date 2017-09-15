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

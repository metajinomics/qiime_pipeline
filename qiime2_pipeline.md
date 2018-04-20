## Qiime 2
#### start virtual environment for qiime2
```
source /mnt/research/germs/softwares/miniconda2/bin/activate qiime2-2018.2
```

#### import paired end fastq file
```
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path liz \
  --source-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path demux-paired-end.qza
  
```
join read

```
qiime vsearch join-pairs --i-demultiplexed-seqs demux-paired-end.qza --o-joined-sequences demux-joined.qza
```


4   # to see summary

qiime demux summarize \
>   --i-data demux-joined.qza \
>   --o-visualization demux-joined.qzv
Saved Visualization to: demux-joined.qzv

To visualize the it, we can copy the file to local computer and drag it to https://view.qiime2.org/

#quality check based on the visualization
qiime quality-filter q-score-joined \
>   --i-demux demux-joined.qza \
>   --o-filtered-sequences demux-joined-filtered.qza \
>   --o-filter-stats demux-joined-filter-stats.qza

Saved SampleData[JoinedSequencesWithQuality] to: demux-joined-filtered.qza
Saved QualityFilterStats to: demux-joined-filter-stats.q



5 #Deblur
qiime deblur denoise-16S \
  --i-demultiplexed-seqs demux-joined-filtered.qza \
  --p-trim-length 255 \
  --p-sample-stats \
  --o-representative-sequences rep-seqs.qza \
  --o-table table.qza \
  --o-stats deblur-stats.qza
Saved FeatureTable[Frequency] to: table.qza
Saved FeatureData[Sequence] to: rep-seqs.qza
Saved DeblurStats to: deblur-stats.qza



6 
qiime feature-table summarize \
  --i-table table.qza \
  --o-visualization table.qzv
Saved Visualization to: table.qzv

7 
https://docs.qiime2.org/2018.2/tutorials/chimera/

#chimera checking

https://docs.qiime2.org/2018.2/tutorials/moving-pictures/#demultiplexing-sequences
 8  qiime alignment mafft \
>   --i-sequences rep-seqs.qza \
>   --o-alignment aligned-rep-seqs.qza



Saved FeatureData[AlignedSequence] to: aligned-rep-seqs.qza
9    qiime alignment mask \
>   --i-alignment aligned-rep-seqs.qza \
>   --o-masked-alignment masked-aligned-rep-seqs.qza
Saved FeatureData[AlignedSequence] to: masked-aligned-rep-seqs.qza
 
10   qiime phylogeny fasttree \
>   --i-alignment masked-aligned-rep-seqs.qza \
>   --o-tree unrooted-tree.qza
Saved Phylogeny[Unrooted] to: unrooted-tree.qza



 11  qiime phylogeny midpoint-root \
>   --i-tree unrooted-tree.qza \
>   --o-rooted-tree rooted-tree.qza
Saved Phylogeny[Rooted] to: rooted-tree.qza


now i have a phylogenetic tree.
But i dont have OTU table.

actually i have the OTU table

qiime tools export table.qza --output-dir ./




denoise?
```
qiime dada2 denoise-single \
  --i-demultiplexed-seqs demux-paired-end.qza \
  --p-trim-left 0 \
  --p-trunc-len 120 \
  --o-representative-sequences rep-seqs-dada2.qza \
  --o-table table-dada2.qza
```

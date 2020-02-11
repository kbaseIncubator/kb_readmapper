#!/bin/sh

/kb/module/bbmap/bbmap.sh in=$1 ref=$2 out=out.bam
samtools sort out.bam  -o sorted.bam
jgi_summarize_bam_contig_depths sorted.bam --outputDepth $3


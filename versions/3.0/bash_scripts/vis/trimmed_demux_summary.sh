#!/bin/bash
#SBATCH --job-name=trimmed_demux_summary
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime demux summarize \
--i-data /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_trimmed-demux-seqs.qza \
--o-visualization /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_trimmed-demux-seqs.qzv 

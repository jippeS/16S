#!/bin/bash
#SBATCH --job-name=Masking_alignment
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8

qiime alignment mask \
--i-alignment /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_aligned-rep-seqs.qza \
--o-masked-alignment /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_masked_aligned-rep-seqs.qza

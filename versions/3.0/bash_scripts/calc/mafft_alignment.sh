#!/bin/bash
#SBATCH --job-name=Mafft_alignment
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16

qiime alignment mafft \
--i-sequences /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_representative_sequences.qza \
--o-alignment /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_aligned-rep-seqs.qza \
--p-n-threads 16 

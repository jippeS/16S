#!/bin/bash
#SBATCH --job-name=representative_sequences_export
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime tools export \
--input-path /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_representative_sequences.qza \
--output-path /export/jippe/jsil/projects/16S/RBRA/

#!/bin/bash
#SBATCH --job-name=feature_table_tabulate
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime feature-table tabulate-seqs \
--i-data /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_representative_sequences.qza \
--o-visualization /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_representative_sequences.qzv

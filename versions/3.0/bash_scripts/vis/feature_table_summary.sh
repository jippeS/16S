#!/bin/bash
#SBATCH --job-name=feature_table_summary
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime feature-table summarize \
--i-table /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_table.qza \
--m-sample-metadata-file /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330@metadata.txt \
--o-visualization /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_table.qzv

#!/bin/bash
#SBATCH --job-name=Metadata_tabulate
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime metadata tabulate \
--m-input-file /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_denoising_stats.qza \
--o-visualization /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_denoising_stats.qzv

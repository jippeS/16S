#!/bin/bash
#SBATCH --job-name=classifier_tabulate
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime metadata tabulate \
--m-input-file /export/jippe/jsil/projects/16S/NB_classifier_SILVA_138_99_16S_515F-926R_QIIME2-2022.11.qza \
--o-visualization /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_taxonomy_NB_classifier_SILVA_132_99_16S_515F-926R_QIIME2-2022.11.qzv

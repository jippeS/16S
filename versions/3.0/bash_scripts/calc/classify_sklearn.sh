#!/bin/bash
#SBATCH --job-name=Classifying_sklearn
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16

qiime feature-classifier classify-sklearn \
--i-classifier /export/jippe/jsil/db/Qiime2/qiime2-2022.11/Silva/138/silva-138-99-nb-classifier.qza \
--i-reads /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_representative_sequences.qza \
--o-classification /export/jippe/jsil/projects/16S/NB_classifier_SILVA_138_99_16S_515F-926R_QIIME2-2022.11.qza \
--p-n-jobs 16 \
--p-reads-per-batch 200

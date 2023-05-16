#!/bin/bash
#SBATCH --job-name=classifier_export
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1


qiime tools export \
--input-path /export/jippe/jsil/projects/16S/NB_classifier_SILVA_138_99_16S_515F-926R_QIIME2-2022.11.qza \
--output-path /export/jippe/jsil/projects/16S/RBRA/

#!/bin/bash
#SBATCH --output=merge_tax_%j.out
#SBATCH --job-name=Import_data
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

# Merge classifiers (taxonomy)
qiime feature-table merge-taxa --o-merged-data $1 --i-data ABOR_16S_515F_926R_13092024_Q17841_ABOR_silva-138-99-nb-classifier_515f_926R.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partA_ABOR_silva-138-99-nb-classifier_515f_926R.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partB_ABOR_silva-138-99-nb-classifier_515f_926R.qza

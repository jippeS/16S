#!/bin/bash
#SBATCH --output=merge_table_%j.out
#SBATCH --job-name=merge_table
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

# Merge feature tables
qiime feature-table merge --o-merged-table $1  --i-tables /export/projects/16S/RPEI/20_05_2020_Q9407/SAM1-30/output/Artifacts_qza/RPEI_16S_515F_926R_20052020_Q9407_RPEI_table.qza /export/projects/16S/RPEI/20_05_2020_Q9407/SAM31-32/output/Artifacts_qza/RPEI_16S_515F_926R_20052020_Q9407_RPEI_table.qza

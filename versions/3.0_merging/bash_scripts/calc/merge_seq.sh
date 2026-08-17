#!/bin/bash
#SBATCH --output=merge_seq_%j.out
#SBATCH --job-name=Import_data
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

# Merge representative sequences
qiime feature-table merge-seqs --o-merged-data $1 --i-data /export/projects/16S/RPEI/20_05_2020_Q9407/SAM1-30/output/Artifacts_qza/RPEI_16S_515F_926R_20052020_Q9407_RPEI_representative_sequences.qza /export/projects/16S/RPEI/20_05_2020_Q9407/SAM31-32/output/Artifacts_qza/RPEI_16S_515F_926R_20052020_Q9407_RPEI_representative_sequences.qza


#!/bin/bash
#SBATCH --output=Tabulate_feature_table_%j.out
#SBATCH --job-name=feature_table_tabulate
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=flex3

qiime feature-table tabulate-seqs --i-data $1 --o-visualization $2

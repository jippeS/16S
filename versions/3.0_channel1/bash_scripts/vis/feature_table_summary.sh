#!/bin/bash
#SBATCH --output=Summarize_feature_table_%j.out
#SBATCH --job-name=feature_table_summary
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=flex3

qiime feature-table summarize --i-table $1 --m-sample-metadata-file $2 --o-visualization $3

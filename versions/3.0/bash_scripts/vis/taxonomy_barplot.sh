#!/bin/bash
#SBATCH --output=taxonomy_%j.out
#SBATCH --job-name=taxonomy_barplot
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime taxa barplot --i-table $1 --i-taxonomy $2 --m-metadata-file $3 --o-visualization $4

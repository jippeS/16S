#!/bin/bash
#SBATCH --job-name=Alpha_rarefaction
#SBATCH --output=Alpha_rarefaction_%j.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime diversity alpha-rarefaction --i-table $1 --i-phylogeny $2 --p-max-depth $3 --m-metadata-file $4 --o-visualization $5

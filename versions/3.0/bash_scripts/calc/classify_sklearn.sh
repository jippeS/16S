#!/bin/bash
#SBATCH --output=Classifying_%j.out
#SBATCH --job-name=Classifying_sklearn
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8

qiime feature-classifier classify-sklearn --i-classifier $1 --i-reads $2 --o-classification $3 --p-n-jobs $4 --p-reads-per-batch $5

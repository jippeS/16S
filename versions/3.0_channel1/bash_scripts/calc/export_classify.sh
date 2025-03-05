#!/bin/bash
#SBATCH --output=Exp_classify_%j.out
#SBATCH --job-name=Exporting_files
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=flex3

qiime tools export --input-path $1 --output-path $2

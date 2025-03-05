#!/bin/bash
#SBATCH --output=Demux_summary_%j.out
#SBATCH --job-name=demux_summary
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=flex3

qiime demux summarize --i-data $1 --o-visualization $2

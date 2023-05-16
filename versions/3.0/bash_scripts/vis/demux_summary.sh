#!/bin/bash
#SBATCH --job-name=demux_summary
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime demux summarize \
--i-data $1 \
--o-visualization $2

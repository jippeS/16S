#!/bin/bash
#SBATCH --output=Pipeline_execution.txt
#SBATCH --job-name=16S_pipeline
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --nodelist=cn2


#FORW=$1
#REVE=$2
#OUT=$3
snakemake --snakefile snakefile_16S.smk --unlock

snakemake \
  --snakefile snakefile_16S.smk \
  -c 10 \
  --latency-wait 30 \
  --use-conda \
 # --config forw=$FORW reve=$REVE output=$OUT


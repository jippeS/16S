#!/bin/bash
#SBATCH --output=Pipeline_execution.txt
#SBATCH --job-name=16S_pipeline
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --nodelist=cn2

snakemake --snakefile snakefile_16S.smk --unlock

snakemake --snakefile snakefile_16S.smk -c 8 --latency-wait 30 --use-conda


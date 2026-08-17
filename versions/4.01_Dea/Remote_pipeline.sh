#!/bin/bash
#SBATCH --output=Pipeline_execution.txt
#SBATCH --job-name=16S_pipeline
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --nodelist=cn2

snakemake --snakefile snakefile_16S.smk --unlock

#snakemake --snakefile snakefile_16S.smk -c 10 --latency-wait 30 --use-conda

snakemake --snakefile snakefile_16S.smk --config forw="$1" reve="$2" -c 5 --latency-wait 30 -j --use-conda --allowed-rules denoising_paired --rerun-triggers mtime

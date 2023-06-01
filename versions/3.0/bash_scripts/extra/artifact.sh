#!/bin/bash
#SBATCH --output=Creating_artifact_%j.out
#SBATCH --job-name=artifact
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' --input-path $1 --output-path $2 --input-format PairedEndFastqManifestPhred33V2

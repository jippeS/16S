#!/bin/bash
#SBATCH --output=Creating_artifact_%j.out
#SBATCH --job-name=artifact
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8

qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' --input-path $1 --output-path $2 --input-format PairedEndFastqManifestPhred33

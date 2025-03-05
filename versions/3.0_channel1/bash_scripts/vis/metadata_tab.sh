#!/bin/bash
#SBATCH --output=Tabulate_metadata_%j.out
#SBATCH --job-name=Metadata_tabulate
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --nodelist=flex3

qiime metadata tabulate --m-input-file $1 --o-visualization $2

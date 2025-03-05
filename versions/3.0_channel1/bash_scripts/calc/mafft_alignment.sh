#!/bin/bash
#SBATCH --output=Mafft_alignment_%j.out
#SBATCH --job-name=Mafft_alignment
#SBATCH --partition=Superflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=flex3

#--partition=Bytesflex
qiime alignment mafft --i-sequences $1 --o-alignment $2 --p-n-threads $3 

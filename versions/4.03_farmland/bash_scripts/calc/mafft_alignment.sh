#!/bin/bash
#SBATCH --output=Mafft_alignment_%j.out
#SBATCH --job-name=Mafft_alignment
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16

#--partition=Bytesflex
qiime alignment mafft --i-sequences $1 --o-alignment $2 --p-n-threads $3 

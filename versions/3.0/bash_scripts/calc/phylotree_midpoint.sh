#!/bin/bash
#SBATCH --output=Phylogenetic_midpoint_%j.out
#SBATCH --job-name=Retrieving_phylo_midpoint
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

qiime phylogeny midpoint-root --i-tree $1 --o-rooted-tree $2

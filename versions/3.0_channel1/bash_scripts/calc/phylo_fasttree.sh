#!/bin/bash
#SBATCH --output=Phylogenetic_fasttree_%j.out
#SBATCH --partition=Superflex
#SBATCH --job-name=Getting_phylo_tree
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=flex3

qiime phylogeny fasttree --i-alignment $1 --o-tree $2 --p-n-threads $3

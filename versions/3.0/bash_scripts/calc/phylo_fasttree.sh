#!/bin/bash
#SBATCH --job-name=Getting_phylo_tree
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16

qiime phylogeny fasttree \
--i-alignment /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_masked_aligned-rep-seqs.qza \
--o-tree /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_unrooted-tree.qza \
--p-n-threads 16

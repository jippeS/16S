#!/bin/bash
#SBATCH --job-name=Retrieving_phylo_midpoint
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8

qiime phylogeny midpoint-root \
--i-tree /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_unrooted-tree.qza \
--o-rooted-tree /export/jippe/jsil/projects/16S/RBRA/RBRA_16S_515F926R_Q11696_20230330_rooted-tree.qza

#!/bin/bash
#SBATCH --output=16S_Q2_%j.out
#SBATCH --job-name=q2_16S
#SBATCH --partition=Bytesflex
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16

# Activate QIIME2 environment
echo "Activating QIIME2 amplicon deployment version 2022.11.16S"
source /export/microlab/miniconda3/etc/profile.d/conda.sh
conda activate qiime2-2022.11.16S

# Navigate to the data directory
cd /users/STEU/merge_phyloseq/ABOR

# Create a directory for merged data
mkdir -p merged_data

# Merge feature tables
qiime feature-table merge \
    --i-tables ABOR_16S_515F_926R_13092024_Q17841_ABOR_table.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partA_ABOR_table.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partB_ABOR_table.qza \
    --o-merged-table "merged_data/merged-table.qza"

# Merge representative sequences
qiime feature-table merge-seqs \
    --i-data ABOR_16S_515F_926R_13092024_Q17841_ABOR_representative_sequences.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partA_ABOR_representative_sequences.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partB_ABOR_representative_sequences.qza \
    --o-merged-data "merged_data/merged-rep-seqs.qza"

# Merge classifiers (taxonomy)
qiime feature-table merge-taxa \
    --i-data ABOR_16S_515F_926R_13092024_Q17841_ABOR_silva-138-99-nb-classifier_515f_926R.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partA_ABOR_silva-138-99-nb-classifier_515f_926R.qza ABOR_16S_515F_926R_17_10_2024_Q17999_partB_ABOR_silva-138-99-nb-classifier_515f_926R.qza \
    --o-merged-data "merged_data/merged-silva-taxonomy.qza"

# Multiple sequence alignment met MAFFT
qiime alignment mafft \
    --i-sequences "merged_data/merged-rep-seqs.qza" \
    --o-alignment "merged_data/merged-aligned-rep-seqs.qza" \
    --p-n-threads 16

# Check if alignment was successful
if [ -f "merged_data/merged-aligned-rep-seqs.qza" ]; then
    echo -e "merged-aligned-rep-seqs.qza is successfully created"
else 
    echo -e "Error: merged alignment file not present"
fi

# Masking the MSA
qiime alignment mask \
    --i-alignment "merged_data/merged-aligned-rep-seqs.qza" \
    --o-masked-alignment "merged_data/masked-merged-aligned-rep-seqs.qza"

# Making phylogenetic tree
qiime phylogeny fasttree \
    --i-alignment "merged_data/masked-merged-aligned-rep-seqs.qza" \
    --o-tree "merged_data/merged-unrooted-tree.qza" \
    --p-n-threads 16

# Determining midpoint root
qiime phylogeny midpoint-root \
    --i-tree "merged_data/merged-unrooted-tree.qza" \
    --o-rooted-tree "merged_data/merged-rooted-tree.qza"

# Check if rooted tree was created successfully
if [ -f "merged_data/merged-rooted-tree.qza" ]; then
    echo -e "rooted-tree.qza is successfully created"
else 
    echo -e "Error: rooted tree file not present"
fi

sleep 2

echo "finished merging script"

# Deactivate conda environment
conda deactivate

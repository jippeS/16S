configfile: "config.yaml"

from os import listdir
from os.path import isfile, join
import os
import re
import argparse
import sys

folder_path = config["inputdir"]

# Retrieve directory names in the specified folder
directory_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

# Print the directory names
folder_name = ""
for directory_name in directory_names:
    folder_name = directory_name
folder_name = f"{folder_name}"

# Get the classifier name
classifier_name = config["classifier"].split("/")[-1][:-4]

# Make the outputdir
outputdir = config["inputdir"] + "output/"

rule all:
    input:
        outputdir + "reports/Qiime_report.txt"
        # outputdir + "Visualization_qzv/" + config["naming_convention"] + "_trimmed_demux_seqs.qzv",
        # outputdir + "Visualization_qzv/" + config["naming_convention"] + "_representative_sequences.qzv",
        # outputdir + "Visualization_qzv/" + config["naming_convention"] + "_table.qzv",
        # outputdir + "Visualization_qzv/" + config["naming_convention"] + "_denoising_stats.qzv",
        # outputdir + "Visualization_qzv/" + config["naming_convention"] + "_" + classifier_name + ".qzv",
        #
        # outputdir + "export/" + config["naming_convention"] + "_dna-sequences.fasta",
        # outputdir + "export/" + config["naming_convention"] + "_feature-table.biom",
        # outputdir + "export/" + config["naming_convention"] + "_tree.nwk",
        # outputdir + "export/" + config["naming_convention"] + "_taxonomy.tsv"

# New Steps
# rule unpack_and_get_manifest:
#     output:
#         manifest = config["inputdir"] + "input/pe-64-manifest",
#         metadata = config["inputdir"] + "input/metadata.txt"
#     shell:
#         "mkdir {config[inputdir]}input/raw_data;"
#         "mkdir {config[inputdir]}tempdir;"
#         "unzip {config[inputdir]}*.zip -d {config[inputdir]}tempdir;"
#         "mv {config[inputdir]}tempdir/*/demux/*.gz {config[inputdir]}input/raw_data;"
#         "echo \"#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tBarcodeName\tReversePrimer\tProjectName\tDescription\" > {config[inputdir]}input/metadata.txt;"
#         "cat {config[inputdir]}tempdir/*/*metadata* >> {config[inputdir]}input/metadata.txt;"
#         "rm -rf {config[inputdir]}tempdir;"
#         "python3 {config[tooldir]}wetsus_packages/convert_to_manifest.py --inputdir={config[inputdir]}input/raw_data --outputdir={outputdir}input/"
#         #"mv pe-64-manifest {config[inputdir]}input/"
#
# rule make_artifact:
#     input:
#         rules.unpack_and_get_manifest.output.manifest
#     output:
#         outputdir + config["naming_convention"] + "_demux.qza"
#     conda:
#         config["condaenvs"] + config["qiime_v2"]
#     shell:
#         "sbatch /export/jippe/jsil/programs/ITS/bash_scripts/first_steps/artifact.sh {input} {output};"
#         "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

# Old Steps

rule Import_data:
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_PairEndSequences.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        inputpath = config["inputdir"] + folder_name
    benchmark:
        outputdir + "benchmarks/Importing_data.txt"
    message:
        "@#"
        "Importing data:   "
        "qiime tools import "
        "   --type 'SampleData[PairedEndSequencesWithQuality]'"
        "    --input-path {params.inputpath}input/raw_data/ "
        "   --output-path {output} "
        "   --input-format PairedEndFastqManifestPhred33V2"
        "@#"
    shell:
        "if [ ! -f {output} ];"
        "then "
        "   mkdir {config[inputdir]}input/;"
        "   mkdir {config[inputdir]}input/raw_data;"
        "   mkdir {config[inputdir]}tempdir;"
        "   unzip {config[inputdir]}*.zip -d {config[inputdir]}tempdir;"
        "   mv {config[inputdir]}tempdir/*.txt {config[inputdir]}input/{config[naming_convention]}@metadata.txt;"
        "   mv {config[inputdir]}tempdir/*/*_R1_*.fastq.gz {config[inputdir]}input/raw_data/forward1.fastq.gz;"
        "   mv {config[inputdir]}tempdir/*/*_R2_*.fastq.gz {config[inputdir]}input/raw_data/reverse1.fastq.gz;"
        "   gunzip -d {config[inputdir]}input/raw_data/forward1.fastq.gz;"
        "   gunzip -d {config[inputdir]}input/raw_data/reverse1.fastq.gz;"
        "   cp config.yaml {config[inputdir]}output/;"
        "   python3 python_scripts/pre_demux.py --inputdir={config[inputdir]};"
        "   gzip -c {config[inputdir]}input/raw_data/forward.fastq > {config[inputdir]}input/raw_data/forward.fastq.gz;"
        "   gzip -c {config[inputdir]}input/raw_data/reverse.fastq > {config[inputdir]}input/raw_data/reverse.fastq.gz;"
        "   rm {config[inputdir]}input/raw_data/*.fastq;"
        "   rm -rf {config[inputdir]}tempdir;"
        "   sbatch bash_scripts/calc/import_data.sh {params.inputpath}input/raw_data/ {output};"
        "   python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"
        "fi"

rule Demultiplex:
    input:
        rules.Import_data.output
        # outputdir + "Artifacts_qza/" + config["naming_convention"] + "_PairEndSequences.qza"
    output:
        demux = outputdir + "Artifacts_qza/"  + config["naming_convention"] + "_demux.qza",
        untrimmed = outputdir + "Artifacts_qza/"  + config["naming_convention"] + "_untrimmed.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        # inputfile = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_PairEndSequences.qza",
        p_error_rate = 0,
        metadata =  config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt"
    benchmark:
        outputdir + "benchmarks/Demultiplexing.txt"
    message:
        "@#"
        "Demultiplexing:   "
        "qiime cutadapt demux-paired "
        "   --m-forward-barcodes-column BarcodeSequence "
        "   --m-forward-barcodes-file {params.metadata} "
        "   --i-seqs {input} "
        "   --p-error-rate {params.p_error_rate} "
        "   --o-per-sample-sequences {output.demux} "
        "   --o-untrimmed-sequences {output.untrimmed} "
        "   --verbose"
        "@#"
    shell:
        "sbatch bash_scripts/calc/demultiplex.sh {params.metadata} {input} {params.p_error_rate} {output.demux} {output.untrimmed};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.demux} {output.untrimmed}"


rule trim_paired:
    input:
        #rules.make_artifact.output
        rules.Demultiplex.output.demux
        # outputdir + config["naming_convention"] + "_demux.qza"
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_trimmed_demux_seqs.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        p_front_f = "GTGYCAGCMGCCGCGGTAA",
        p_front_r = "CCGYCAATTYMTTTRAGTTT"
    benchmark:
        outputdir + "benchmarks/Trim_paired.txt"
    message:
        "@#"
        "Trimming paired ends:   "
        "qiime cutadapt trim-paired "
        "   --i-demultiplexed-sequences {input} "
        "   --p-front-f {params.p_front_f} "
        "   --p-front-r {params.p_front_r} "
        "   --p-discard-untrimmed "
        "   --o-trimmed-sequences {output}"
        "@#"
    shell:
        "mkdir {outputdir}export/;"
        "sbatch bash_scripts/calc/trim_paired.sh {input} {params.p_front_f} {params.p_front_r} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"


rule trimmed_demux_summary:
    input:
        rules.trim_paired.output
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_trimmed_demux_seqs.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    benchmark:
        outputdir + "benchmarks/visualize_trimmed_demux.txt"
    message:
        "@#"
        "Trimmed demux summary:   "
        "qiime demux summarize "
        "   --i-data {input} "
        "   --o-visualization {output}"
        "@#"
    shell:
        "sbatch bash_scripts/vis/demux_summary.sh {input} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"


rule denoising_paired:
    input:
        rules.trim_paired.output
    output:
        representative = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_representative_sequences.qza",
        table = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_table.qza",
        denoising_stats = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_denoising_stats.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        p_trim_left = 5,
        p_trim_right = 5,
        p_trunc_len_f = 200,
        p_trunc_len_r = 190
        #threads = 8
    benchmark:
        outputdir + "benchmarks/denoising_paired.txt"
    message:
        "@#"
        "Denoising paired end:   "
        "qiime dada2 denoise-paired "
        "   --i-demultiplexed-seqs {input} "
        "   --p-trim-left-f {params.p_trim_left} "
        "   --p-trim-left-r {params.p_trim_right} "
        "   --p-trunc-len-f {params.p_trunc_len_f} "
        "   --p-trunc-len-r {params.p_trunc_len_r} "
        "   --o-table  {output.table} "
        "   --o-representative-sequences {output.representative} "
        "   --o-denoising-stats {output.denoising_stats} "
        "   --p-n-threads 16"
        "@#"
    shell:
        "sbatch bash_scripts/calc/denoise_paired.sh {input} {params.p_trim_left} {params.p_trim_right} {params.p_trunc_len_f} {params.p_trunc_len_r} {output.table} {output.representative} {output.denoising_stats};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.representative} {output.table} {output.denoising_stats};"

rule visualize_denoising_stats:
    input:
        rules.denoising_paired.output.denoising_stats
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_denoising_stats.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    benchmark:
        outputdir + "benchmarks/visualize_denoising_stats.txt"
    message:
        "@#"
        "Visualizing denoising stats:   "
        "qiime metadata tabulate "
        "   --m-input-file {input} "
        "   --o-visualization {output}"
        "@#"
    shell:
        "sbatch bash_scripts/vis/metadata_tab.sh {input} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule visualize_table:
    input:
        table = rules.denoising_paired.output.table
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_table.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        metadata = config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt"
    benchmark:
        outputdir + "benchmarks/visualize_table.txt"
    message:
        "@#"
        "Visualizing table:   "
        "qiime feature-table summarize "
        "   --i-table {input.table} "
        "   --m-sample-metadata-file {params.metadata} "
        "   --o-visualization {output}"
        "@#"
    shell:
        "sbatch bash_scripts/vis/feature_table_summary.sh {input.table} {params.metadata} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule visualize_representative_sequences:
    input:
        rules.denoising_paired.output.representative
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_representative_sequences.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    benchmark:
        outputdir + "benchmarks/visualize_representative_sequences.txt"
    message:
        "@#"
        "Visualizing representative sequences:   "
        "qiime feature-table tabulate-seqs "
        "   --i-data {input} "
        "   --o-visualization {output}"
        "@#"
    shell:
        "sbatch bash_scripts/vis/feature_table_tab.sh {input} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule mafft_alignment:
    input:
        rules.denoising_paired.output.representative
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_aligned-rep-seqs.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        threads = 16
    benchmark:
        outputdir + "benchmarks/Mafft_alignment.txt"
    message:
        "@#"
        "Multiple sequence alignment met Mafft:   "
        "qiime alignment mafft "
        "   --i-sequences {input} "
        "   --o-alignment {output} "
        "   --p-n-threads {params.threads} "
        "@#"
    shell:
        "sbatch bash_scripts/calc/mafft_alignment.sh {input} {output} {params.threads};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule masking_alignment:
    input:
        rules.mafft_alignment.output
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_masked_aligned-rep-seqs.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    benchmark:
        outputdir + "benchmarks/Masking_alignment.txt"
    message:
        "@#"
        "Masking MSA:   "
        "qiime alignment mask "
        "   --i-alignment {input} "
        "   --o-masked-alignment {output}"
        "@#"
    shell:
        "sbatch bash_scripts/calc/alignment_mask.sh {input} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule Phylogenetic_Fasttree:
    input:
        rules.masking_alignment.output
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_unrooted-tree.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        threads = 16
    benchmark:
        outputdir + "benchmarks/Phylogenetic_Fasttree.txt"
    message:
        "@#"
        "Making phylogenetic tree:   "
        "qiime phylogeny fasttree "
        "   --i-alignment {input} "
        "   --o-tree {output} "
        "   --p-n-threads {params.threads}"
        "@#"
    shell:
        "sbatch bash_scripts/calc/phylo_fasttree.sh {input} {output} {params.threads};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule midpoint_root:
    input:
        rules.Phylogenetic_Fasttree.output
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_rooted-tree.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    benchmark:
        outputdir + "benchmarks/midpoint_root.txt"
    message:
        "@#"
        "Determining midpoint:    "
        "qiime phylogeny midpoint-root "
        "   --i-tree {input} "
        "   --o-rooted-tree {output}"
        "@#"
    shell:
        "sbatch bash_scripts/calc/phylotree_midpoint.sh {input} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule classifying_reads:
    input:
        rules.denoising_paired.output.representative
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_" + classifier_name + ".qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        threads = 16,
        batch_size = 200
    benchmark:
        outputdir + "benchmarks/Classification.txt"
    message:
        "@#"
        "Classify reads:   "
        "qiime feature-classifier classify-sklearn "
        "   --i-classifier {config[classifier]} "
        "   --i-reads {input} "
        "   --o-classification {output} "
        "   --p-n-jobs {params.threads} "
        "   --p-reads-per-batch {params.batch_size}"
        "@#"
    shell:
        "sbatch bash_scripts/calc/classify_sklearn.sh {config[classifier]} {input} {output} {params.threads} {params.batch_size};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule visualize_classification:
    input:
        rules.classifying_reads.output
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_" + classifier_name + ".qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    benchmark:
        outputdir + "benchmarks/visualize_classification.txt"
    message:
        "@#"
        "Visualize classification:   "
        "qiime metadata tabulate "
        "   --m-input-file {input} "
        "   --o-visualization {output}"
        "@#"
    shell:
        "sbatch bash_scripts/vis/metadata_tab.sh {input} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"


rule export_representative:
    input:
        rules.denoising_paired.output.representative
    output:
        outputdir + "export/" + config["naming_convention"] + "_dna-sequences.fasta"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        first_output = outputdir +"export/dna-sequences.fasta"
    benchmark:
        outputdir + "benchmarks/export_representative.txt"
    message:
        "@#"
        "Exporting respresentative sequences:   "
        "qiime tools export "
        "   --input-path {input} "
        "   --output-path {outputdir}export/"
        "@#"
    shell:
        "sbatch bash_scripts/calc/export_files.sh {input} {outputdir}export/;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {params.first_output};"
        "mv {params.first_output} {output}"

rule export_table:
    input:
        rules.denoising_paired.output.table
    output:
         outputdir + "export/" + config["naming_convention"] + "_feature-table.biom"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        first_output = outputdir + "export/feature-table.biom"
    benchmark:
        outputdir + "benchmarks/export_table.txt"
    message:
        "@#"
        "Exporting table:   "
        "qiime tools export "
        "   --input-path {input} "
        "   --output-path {outputdir}export/"
        "@#"
    shell:
        "sbatch bash_scripts/calc/export_files.sh {input} {outputdir}export/;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {params.first_output};"
        "mv {params.first_output} {output}"

rule export_rooted_tree:
    input:
        rules.midpoint_root.output
    output:
        outputdir + "export/" + config["naming_convention"] + "_tree.nwk"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        first_output = outputdir + "export/tree.nwk"
    benchmark:
        outputdir + "benchmarks/export_rooted_tree.txt"
    message:
        "@#"
        "Exporting rooted tree:   "
        "qiime tools export "
        "   --input-path {input} "
        "   --output-path {outputdir}export/"
        "@#"
    shell:
        "sbatch bash_scripts/calc/export_files.sh {input} {outputdir}export/;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {params.first_output};"
        "mv {params.first_output} {output}"

rule export_classified:
    input:
        rules.classifying_reads.output
    output:
        outputdir + "export/" + config["naming_convention"] + "_taxonomy.tsv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        first_output = outputdir + "export/taxonomy.tsv"
    benchmark:
        outputdir + "benchmarks/export_classified.txt"
    message:
        "@#"
        "Exporting classifications:   "
        "qiime tools export "
        "   --input-path {input} "
        "   --output-path {outputdir}export/"
        "@#"
    shell:
        "sbatch bash_scripts/calc/export_files.sh {input} {outputdir}export/;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {params.first_output};"
        "mv {params.first_output} {output}"

rule make_reports:
    input:
        export_rooted_tree = rules.export_rooted_tree.output,
        export_representative = rules.export_representative.output,
        export_table = rules.export_table.output,
        export_classify = rules.export_classified.output,
        vis_trimmed = rules.trimmed_demux_summary.output,
        vis_repr = rules.visualize_representative_sequences.output,
        vis_table = rules.visualize_table.output,
        vis_denoise = rules.visualize_denoising_stats.output,
        vis_classify = rules.visualize_classification.output
    output:
        outputdir + "reports/Qiime_report.txt"
    shell:
        "mkdir {outputdir}slurm_output/;"
        "mv *.out {outputdir}slurm_output/;"
        "mv Pipeline_execution.txt {outputdir}reports/;"
        "python3 python_scripts/snakemake_report.py --inputdir={outputdir}"
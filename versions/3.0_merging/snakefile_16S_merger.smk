configfile: "config.yaml"

from os import listdir
from os.path import isfile, join
import os
import re
import argparse
import sys


folder_path = config["inputdir"]
# Retrieve directory names in the specified folder
directory_names = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name)) and name != "output" and name != "input"]
# print(directory_names)

# Get the classifier name
classifier_name = config["classifier"].split("/")[-1][:-4]

# Make the outputdir
outputdir = config["inputdir"] + "output/"

# directory_names = directory_names[0]

rule all:
    input:
        outputdir + "reports/" + config["naming_convention"] + ".zip"
        # config["inputdir"] + "output/Artifacts_qza/merged-rep-seqs.qza",
        # config["inputdir"] + "output/Artifacts_qza/merged_feature_table.qza"

rule Import_data:
    output:
        input1 = config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/" + config["naming_convention"] + "_PairEndSequences.qza",
        input2 = config["inputdir"] + "output/{dataset}_config.yaml"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        inputpath = config["inputdir"] + "{dataset}"
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
        "python3 {config[tooldir]}16S/versions/3.0_merging/python_scripts/pre_data.py {params.inputpath};"
        "mkdir {params.inputpath}/input/raw_data;"
        "mv {params.inputpath}/input/*.fastq {params.inputpath}/input/raw_data/;"
        "mv {params.inputpath}/*.txt {params.inputpath}/input/{config[naming_convention]}_{wildcards.dataset}@metadata.txt;"
        "python3 {config[tooldir]}16S/versions/3.0_merging/python_scripts/change_metadata.py {params.inputpath}/input/{config[naming_convention]}_{wildcards.dataset}@metadata.txt {config[quote]};"
        #"mv {params.inputpath}/*.txt {config[inputdir]}/{config[naming_convention]}@metadata.txt;"
        #"python3 {config[tooldir]}16S/versions/3.0_merging/python_scripts/change_metadata.py {params.inputpath}/{config[naming_convention]}@metadata.txt {config[quote]}"
        "cp config.yaml {params.inputpath}/output/;"
        "cp config.yaml {config[inputdir]}output/{wildcards.dataset}_config.yaml;"
        "python3 {config[tooldir]}16S/versions/3.0_merging/python_scripts/pre_demux.py --inputdir={params.inputpath}/;"
        "gzip -c {params.inputpath}/input/raw_data/forward.fastq > {params.inputpath}/input/raw_data/forward.fastq.gz;"
        "gzip -c {params.inputpath}/input/raw_data/reverse.fastq > {params.inputpath}/input/raw_data/reverse.fastq.gz;"
        "rm {params.inputpath}/input/raw_data/*.fastq;"
        # "mkdir {params.inputpath}/output/Artifacts_qza;"
        # "mkdir {outputdir}Artifacts_qza;"
        "sbatch bash_scripts/calc/import_data.sh {params.inputpath}/input/raw_data/ {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule Demultiplex:
    input:
        rules.Import_data.output.input1
        # outputdir + "Artifacts_qza/" + config["naming_convention"] + "_PairEndSequences.qza"
    output:
        demux = config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/"  + config["naming_convention"] + "_demux.qza",
        untrimmed = config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/"  + config["naming_convention"] + "_untrimmed.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        # inputfile = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_PairEndSequences.qza",
        p_error_rate = 0,
        metadata =  config["inputdir"] + "input/" + config["naming_convention"] + "_{dataset}@metadata.txt",
        inputpath = config["inputdir"] + "{dataset}",
        cores = 8
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
        "   --p-cores {params.cores}    "
        "   --verbose"
        "@#"
    shell:
        "sbatch bash_scripts/calc/demultiplex.sh {params.inputpath}/input/{config[naming_convention]}_{wildcards.dataset}@metadata.txt {input} {params.p_error_rate} {output.demux} {output.untrimmed} {params.cores};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.demux} {output.untrimmed}"


rule trim_paired:
    input:
        #rules.make_artifact.output
        rules.Demultiplex.output.demux
        # outputdir + config["naming_convention"] + "_demux.qza"
    output:
        config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/" + config["naming_convention"] + "_trimmed_demux_seqs.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        p_front_f = "GTGYCAGCMGCCGCGGTAA",
        p_front_r = "CCGYCAATTYMTTTRAGTTT",
        cores = 16
    message:
        "@#"
        "Trimming paired ends:   "
        "qiime cutadapt trim-paired "
        "   --i-demultiplexed-sequences {input} "
        "   --p-front-f {params.p_front_f} "
        "   --p-front-r {params.p_front_r} "
        "   --p-discard-untrimmed "
        "   --o-trimmed-sequences {output}  "
        "   --p-cores {params.cores}"
        "@#"
    shell:
        # "mkdir {outputdir}export/;"
        "sbatch bash_scripts/calc/trim_paired.sh {input} {params.p_front_f} {params.p_front_r} {output} {params.cores};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"


rule trimmed_demux_summary:
    input:
        rules.trim_paired.output
    output:
        config["inputdir"] + "{dataset}/output/" + "Visualization_qzv/" + config["naming_convention"] + "_trimmed_demux_seqs.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
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
        representative = config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/" + config["naming_convention"] + "_representative_sequences.qza",
        table = config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/" + config["naming_convention"] + "_table.qza",
        denoising_stats = config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/" + config["naming_convention"] + "_denoising_stats.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        p_trim_left = 5,
        p_trim_right = 5,
        p_trunc_len_f = 200,
        p_trunc_len_r = 190
        #threads = 8
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

### make merged visualization and unmerged visualization look at metadata changes.

rule visualize_denoising_stats:
    input:
        rules.denoising_paired.output.denoising_stats
    output:
        config["inputdir"] + "{dataset}/output/" + "Visualization_qzv/" + config["naming_convention"] + "_denoising_stats.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
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
        config["inputdir"] + "{dataset}/output/" + "Visualization_qzv/" + config["naming_convention"] + "_table.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        metadata =  config["inputdir"] + "{dataset}/input/" + config["naming_convention"]+ "_{dataset}@metadata.txt"
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
        config["inputdir"] + "{dataset}/output/" + "Visualization_qzv/" + config["naming_convention"] + "_representative_sequences.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
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

rule merge_feature_tables:
    input:
        expand(config["inputdir"] + "{dataset}/output/Artifacts_qza/" + config["naming_convention"] + "_representative_sequences.qza", dataset=directory_names),
        expand(config["inputdir"] + "{dataset}/output/Artifacts_qza/" + config["naming_convention"] + "_table.qza", dataset=directory_names),
        expand(config["inputdir"] + "{dataset}/output/Artifacts_qza/" + config["naming_convention"] + "_denoising_stats.qza", dataset=directory_names)
    output:
        config["inputdir"] + "output/Artifacts_qza/merged_feature_table.qza"
    params:
        name = "/output/Artifacts_qza/" + config["naming_convention"] + "_table.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    shell:
        "python3 /export/jippe/jsil/programs/16S/versions/3.0_merging/python_scripts/merge_change.py {directory_names} --input_file=bash_scripts/calc/merge_table.sh --inputdir={config[inputdir]} --name={params.name};"
        "sbatch bash_scripts/calc/merge_table.sh {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

# rule merge_taxa:
#     input:
#         rules.merge_feature_tables.output
#     output:
#         config["inputdir"] + "output/Artifacts_qza/merged-silva-taxonomy.qza"
#     params:
#         name = "/output/Artifacts_qza/" + config["naming_convention"] + "_table.qza"
#     shell:
#         "python3 /export/jippe/jsil/programs/16S/versions/3.0_merging/python_scripts/merge_change.py --i {directory_names} --input_file bash_scripts/calc/merge_tax.sh;"
#         "sbatch bash_scripts/vis/merge_tax.sh {input} {output};"
#         "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule merge_seq:
    input:
        rules.merge_feature_tables.output
    output:
        config["inputdir"] + "output/Artifacts_qza/merged-rep-seqs.qza"
    params:
        name = "/output/Artifacts_qza/" + config["naming_convention"] + "_representative_sequences.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    shell:
        "python3 /export/jippe/jsil/programs/16S/versions/3.0_merging/python_scripts/merge_change.py {directory_names} --input_file=bash_scripts/calc/merge_seq.sh --inputdir={config[inputdir]} --name={params.name};"
        "sbatch bash_scripts/calc/merge_seq.sh {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

rule mafft_alignment:
    input:
        rules.merge_seq.output
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
        rules.merge_seq.output
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_" + classifier_name + ".qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        threads = 8,
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
        rules.merge_seq.output
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
        "sbatch bash_scripts/calc/export_repr.sh {input} {outputdir}export/;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {params.first_output};"
        "mv {params.first_output} {output}"

rule export_table:
    input:
        rules.merge_feature_tables.output
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
        "sbatch bash_scripts/calc/export_table.sh {input} {outputdir}export/;"
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
        "sbatch bash_scripts/calc/export_rooted_tree.sh {input} {outputdir}export/;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {params.first_output};"
        "mv {params.first_output} {output}"

rule export_classified:
    input:
        rules.classifying_reads.output
    output:
        outputdir + "export/" + config["naming_convention"] + "_taxonomy.tsv"
    params:
        first_output = outputdir + "export/taxonomy.tsv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    benchmark:
        outputdir + "benchmarks/export_classified.txt"
    message:
        "@#"
        "Exporting classifications: "
        "qiime tools export "
        "   --input-path {input} "
        "   --output-path {outputdir}export/"
        "@#"
    shell:
        "sbatch bash_scripts/calc/export_classify.sh {input} {outputdir}export/;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {params.first_output};"
        "mv {params.first_output} {output}"



rule visualize_merge_table:
    input:
        table = rules.merge_feature_tables.output
    output:
        table_qzv = config["inputdir"] + "output/" + "Visualization_qzv/" + config["naming_convention"] + "_table.qzv",
        metadata = config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        metadata=config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt",
    message:
        "@#"
        "Visualizing table:   "
        "qiime feature-table summarize "
        "   --i-table {input.table} "
        "   --m-sample-metadata-file {params.metadata} "
        "   --o-visualization {output}"
        "@#"
    shell:
        "mv {config[inputdir]}*.txt {config[inputdir]}input/{config[naming_convention]}@metadata.txt;"
        "python3 {config[tooldir]}16S/versions/3.0_merging/python_scripts/change_metadata.py {config[inputdir]}input/{config[naming_convention]}@metadata.txt {config[quote]};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.metadata};"
        "sbatch bash_scripts/vis/feature_table_summary.sh {input.table} {params.metadata} {output.table_qzv};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.table_qzv};"


rule alpha_rarefaction:
    input:
        rooted_tree = rules.midpoint_root.output,
        table_denoise = rules.merge_feature_tables.output,
        make_metadata = rules.visualize_merge_table.output.metadata
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_alpha-rarefaction.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        max_depth = 60000,
        metadata = config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt"
    benchmark:
        outputdir + "benchmarks/alpha_rarefaction.txt"
    message:
        "@#"
        "Retrieving_alpha_rarefaction:  "
        "qiime diversity alpha-rarefaction  "
        "   --i-table {input.table_denoise} "
        "   --i-phylogeny {input.rooted_tree} "
        "   --p-max-depth {params.max_depth} "
        "   --m-metadata-file {params.metadata} "
        "   --o-visualization {output}"
        "@#"
    shell:
        # "mv {config[inputdir]}*.txt {config[inputdir]}input/{config[naming_convention]}@metadata.txt;"
        # "python3 {config[tooldir]}16S/versions/3.0_merging/python_scripts/change_metadata.py {params.metadata} {config[quote]}"
        "qiime diversity alpha-rarefaction --i-table {input.table_denoise} --i-phylogeny {input.rooted_tree} --p-max-depth {params.max_depth} --m-metadata-file {input.make_metadata} --o-visualization {output};"
        # "sbatch bash_scripts/vis/Alpha_rarefaction.sh {input.table_denoise} {input.rooted_tree} {params.max_depth} {params.metadata} {output};"
        # "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"


rule Taxonomy_analysis:
    input:
        metadata = rules.visualize_merge_table.output.metadata,
        taxa = rules.classifying_reads.output,
        table = rules.merge_feature_tables.output
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_taxonomy_barplot.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    message:
        "@#"
        "qiime taxa barplot "
        "   --i-table {input.table} "
        "   --i-taxonomy {input.taxa}   "
        "   --m-metadata-file {params.metadata} "
        "   --o-visualization {output}"
        "@#"
    params:
        metadata=config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt"
    shell:
        "sbatch bash_scripts/vis/taxonomy_barplot.sh {input.table} {input.taxa} {input.metadata} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"

rule visualize_merge_representative_sequences:
    input:
        rules.merge_seq.output
    output:
        config["inputdir"] + "output/" + "Visualization_qzv/" + config["naming_convention"] + "_representative_sequences.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
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

rule return_zipped_results:
    input:
        table = rules.merge_feature_tables.output,
        representative = rules.merge_seq.output,
        rooted = rules.midpoint_root.output,
        taxonomy = rules.classifying_reads.output,
        alpha = rules.alpha_rarefaction.output,

        trim_demux = expand(config["inputdir"] + "{dataset}/output/" + "Artifacts_qza/" + config["naming_convention"] + "_trimmed_demux_seqs.qza", dataset=directory_names),

        export_rooted_tree= rules.export_rooted_tree.output,
        export_representative= rules.export_representative.output,
        export_table= rules.export_table.output,
        export_classify= rules.export_classified.output,
        taxonomy_analysis= rules.Taxonomy_analysis.output,

        vis_trimmed= expand(config["inputdir"] + "{dataset}/output/" + "Visualization_qzv/" + config["naming_convention"] + "_trimmed_demux_seqs.qzv", dataset=directory_names),
        vis_denoise= expand(config["inputdir"] + "{dataset}/output/Visualization_qzv/" + config["naming_convention"] + "_denoising_stats.qzv",dataset=directory_names),
        vis_representative_single=expand(config["inputdir"] + "{dataset}/output/Visualization_qzv/" + config["naming_convention"] + "_representative_sequences.qzv", dataset=directory_names),
        vis_table_single=expand(config["inputdir"] + "{dataset}/output/Visualization_qzv/" + config["naming_convention"] + "_table.qzv", dataset=directory_names),

        vis_repr= rules.visualize_merge_representative_sequences.output,
        vis_table= rules.visualize_merge_table.output,
        vis_classify= rules.visualize_classification.output
    output:
        outputdir + "reports/"+ config["naming_convention"] + ".zip"
    params:
        metadata = config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt",
        zip_folder = outputdir + "reports/"+ config["naming_convention"]
    conda:
        config["condaenvs"] + config["qiime_v2"]
    shell:
        "mkdir {params.zip_folder};"
        # "mkdir {outputdir}export/;"
        "cp {input.table} {params.zip_folder};"
        "cp {input.representative} {params.zip_folder};"
        "cp {input.rooted} {params.zip_folder};"
        "cp {input.taxonomy} {params.zip_folder};"
        "cp {input.alpha} {params.zip_folder};"
        "cp {params.metadata} {params.zip_folder};"
        # "cp {input.vis_denoise} {params.zip_folder};"
        # "cp {input.trim_demux} {params.zip_folder};"
        "mkdir {outputdir}slurm_output/;"
        "mv *.out {outputdir}slurm_output/;"
        "mv Pipeline_execution.txt {outputdir}reports/;"
        "python3 python_scripts/snakemake_report.py --inputdir={outputdir};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {outputdir}reports/Qiime_report.txt;"
        "cp {outputdir}reports/Qiime_report.txt {params.zip_folder};"
        "zip -r {output} {params.zip_folder};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"


# rule make_reports:
#     output:
#         report = outputdir + "reports/pipeline_flow.svg"
#     conda:
#         config["condaenvs"] + "R.yaml"
#     shell:
#         "Rscript r_scripts/Visualize_time.R {params.input_file} {output.time}"

# rule make_reports:
#     input:
#         zipped = rules.return_zipped_results.output
#     output:
#         report = outputdir + "reports/Qiime_report.txt",
#         # time = outputdir + "reports/time.png"
#     params:
#         input_file = outputdir + "reports/time.csv"
#     conda:
#         config["condaenvs"] + "R.yaml"
#     shell:
#         "Rscript r_scripts/Visualize_time.R {params.input_file} {output.time}"

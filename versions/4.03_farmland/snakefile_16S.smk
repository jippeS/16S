configfile: "config.yaml"

from os import listdir
from os.path import isfile, join
import os
import re
import argparse
import sys
from python_scripts.rename_files import FastqRenamer

def list_files_in_folder(folder_path):
    list_1 = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and not f.endswith(".txt") and not f.endswith(".sh")]
    return_list = set()
    for i in list_1:
        if i != "folder.sh":
            i = i.replace("_2.fastq.gz","")
            i = i.replace("_1.fastq.gz","")
            return_list.add(i)
    return list(return_list)


def create_metadata(inputdir, forward, reverse):
    # collect unique sample IDs from filenames (remove _1/_2)
    samples = sorted({
        re.sub(r'_[12]$', '', f.split(".")[0])
        for f in os.listdir(inputdir)
        if f.endswith((".fastq", ".fastq.gz"))
    })

    with open(os.path.join(inputdir, "metadata.txt"), "w") as out:
        out.write("#SampleID\tForward Primer\tReverse Primer\tDescription\n")
        for sample in samples:
            out.write(f"{sample}\t{forward}\t{reverse}\t{sample}\n")


inputdir = config["inputdir"]
forward = config["forward"]
reverse = config["reverse"]


renamer = FastqRenamer(
    inputdir=inputdir,
    metadata_file=inputdir + "meta_data.txt",
    dry_run=False
)

renamer.run()

folder_path = config["inputdir"]
create_metadata(inputdir, forward, reverse)
files_list = list_files_in_folder(folder_path)


# config["naming_convention"] = config["naming_convention"] + "_" + config["forw"] + "_" + config["reve"]

files_list = list_files_in_folder(folder_path)

# Make the outputdir
outputdir = config["inputdir"] + "output/"

classifier_name = config["classifier"].split("/")[-1][:-4]
rule all:
    input:
        outputdir + "reports/" + config["naming_convention"] + ".zip"
        # outputdir + "Visualization_qzv/" + config["naming_convention"] + "_denoising_stats.qzv",
        # outputdir + "Visualization_qzv/" + config["naming_convention"] + "_representative_sequences.qzv"
        # expand(startdir + "input/start_data/{dataset}_1.fastq.gz", dataset=files_list),
        # expand(startdir + "input/start_data/{dataset}_2.fastq.gz", dataset=files_list)


rule unpack_and_get_manifest:
    output:
        manifest = config["inputdir"] + "input/pe-64-manifest.csv",
        metadata = config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt"
    benchmark:
        outputdir + "benchmarks/pe-64-manifest.csv"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
    message:
        "@#"
        "Getting a manifest file start"
        "@#"
    shell:
        "cp {config[inputdir]}*metadata* {config[inputdir]}input/{config[naming_convention]}@metadata.txt;"
        "echo 'sample-id,absolute-filepath,direction' > {output.manifest}"


rule pre_demux:
    input:
        manifest = rules.unpack_and_get_manifest.output.manifest,
        fw = config["inputdir"] + "{dataset}_1.fastq.gz",
        rv = config["inputdir"] + "{dataset}_2.fastq.gz"
    output:
        fw= config["inputdir"] + "input/raw_data/{dataset}_1.fastq.gz",
        rv= config["inputdir"] + "input/raw_data/{dataset}_2.fastq.gz"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
    params:
        id = "{dataset}",
        manifest = config["inputdir"] + "input/pe-64-manifest.csv"
    message:
        "@#"
        "Creating manifest"
        "@#"
    shell:
        # "python3 python_scripts/pre_demux.py --forward={input.fw} --forward_out={output.fw} --reverse={input.rv} --reverse_out={output.rv} --config=config.yaml;"
        # "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.fw} {output.rv}  --seconds=40;"
        "cp {input.fw} {output.fw};"
        "cp {input.rv} {output.rv};"
        "echo '{params.id},{output.fw},forward' >> {params.manifest};"
        "echo '{params.id},{output.rv},reverse' >> {params.manifest};"


rule Demultiplex:
    input:
        fw = expand(config["inputdir"] + "input/raw_data/{dataset}_1.fastq.gz", dataset=files_list),
        rv = expand(config["inputdir"] + "input/raw_data/{dataset}_2.fastq.gz", dataset=files_list),
        manifest = rules.unpack_and_get_manifest.output.manifest
    output:
        demux = outputdir + "Artifacts_qza/"  + config["naming_convention"] + "_demux.qza",
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
    benchmark:
        outputdir + "benchmarks/Demux_artifact_generation.txt"
    message:
        "@#"
        "Trimming paired ends:"
        "qiime tools import      "
        "   --type 'SampleData[PairedEndSequencesWithQuality]' "
        "   --input-path {input}"
        "   --output-path {output}"
        "   --input-format PairedEndFastqManifestPhred33V2"
        "@#"
    shell:
        "cp {config[inputdir]}*metadata* {config[inputdir]}input/{config[naming_convention]}@metadata.txt;"
        "sbatch bash_scripts/extra/artifact.sh {input.manifest} {output.demux};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.demux};"



rule trim_paired:
    input:
        #rules.make_artifact.output
        rules.Demultiplex.output.demux
        # outputdir + config["naming_convention"] + "_demux.qza"
    output:
        outputdir + "Artifacts_qza/" + config["naming_convention"] + "_trimmed_demux_seqs.qza"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
    params:
        p_front_f = config["forward"],
        p_front_r = config["reverse"],
        cores = 16
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
        "   --o-trimmed-sequences {output}  "
        "   --p-cores {params.cores}"
        "@#"
    shell:
        "mkdir {outputdir}export/;"
        "sbatch bash_scripts/calc/trim_paired.sh {input} {params.p_front_f} {params.p_front_r} {output} {params.cores};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"


rule trimmed_demux_summary:
    input:
        rules.Demultiplex.output
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_trimmed_demux_seqs.qzv"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
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
        rules.Demultiplex.output,
    output:
        representative = outputdir + "Artifacts_qza/denoise/" + str(config["forw"]) + "_" + str(config["reve"]) + "_representative_sequences.qza",
        table = outputdir + "Artifacts_qza/denoise/" + str(config["forw"]) + "_" + str(config["reve"]) + "_table.qza",
        denoising_stats = outputdir + "Artifacts_qza/denoise/" + str(config["forw"]) + "_" + str(config["reve"]) + "_denoising_stats.qza"
        # representative = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_representative_sequences.qza",
        # table = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_table.qza",
        # denoising_stats = outputdir + "Artifacts_qza/" + config["naming_convention"] + "_denoising_stats.qza"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
    params:
        p_trim_left = 5,
        p_trim_right = 5,
        p_trunc_len_f = config["forw"],
        p_trunc_len_r = config["reve"]
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
        "   --p-n-threads 8"
        "@#"
    shell:
        # "sbatch bash_scripts/calc/denoise_paired.sh {input} {params.p_trim_left} {params.p_trim_right} {params.p_trunc_len_f} {params.p_trunc_len_r} {output.table} {output.representative} {output.denoising_stats};"
        "qiime dada2 denoise-paired --i-demultiplexed-seqs {input} --p-trim-left-f {params.p_trim_left} --p-trim-left-r {params.p_trim_right} --p-trunc-len-f {params.p_trunc_len_f} --p-trunc-len-r {params.p_trunc_len_r} --o-table  {output.table} --o-representative-sequences {output.representative}  --o-denoising-stats {output.denoising_stats} --p-n-threads 8;"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.representative} {output.table} {output.denoising_stats};"
        "sleep 11000;"

rule visualize_denoising_stats:
    input:
        rules.denoising_paired.output.denoising_stats
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_denoising_stats.qzv"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        rules.denoising_paired.output.table
    output:
         outputdir + "export/" + config["naming_convention"] + "_feature-table.biom"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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
        "env/qiime2-amplicon-2024.10.yaml"
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

rule alpha_rarefaction:
    input:
        rooted_tree = rules.midpoint_root.output,
        table_denoise = rules.denoising_paired.output.table
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_alpha-rarefaction.qzv"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
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
        "qiime diversity alpha-rarefaction --i-table {input.table_denoise} --i-phylogeny {input.rooted_tree} --p-max-depth {params.max_depth} --m-metadata-file {params.metadata} --o-visualization {output};"
        # "sbatch bash_scripts/vis/Alpha_rarefaction.sh {input.table_denoise} {input.rooted_tree} {params.max_depth} {params.metadata} {output};"
        # "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"


rule Taxonomy_analysis:
    input:
        taxa = rules.classifying_reads.output,
        table = rules.denoising_paired.output.table
    output:
        outputdir + "Visualization_qzv/" + config["naming_convention"] + "_taxonomy_barplot.qzv"
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
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
        "sbatch bash_scripts/vis/taxonomy_barplot.sh {input.table} {input.taxa} {params.metadata} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"

rule return_zipped_results:
    input:
        table = rules.denoising_paired.output.table,
        representative = rules.denoising_paired.output.representative,
        rooted = rules.midpoint_root.output,
        taxonomy = rules.classifying_reads.output,
        alpha = rules.alpha_rarefaction.output,
        vis_denoise = rules.visualize_denoising_stats.output,
        # trim_demux = rules.trim_paired.output,

        export_rooted_tree= rules.export_rooted_tree.output,
        export_representative= rules.export_representative.output,
        export_table= rules.export_table.output,
        export_classify= rules.export_classified.output,
        # vis_trimmed= rules.trimmed_demux_summary.output,
        vis_repr= rules.visualize_representative_sequences.output,
        vis_table= rules.visualize_table.output,
        vis_classify= rules.visualize_classification.output,
        taxonomy_analysis= rules.Taxonomy_analysis.output,

    output:
        outputdir + "reports/"+ config["naming_convention"] + ".zip"
    params:
        metadata = config["inputdir"] + "input/" + config["naming_convention"] + "@metadata.txt",
        zip_folder = outputdir + "reports/"+ config["naming_convention"]
    conda:
        "env/qiime2-amplicon-2024.10.yaml"
    shell:
        "mkdir {params.zip_folder};"
        "cp {input.table} {params.zip_folder};"
        "cp {input.representative} {params.zip_folder};"
        "cp {input.rooted} {params.zip_folder};"
        "cp {input.taxonomy} {params.zip_folder};"
        "cp {input.alpha} {params.zip_folder};"
        "cp {params.metadata} {params.zip_folder};"
        "cp {input.vis_denoise} {params.zip_folder};"
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

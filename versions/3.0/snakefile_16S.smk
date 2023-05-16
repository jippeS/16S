configfile: "config.yaml"

from os import listdir
from os.path import isfile, join
import os
import re
import argparse
import sys


rule all:
    input:
        config["outputdir"] + config["naming_convention"] + "_trimmed_demux_seqs.qza",
        config["outputdir"] + config["naming_convention"] + "_trimmed_demux_seqs.qzv"
        # config["outputdir"] + config["naming_convention"] + "_trimmed_demux_seqs.qza"
        # config["outputdir"] + config["naming_convention"] + "_representative_sequences.qza",
        # config["outputdir"] + config["naming_convention"] + "_table.qza",
        # config["outputdir"] + config["naming_convention"] + "_denoising_stats.qza"

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
#         "python3 {config[tooldir]}wetsus_packages/convert_to_manifest.py --inputdir={config[inputdir]}input/raw_data --outputdir={config[inputdir]}input/"
#         #"mv pe-64-manifest {config[inputdir]}input/"
#
# rule make_artifact:
#     input:
#         rules.unpack_and_get_manifest.output.manifest
#     output:
#         config["outputdir"] + config["naming_convention"] + "_demux.qza"
#     conda:
#         config["condaenvs"] + config["qiime_v2"]
#     shell:
#         "sbatch /export/jippe/jsil/programs/ITS/bash_scripts/first_steps/artifact.sh {input} {output};"
#         "python3 {config[tooldir]}wetsus_packages/wait_file.py {output};"

# Old Steps
rule Import_data:
    output:
        config["inputdir"]+"output/PairEndSequences.qza"
    conda:
        config["condaenvs"] + config["qiime_v"]
    shell:
        "qiime tools import"
        "   --type MultiplexedPairedEndBarcodeInSequence"
        "   --input-path {config[inputdir]}input/raw_data/"
        "   --output-path {output}"

rule Demultiplex:
    input:
        rules.Import_data.output
    output:
        demux = config["inputdir"]+"output/demux.qza",
        untrimmed = config["inputdir"]+"output/untrimmed.qza"
    conda:
        config["condaenvs"] + config["qiime_v"]
    shell:
        "qiime cutadapt demux-paired"
        "   --m-forward-barcodes-column BarcodeSequence"
        "   --m-forward-barcodes-file {config[inputdir]}input/*@metadata.txt"
        "   --i-seqs {input}"
        "   --p-error-rate 0"
        "   --o-per-sample-sequences {output.demux}"
        "   --o-untrimmed-sequences {output.untrimmed}"
        "   --verbose"


rule trim_paired:
    input:
        rules.make_artifact.output
    output:
        config["outputdir"] + config["naming_convention"] + "_trimmed_demux_seqs.qza"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    params:
        p_front_f = "GTGYCAGCMGCCGCGGTAA",
        p_front_r = "CCGYCAATTYMTTTRAGTTT"
    shell:
        "sbatch bash_scripts/calc/trim_paired.sh {input} {params.p_front_f} {params.p_front_r} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"


rule trimmed_demux_summary:
    input:
        rules.make_artifact.output
    output:
        config["outputdir"] + config["naming_convention"] + "_trimmed_demux_seqs.qzv"
    conda:
        config["condaenvs"] + config["qiime_v2"]
    shell:
        "sbatch bash_scripts/vis/demux_summary.sh {input} {output};"
        "python3 {config[tooldir]}wetsus_packages/wait_file.py {output}"


    # rule denoising_paired:
#     input:
#         rules.make_artifact.output
#     output:
#         representative = config["outputdir"] + config["naming_convention"] + "_representative_sequences.qza",
#         table = config["outputdir"] + config["naming_convention"] + "_table.qza",
#         denoising_stats = config["outputdir"] + config["naming_convention"] + "_denoising_stats.qza"
#     conda:
#         config["condaenvs"] + config["qiime_v2"]
#
#     params:
#         p_trim_left = 5,
#         p_trim_right = 5,
#         p_trunc_len_f = 200,
#         p_trunc_len_r = 190
#         #threads = 8
#
#     shell:
#         "sbatch bash_scripts/calc/denoise_paired.sh {input} {params.p_trim_left} {params.p_trim_right} {params.p_trunc_len_f} {params.p_trunc_len_r} {output.table} {output.representative} {output.denoising_stats};"
#         "python3 {config[tooldir]}wetsus_packages/wait_file.py {output.representative} {output.table} {output.denoising_stats};"

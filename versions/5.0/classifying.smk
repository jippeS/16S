rule classifying_reads:
    input:
        rules.denoising_paired.output.representative
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
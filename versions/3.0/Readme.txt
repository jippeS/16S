Usage:
  if you want to execute the pipeline from current terminal use:
  snakemake --snakefile snakefile_16S.smk -c 16 --latency-wait 30 -j --use-conda > Pipeline_execution.txt
  
  If you want to use it from sbatch use:
  sbatch Remote_pipeline.sh
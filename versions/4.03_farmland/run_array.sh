#!/bin/bash

START=200
END=300
STEP=10

# build parameter list
params=()
for forw in $(seq $START $STEP $END); do
  for reve in $(seq $START $STEP $END); do
    params+=("${forw}_${reve}")
  done
done

pair=${params[$SLURM_ARRAY_TASK_ID]}
forw=${pair%_*}
reve=${pair#*_}

snakemake -s snakefile_16S.smk denoising_paired \
  --cores 1 \
  --config forw=$forw reve=$reve --force

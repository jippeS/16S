#!/bin/bash
# =====================================
# submit_all_combinations.sh
# =====================================
# Submits Snakemake jobs for all combinations of 190–280 (step 10)
# Skips any where output folder already exists with contents
# =====================================

BASE_DIR="/export/projects/16S/Macrogen_bkis_versions"
START=190
END=280
STEP=10

# Optional: directory for logs
mkdir -p logs

for forw in $(seq $START $STEP $END); do
  for reve in $(seq $START $STEP $END); do
    FOLDER="${BASE_DIR}/${forw}_${reve}"
    OUTPUT_DIR="${FOLDER}/output/export/"

    # Check if the output folder exists and has content
    if [ -d "$OUTPUT_DIR" ] && [ "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]; then
      echo "Skipping $forw $reve — output already exists."
    else
      echo "Submitting job for $forw_$reve"
      sbatch \
        --job-name="${forw}_${reve}" \
        Remote_pipeline.sh "$forw" "$reve"
    fi
  done
done

#!/bin/bash
# =====================================
# submit_all_combinations.sh
# =====================================
# Submits Snakemake jobs for all combinations of 190–280 (step 10)
# Skips any where output folder already exists with contents
# =====================================

BASE_DIR="/export/projects/Other/BSPE/input_data/farmland_data_bioclear/Bac/analysis_test_fw_rv"
START=180
END=240
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
        Remote_pipeline.sh "$forw" "$reve" "$OUTPUT_DIR"
    fi
  done
done

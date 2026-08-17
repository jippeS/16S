#!/bin/bash

START=230
END=300
STEP=10
MAX_PARALLEL=1

mkdir -p logs

jobs=()

for forw in $(seq $START $STEP $END); do
  for reve in $(seq $START $STEP $END); do
    jobs+=("$forw,$reve")
  done
done

echo "Total jobs: ${#jobs[@]}"

running=0

for job in "${jobs[@]}"; do
  IFS=',' read -r forw reve <<< "$job"

  OUTPUT_DIR="/export/projects/Other/BSPE/input_data/farmland_data_bioclear/Arc/Arc2/output/Artifacts_qza/denoise"
  TABLE="${OUTPUT_DIR}/${forw}_${reve}_table.qza"

  # =========================
  # SKIP IF EXISTS
  # =========================
  if [[ -f "$TABLE" ]]; then
    echo "Skipping ${forw}_${reve} — already done"
    continue
  fi

  sbatch \
    --job-name="${forw}_${reve}" \
    --output="logs/${forw}_${reve}.out" \
    --error="logs/${forw}_${reve}.err" \
    --cpus-per-task=16 \
    --nodelist=cn2 \
    --wrap="qiime dada2 denoise-paired \
      --i-demultiplexed-seqs /export/projects/Other/BSPE/input_data/farmland_data_bioclear/Arc/Arc2/output/Artifacts_qza/BSPE_26_03_2026_Arc_demux.qza \
      --p-trim-left-f 5 \
      --p-trim-left-r 5 \
      --p-trunc-len-f ${forw} \
      --p-trunc-len-r ${reve} \
      --o-table ${OUTPUT_DIR}/${forw}_${reve}_table.qza \
      --o-representative-sequences ${OUTPUT_DIR}/${forw}_${reve}_rep_seqs.qza \
      --o-denoising-stats ${OUTPUT_DIR}/${forw}_${reve}_stats.qza \
      --p-n-threads 16"

  ((running++))

  if (( running >= MAX_PARALLEL )); then
    wait -n
    ((running--))
  fi
done

wait

echo "All jobs submitted"

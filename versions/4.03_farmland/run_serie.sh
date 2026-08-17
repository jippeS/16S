#!/bin/bash
#SBATCH --job-name=dada2_grid
#SBATCH --output=logs/dada2_grid.out
#SBATCH --error=logs/dada2_grid.err
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=cn2
#SBATCH --time=48:00:00

START=230
END=300
STEP=10

mkdir -p logs

OUTPUT_DIR="/export/projects/Other/BSPE/input_data/farmland_data_bioclear/Arc/Arc2/output/Artifacts_qza/denoise"
INPUT_QZA="/export/projects/Other/BSPE/input_data/farmland_data_bioclear/Arc/Arc2/output/Artifacts_qza/BSPE_26_03_2026_Arc_demux.qza"

for forw in $(seq $START $STEP $END); do
  for reve in $(seq $START $STEP $END); do

    TABLE="${OUTPUT_DIR}/${forw}_${reve}_table.qza"

    # =========================
    # SKIP IF EXISTS
    # =========================
    if [[ -f "$TABLE" ]]; then
      echo "Skipping ${forw}_${reve} — already done"
      continue
    fi

    echo "Running ${forw}_${reve}"

    qiime dada2 denoise-paired \
      --i-demultiplexed-seqs "$INPUT_QZA" \
      --p-trim-left-f 5 \
      --p-trim-left-r 5 \
      --p-trunc-len-f "${forw}" \
      --p-trunc-len-r "${reve}" \
      --o-table "${OUTPUT_DIR}/${forw}_${reve}_table.qza" \
      --o-representative-sequences "${OUTPUT_DIR}/${forw}_${reve}_rep_seqs.qza" \
      --o-denoising-stats "${OUTPUT_DIR}/${forw}_${reve}_stats.qza" \
      --p-n-threads 16

    echo "Finished ${forw}_${reve}"

  done
done

echo "All jobs completed"

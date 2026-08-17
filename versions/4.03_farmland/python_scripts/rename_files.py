#!/usr/bin/env python3

import os
import argparse
import pandas as pd


class FastqRenamer:
    def __init__(self, inputdir, metadata_file, dry_run=False):
        self.inputdir = inputdir
        self.metadata_file = metadata_file
        self.dry_run = dry_run
        self.metadata_df = None

    def load_metadata(self):
        # Load metadata into DataFrame
        self.metadata_df = pd.read_csv(
            self.metadata_file,
            sep="\t",
            comment="#"
        )

        # Strip column names (in case of trailing spaces)
        self.metadata_df.columns = self.metadata_df.columns.str.strip()

        print(f"Loaded {len(self.metadata_df)} metadata rows")

    def build_sample_id(self, parts):
        # "S" + splitted[1] + "P" + splitted[0]
        # Ensure parts[1] is always 3 digits
        part1_padded = parts[1].zfill(3)
        return f"S{part1_padded}P{parts[0]}"

    def find_metadata_row(self, sample_id):
        row = self.metadata_df[self.metadata_df["Samples"] == sample_id]
        if row.empty:
            return None
        return row.iloc[0]

    def build_new_name(self, parts, metadata_row):
        # Extract needed parts
        sample_id = metadata_row["Samples"]
        sample_name = metadata_row["Sample name"]
        replicate = str(metadata_row["Replicate"]).strip()

        # Clean sample name (KV 1.1 → KV_1)
        sample_name_clean = sample_name.replace(" ", "_").split(".")[0]
        # From filename
        part3 = parts[3]  # DNA
        part4 = parts[4]  # Fun
        part5 = parts[-2][-1]
        read = parts[-1].replace("_", ".")  # 1.fastq.gz or 2.fastq.gz
        read = read.split('.', 1)[1]
        file = f"{sample_id}_{sample_name_clean}_{replicate}_{part3}_{part4}_{part5}.{read}"
        return file

    def rename_files(self):
        for filename in os.listdir(self.inputdir):

            if not filename.endswith(".fastq.gz"):
                continue

            old_path = os.path.join(self.inputdir, filename)

            parts = filename.split("_")

            # Safety check
            if len(parts) < 6:
                print(f"Skipping malformed: {filename}")
                continue

            sample_id = self.build_sample_id(parts)

            metadata_row = self.find_metadata_row(sample_id)
            if metadata_row is None:
                print(f"No metadata match: {filename}")
                continue

            new_name = self.build_new_name(parts, metadata_row)


            new_path = os.path.join(self.inputdir, new_name)

            if old_path == new_path:
                continue

            if os.path.exists(new_path):
                print(f"Exists, skipping: {new_name}")
                continue

            if self.dry_run:
                print(f"[DRY RUN] {filename} → {new_name}")
            else:
                os.rename(old_path, new_path)
                print(f"{filename} → {new_name}")

    def run(self):
        self.load_metadata()
        self.rename_files()


def main():
    parser = argparse.ArgumentParser(description="Rename FASTQ files using metadata")

    parser.add_argument("-i", "--inputdir", required=True)
    parser.add_argument("-m", "--metadata", required=True)
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    renamer = FastqRenamer(
        inputdir=args.inputdir,
        metadata_file=args.metadata,
        dry_run=args.dry_run
    )

    renamer.run()


if __name__ == "__main__":
    main()
#!/bin/bash
#SBATCH --output=logs/log_stretcher_%j_%a.log
#SBATCH --partition=example
#SBATCH --time=0-00:05:00
#SBATCH --mem=500M
#SBATCH --mincpus=1

# Slusky Lab
# Emily Proctor

# this should be submitted with --array tag
# this is ran with run_clean_stretcher_output.sh and run_continuous.sh

INDEX=$SLURM_ARRAY_TASK_ID
PAIR_INDEXES=$(sed -n "${INDEX}p" 8025_pairs.txt)
SEQ1_INDEX=$(echo $PAIR_INDEXES | cut -f 1 -d " ")
SEQ2_INDEX=$(echo $PAIR_INDEXES | cut -f 2 -d " ")

./EMBOSS-6.6.0/emboss/stretcher -filter \
-sprotein1 -sid1 "$(sed -n "$((2 * ${SEQ1_INDEX} - 1))p" 8025_stretcher/8025_seqs.fasta)" -sformat1 "raw" \
-sprotein2 -sid2 "$(sed -n "$((2 * ${SEQ2_INDEX} - 1))p" 8025_stretcher/8025_seqs.fasta)" -sformat2 "raw" \
-gapopen 12 -gapextend 2 \
-datafile EBLOSUM62 -stdout \
-asequence <(sed -n $((2 * ${SEQ1_INDEX}))p 8025_stretcher/8025_seqs.fasta) \
-bsequence <(sed -n $((2 * ${SEQ2_INDEX}))p 8025_stretcher/8025_seqs.fasta) | grep -E "1: |2: |Similarity" >> outdir/results_${SEQ1_INDEX}_${SEQ2_INDEX}.txt

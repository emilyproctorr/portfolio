#!/bin/bash
#SBATCH --output=logs/log_stretcher_%j.log
#SBATCH --partition=example
#SBATCH --time=4-00:00:00
#SBATCH --mem=1G
#SBATCH --mincpus=1

# Emily Proctor
# Script Info
    # This script runs EMBOSS Stretcher on all sequence pairs listed in the provided pair file. The pair file contains
    # all combinations of sequence index comparisons. To accelerate computation, the full set of pairwise index 
    # combinations is typically split across multiple pair files. Each pair file contains a subset of sequence 
    # index pairs, allowing the workload to be distributed across many tasks. This significantly reduces the total 
    # runtime for large all-vs-all similarity datasets. Using these index pairs, the corresponding sequences are extracted
    # from two fasta files and compared using EMBOSS Stretcher. The output file is parsed to extract the similarity 
    # percentage, and results are saved to an output file.


PAIR_FILEPATH=$1 # filename that contains all possible combinations of indexed sequence comparisons
PAIR_FILE_BASENAME=$(basename $PAIR_FILEPATH .txt) # basename without extention
PAIR_FILE_LEN=$(wc -l $PAIR_FILEPATH | cut -f 1 -d " ") # grab length of file

# log variables
echo "pair filepath $PAIR_FILEPATH"
echo "pair PAIR_FILE_BASENAME $PAIR_FILE_BASENAME"
echo "pair PAIR_FILE_LEN $PAIR_FILE_LEN"

for ((INDEX = 1; INDEX <= $PAIR_FILE_LEN; INDEX++)) # for each line in file = each sequence index combination
do 
    PAIR_INDEXES=$(sed -n "${INDEX}p" $PAIR_FILEPATH) # grab particular sequence index combination on line, ex: 1 2
    SEQ1_INDEX=$(echo $PAIR_INDEXES | cut -f 1 -d " ") # output first sequence index, ex: 1
    SEQ2_INDEX=$(echo $PAIR_INDEXES | cut -f 2 -d " ") # output second sequence index, ex: 2

    # run emboss stretcher program to get sequence similarity percentage for two sequences
    ./EMBOSS-6.6.0/emboss/stretcher -filter \
    -sprotein1 -sid1 "$(sed -n "$((2 * ${SEQ1_INDEX} - 1))p" viri_ref_seqs/Triticum_aestivum_clu40.fasta)" -sformat1 "raw" \
    -sprotein2 -sid2 "$(sed -n "$((2 * ${SEQ2_INDEX} - 1))p" viri_ref_seqs/Chlamydomonas_reinhardtii_clu40.fasta)" -sformat2 "raw" \
    -gapopen 12 -gapextend 2 \
    -datafile EBLOSUM62 -stdout \
    -asequence <(sed -n $((2 * ${SEQ1_INDEX}))p viri_ref_seqs/Triticum_aestivum_clu40.fasta) \
    -bsequence <(sed -n $((2 * ${SEQ2_INDEX}))p viri_ref_seqs/Chlamydomonas_reinhardtii_clu40.fasta) \
                | grep -E "1: |2: |Similarity" | awk '/^# 1:/ {first=substr($3, 2)} /^# 2:/ {second=substr($3, 2)} /^# Similarity:/ {match($NF, /([0-9.]+)/, perc); print first, second, perc[1]}' >> /home/scratch/stretcher/${PAIR_FILE_BASENAME}_results.txt
done
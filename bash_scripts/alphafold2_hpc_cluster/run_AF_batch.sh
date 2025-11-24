#!/bin/bash
#SBATCH --partition=example
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=60g
#SBATCH --time=6-00:00:00
#SBATCH --output=run_af_18_chlam_trit_hits_483training/logs/af_bigjay_array_%j_%a.log
#SBATCH --array=1-18

# Emily Proctor
# Script info
    # This script runs AlphaFld2 on a single sequence from a fasta file. This script is submitted as a job array, 
    # with each array index corresponding to a sequence in the fasta file.

# clean up environment and load required modules
module purge
module load singularity alphafold

# obtain file basename
BASEFILE=$(basename $INPUT_FILE)
BASENAME=$(basename -s .fasta $INPUT_FILE)

# log variables
echo "INPUT_FILE $INPUT_FILE"
echo "SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_ID"
echo "BASENAME $BASENAME"
echo "BASEFILE $BASEFILE"

# select header and sequence and save to temporary file
sed -n $((2*${SLURM_ARRAY_TASK_ID}-1)),+1p $INPUT_FILE > run_af_18_chlam_trit_hits_483training/fasta_files/${BASENAME}_${SLURM_ARRAY_TASK_ID}.fasta

# run af2
run --fasta_paths=run_af_18_chlam_trit_hits_483training/fasta_files/${BASENAME}_${SLURM_ARRAY_TASK_ID}.fasta \
    --output_dir=run_af_18_chlam_trit_hits_483training/outdir \
    --model_preset=monomer_ptm \
    --max_template_date=2025-12-31 \
    --pdb70_database_path=/data/pdb70/pdb70 \
    --uniref30_database_path=/data/uniref30/UniRef30_2021_03 \
    --db_preset=full_dbs \
    --bfd_database_path=/data/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
    --template_mmcif_dir=/data/pdb_mmcif/mmcif_files \
    --obsolete_pdbs_path=/data/pdb_mmcif/obsolete.dat \
    --use_gpu_relax=False \
    --run_relax=False

# remove temporary file
rm run_af_18_chlam_trit_hits_483training/fasta_files/${BASENAME}_${SLURM_ARRAY_TASK_ID}.fasta

#!/bin/bash
#SBATCH --output=logs/logs_2301_2400/log_raptorx_%a.log
#SBATCH --partition=example
#SBATCH --time=0-06:00:00
#SBATCH --mem=1G

# Emily Proctor
# Script info
    # This file generates a RaptorX protein cotnact map for a single sequence. This script is submitted by the run_continuous.sh 
    # script as a job array (for each sequence index). This process requires sequential execution of three scripts - first_step.sh, second_step.sh, third_step.sh. 
    # These scripts have to be run sequentially, as only parts of the RaptorX workflow are able to be GPU ran, and this provides a more efficient process. 
    # If one step has already been completed (indicated by flag_file), a wrapper job is ran to skip that step. The wrapper job is required to maintain job dependencies.

# activate conda environment
module load conda
eval "$(conda shell.bash hook)"
conda activate conrap_env

# define variables
fasta_file="Chlamydomonas_reinhardtii_lens_2301_to_2400.fasta"
fasta_basename_noex=$(basename -s .fasta $fasta_file) # basename without extension
main_path="example"
seq_id=$SLURM_ARRAY_TASK_ID # sequence id to process

# make output directory for this sequence
mkdir -p $main_path/output_files/$fasta_basename_noex/$seq_id

# if final output file (contact map) is present then job complete
if find "$main_path/output_folders/$fasta_basename_noex/$seq_id/" -name '*CASPmap.pkl' | grep -q .; then
        echo "job complete, no steps need ran"
else
        # if first step complete (yestgt file present)
        if [ -f "$main_path/output_folders/$fasta_basename_noex/$seq_id/yestgt" ]; then
            # run wrapper job
            job_id1=$(sbatch --partition=example --output=/dev/null --wrap="sleep 0" | awk '{print $4}') # 4th field is job id
            echo "step 1 already complete, skip running, jobid = $job_id1"
        # if first step not complete
        else
            # run first step
            job_id1=$(sbatch --partition=example --time=1-00:00:00 --cpus-per-task=4 --mem=5G --output=$main_path/output_files/$fasta_basename_noex/$seq_id/step1_output.txt $main_path/first_step.sh $main_path/data/$fasta_file $seq_id | awk '{print $4}')
            echo "step 1 not complete, running, jobid = $job_id1"
        fi

        # if second step complete (yesfts file present)
        if [ -f "$main_path/output_folders/$fasta_basename_noex/$seq_id/yesfts" ]; then
            # run wrapper job
            job_id2=$(sbatch --dependency=afterok:$job_id1 --partition=example --output=/dev/null --wrap="sleep 0" | awk '{print $4}')
            echo "step 2 already complete, skip running, jobid = $job_id2"
        # if second step not complete
        else
            # run second step
            job_id2=$(sbatch --dependency=afterok:$job_id1 --partition=example --time=0-00:30:00 --mem=2G --gres=gpu:1 --output=$main_path/output_files/$fasta_basename_noex/$seq_id/step2_output.txt $main_path/second_step.sh $main_path/data/$fasta_file $seq_id 0 | awk '{print $4}')
	    echo "step 2 not complete, running, jobid = $job_id2"
        fi

        # if third step complete (yesmap file present)
        if [ -f "$main_path/output_folders/$fasta_basename_noex/$seq_id/yesmap" ]; then
            # run wrapper job
            job_id3=$(sbatch --dependency=afterok:$job_id2 --partition=example --output=/dev/null --wrap="sleep 0" | awk '{print $4}')
            echo "step 3 already complete, skip running, jobid = $job_id3"
        # if third step not complete
        else
            # run third step
            job_id3=$(sbatch --dependency=afterok:$job_id2 --partition=example --time=0-06:00:00 --cpus-per-task=4 --mem=150G --output=$main_path/output_files/$fasta_basename_noex/$seq_id/step3_output.txt $main_path/third_step.sh $main_path/data/$fasta_file $seq_id | awk '{print $4}')
            echo "step 3 not complete, running, jobid = $job_id3"
        fi
fi

conda deactivate

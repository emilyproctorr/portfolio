#!/bin/bash
#SBATCH --output=cont_logs/log_%j.log
#SBATCH --partition=example
#SBATCH --time=0-06:00:00
#SBATCH --mem=1G

# Emily Proctor

current_time=$(date +"%Y-%m-%d %H:%M:%S")

echo "----- Starting new run at $current_time -----" >> log_run_cont.log

fasta_filename="data/Chlamydomonas_reinhardtii_lens_1401_to_1500.fasta"
num_seqs=$(grep ">" "$fasta_filename"| wc -l)
num_jobs_running=$(squeue --user=$USER | grep "R  " | wc -l)
num_jobs_total=$(squeue --user=$USER | wc -l)
last_job_ran_id=$1

{
    echo "num seqs: $num_seqs"
    echo "num_jobs_running: $num_jobs_running"
    echo "num_jobs_total: $num_jobs_total"
    echo "last_job_ran_id: $last_job_ran_id"
} >> log_run_cont.log

if [ "$num_jobs_running" -ge 50 ]; then
    next_end_index=$last_job_ran_id
    echo "greater than" >> log_run_cont.log
else
    echo "less than" >> log_run_cont.log

    # extra check just to make sure jobs dont get too backed up when cluster is slow
    if [ "$num_jobs_total" -gt 200 ]; then
        echo "too many jobs pending/waiting to run" >> log_run_cont.log
        exit 0
    fi

    # if the last job ran id is the last sequence in this fasta file then dont run anymore jobs
    if [ "$last_job_ran_id" -eq "$num_seqs" ]; then
        echo "last job ran equal to num seqs" >> log_run_cont.log
        exit 0
    fi

    # want to run around 50 jobs at all times
    more_jobs_to_run=$((50 - $num_jobs_running))
    echo "more_jobs_to_run $more_jobs_to_run" >> log_run_cont.log

    # update start and end index to run more jobs
    next_start_index=$(($last_job_ran_id + 1))
    next_end_index=$(($next_start_index + $more_jobs_to_run))
    last_job_ran_id=$next_end_index

    echo "next_start_index $next_start_index" >> log_run_cont.log
    echo "next_end_index $next_end_index" >> log_run_cont.log

    # if the updated end index is greater than how many sequences there are in fasta file
        # update end index to match how many sequences in fasta
    if [ "$next_end_index" -gt "$num_seqs" ]; then
        echo "last job ran greater than num seqs" >> log_run_cont.log
        next_end_index=$num_seqs
        echo "updated next_end_index $next_end_index" >> log_run_cont.log
    fi

    echo "submitting job array: $next_start_index-$next_end_index" >> log_run_cont.log
    sbatch --array=$next_start_index-$next_end_index run_job_batch.sh
    
fi

sbatch --begin=now+10minutes "$0" "$next_end_index"
echo "----- End of run -----" >> log_run_cont.log
echo >> log_run_cont.log

#!/bin/bash
#SBATCH --output=cont_logs/log_%j.txt
#SBATCH --partition=example
#SBATCH --time=0-06:00:00
#SBATCH --mem=1G

# Slusky Lab
# Emily Proctor

current_time=$(date +"%Y-%m-%d %H:%M:%S")

echo "----- Starting new run at $current_time -----" >> log_run_cont.log # log time of run

num_pairs=1000000
num_jobs_running=$(squeue --user=$USER --array | grep "R  " | wc -l) # check number of jobs currently running
num_jobs_total=$(squeue --user=$USER --array | wc -l) # check number of total jobs submitted, including pending, running, etc.
last_job_ran_id=$1

{
    echo "num_jobs_running: $num_jobs_running"
    echo "num_jobs_total: $num_jobs_total"
    echo "last_job_ran_id: $last_job_ran_id"
} >> log_run_cont.log

# if there are over 500 jobs currently submitted
if [ "$num_jobs_total" -ge 500 ]; then
    # update end job index
    next_end_index=$last_job_ran_id
    echo "greater than" >> log_run_cont.log
# if there are less than 500 jobs currently submitted
else
    echo "less than" >> log_run_cont.log

    # if the last job ran id is the last sequence in this fasta file then dont run anymore jobs
    if [ "$last_job_ran_id" -eq "$num_pairs" ]; then
        echo "last job ran equal to num seqs" >> log_run_cont.log
        exit 0
    fi

    # want to run around 500 jobs at all times
    more_jobs_to_run=$((500 - $num_jobs_total))
    echo "more_jobs_to_run $more_jobs_to_run" >> log_run_cont.log

    # update start and end index to run more jobs
    next_start_index=$(($last_job_ran_id + 1))
    next_end_index=$(($next_start_index + $more_jobs_to_run))
    last_job_ran_id=$next_end_index

    echo "next_start_index $next_start_index" >> log_run_cont.log
    echo "next_end_index $next_end_index" >> log_run_cont.log

    # if the updated end index is greater than how many sequences there are in fasta file
        # update end index to match number of sequences in fasta
    if [ "$next_end_index" -gt "$num_pairs" ]; then
        echo "last job ran greater than num seqs" >> log_run_cont.log
        next_end_index=$num_pairs
        echo "updated next_end_index $next_end_index" >> log_run_cont.log
    fi

    echo "submitting job array: $next_start_index-$next_end_index" >> log_run_cont.log
    sbatch --array=$next_start_index-$next_end_index run_stretcher.sh
    
fi

sbatch --begin=now+10seconds "$0" "$next_end_index"
echo "----- End of run -----" >> log_run_cont.log
echo >> log_run_cont.log

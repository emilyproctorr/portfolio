#!/bin/bash
#SBATCH --output=clean_stretcher_logs/log_%j.txt
#SBATCH --partition=example
#SBATCH --time=0-06:00:00
#SBATCH --mem=1G

current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "new run at $current_time" >> clean_log.txt # log time of run

result_files=$(ls outdir/) # get all files in output folder

for file in $result_files # for each file
do
    if ! lsof "outdir/$file" >/dev/null 2>&1 # if file is not in use
    then
        # condense output
        awk '/^# 1:/ {first=substr($3, 2)} /^# 2:/ {second=substr($3, 2)} /^# Similarity:/ {match($4, /\(([0-9.]+)%\)/, perc); print first, second, perc[1]}' outdir/$file >> total_results.txt
        rm outdir/$file # remove file
        echo "file $file removed" >> clean_log.txt
    else
        echo "file $file being proccessed, not removed" >> clean_log.txt
    fi
done

sbatch --begin=now+10seconds "$0" # run again in 10 seconds
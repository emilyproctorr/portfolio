#!/bin/bash
#SBATCH --output=copy_logs/log_%j.log
#SBATCH --partition=example
#SBATCH --time=0-06:00:00
#SBATCH --mem=1G

module load python/3.7
python3 copy_af_output.py

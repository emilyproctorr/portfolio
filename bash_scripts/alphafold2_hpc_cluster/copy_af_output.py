# Emily Proctor
# Script Info
    # This script copies over the top AlphaFold prediction (based on pLDDT score) for each protein from a set of
    # AlphaFold output directories to a new output directory, renaming the files based on a provided index mapping file.

import json
import shutil
import os
import argparse

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--index_file', type=str, help='File containing one column of indexes and one column of protein ids')
parser.add_argument("--af_output_dir", type=str, help="Directory containing AF output folders")
parser.add_argument("--af_subdir_prefix", type=str, help="Prefix for AF output subdirectories")
parser.add_argument("--output_dir", type=str, help="Output folder")
args = parser.parse_args()

# assign arguments to variables
index_file = args.index_file
af_output_dir = args.af_output_dir
af_subdir_prefix = args.af_subdir_prefix
output_dir = args.output_dir

# read index file and get dictionary mapping index to protein ids
def get_id_indexes():
    ids_indexes_dict = {}
    with open(f"{index_file}", "r") as file:
        for line in file:
            line = line.strip().split()
            ids_indexes_dict[int(line[0])] = line[1]
    return ids_indexes_dict # {1: id1, 2: id2, etc.}

# for each index (protein id), find top AF prediction by pLDDT, copy over to new folder with new name, log to file
def copy_over_top_af_results(index_dict):
    for index in range(1, len(index_dict)+1):
        try:
            # find ranking file that shows the highest plddt for each prediction
            with open(f"{af_output_dir}/{af_subdir_prefix}_{index}/ranking_debug.json", "r") as file:
                plddts = json.load(file)['plddts']

                # get top model according to plddt score
                top_model = max(plddts, key=plddts.get)
                top_plddt = plddts[top_model]
                top_model_file_name = f"unrelaxed_{top_model}.pdb"

                with open(f"protid_to_top_model_mapping.txt", "a") as file:
                    file.write(f"{index} {index_dict[index]} {top_model} {top_plddt}\n")

                # source path for top model file
                source_path = f"{af_output_dir}/{af_subdir_prefix}_{index}/{top_model_file_name}"

                new_file_name = f"{index_dict[index]}_top_af_prediction.pdb"
                # destination path where we want to copy to along with new file name (index id -> prot id)
                destination_path = f"{output_dir}/{new_file_name}"

                # copy over top prediction to new folder
                shutil.copy(source_path, destination_path)

        # catch errors with any protein ids
        except:
            print(f"Error index = {index}")

id_indexes_dict = get_id_indexes()
copy_over_top_af_results(id_indexes_dict)

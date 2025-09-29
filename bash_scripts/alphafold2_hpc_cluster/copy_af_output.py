# Emily Proctor
# Purpose
    # For each protein with AF output, grab the prediction with higheset pLDDT, copy over to separate folder, log to file, rename top prediction with protein id

import json
import shutil
import os

def get_id_indexes():
    ids_indexes_dict = {}
    with open(f"18_indexed_ids.txt", "r") as file:
        for line in file:
            line = line.strip().split()
            ids_indexes_dict[int(line[0])] = line[1]
    return ids_indexes_dict # [1: id1, 2: id2, etc.]

def copy_over_top_af_results(index_dict):
    for index in range(1, 19):
        try:
            # find ranking file that shows the highest plddt for each prediction
            with open(f"outdir/18_chlam_trit_hit_483training_seqs_{index}/ranking_debug.json", "r") as file:
                plddts = json.load(file)['plddts']

                # get top model according to plddt score
                top_model = max(plddts, key=plddts.get)
                top_plddt = plddts[top_model]
                top_model_file_name = f"unrelaxed_{top_model}.pdb"

                with open(f"protid_to_top_model_mapping.txt", "a") as file:
                    file.write(f"{index} {index_dict[index]} {top_model} {top_plddt}\n")

                # source path for top model file
                source_path = f"outdir/18_chlam_trit_hit_483training_seqs_{index}/{top_model_file_name}"

                new_file_name = f"{index_dict[index]}_top_af_prediction.pdb"
                # destination path where we want to copy to along with new file name (index id -> prot id)
                destination_path = f"18_af_predictions/{new_file_name}"

                # copy over top prediction to new folder
                shutil.copy(source_path, destination_path)

        except:
            print(f"Error index = {index}")


id_indexes_dict = get_id_indexes()
copy_over_top_af_results(id_indexes_dict)

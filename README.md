# Portfolio

## Programming Projects

### 1. Bidirectional LSTM for per-residue secondary protein structure classification

A PyTorch implementation of a bidirectional LSTM used to predict per-residue secondary structure assignment given primary amino acid sequence. The model predicts either 3-class (general) or 9-class (specific) secondary structure assignment using DSSP (Database of Secondary Structure Assignments) labels. This model supports both training and inference of protein sequences.

- **Repository**: [BiLSTM for SS prediction](https://github.com/emilyproctorr/protein_ss_biLSTM)

### 2. PlanNova (full stack)

This was my capstone project created in my senior year of my undergraduate degree. This was a team project including members Emily Proctor, Nathan Mignot, Gabi Kruger, Brooke West, and Kenadi Krueger. PlanNova is a cohesive organizational app designed specifically for college students. It offers tools to help users balance their academic responsibilities, maintain fitness goals, and enjoy their social lives. With features like meal planning, fitness tracking, and list making, PlanNova empowers students to stay organized and achieve success in all aspects of their college experience. 

- **Repository**: [PlanNova](https://github.com/brookewest11/PlanNova)

### 3. Budget Tracker (full stack)

Tracks monthly expenses, including individual transactions, planned amount to spend for individual categories, and income on a monthly basis.

- **Repository**: [Budget Tracker Repository](https://github.com/emilyproctorr/budget_tracker)

### 4. Product List Web App (frontend)

Frontend design challenge provided by Frontend Mentor. Implementation includes user ability to add and remove items from cart, increase/decrease the number of items in cart, provide order confirmation popup, see hover and focus states for all interactive elements on page, and more. 

- **Repository**: [Product List App Repository](https://github.com/emilyproctorr/product_list_project)
- **Live Site URL**: [View Demo](https://emilyproctorr.github.io/product_list_project)

### 5. Tkinter GUI Tool

I developed a GUI using the Tkinter library to visualize a proteins contact map and AlphaFold 2 prediction image. This application enables users to classify proteins as "yes," "maybe," or "no" based on a specific characteristic of interest. It displays the selected classification along with the corresponding protein ID. Additionally, the application automatically saves progress, ensuring that user responses are preserved. Upon restarting, it resumes from the last recorded protein, allowing for continuation of the analysis. I have also included an image of the application within this folder.

- **Script and example image**: [Tkinter GUI Tool](tkinter_tool)

## Bash Scripts - HPC Cluster (Slurm)

### Protein Contact Map Generation with RaptorX

Link: [Protein Contact Map Generation](bash_scripts/contact_map_generation)

I present a workflow that automates the large-scale generation of RaptorX protein contact maps for protein sequences using Slurm job arrays. A controller script (`run_continuous.sh`) iteratively submits new job arrays with updated sequence IDs, to ensure maps are continuously being generated without overloading the cluster. Each array ID processes a single sequence by invoking a wrapper script (`run_job_batch.sh`), which executes the three required RaptorX steps (first_step.sh, second_step.sh, third_step.sh), which have to be run sequentially. Together, this provides an efficient workflow for generating contact maps for large numbers of sequences on an HPC cluster. 

### EMBOSS Stretcher Pairwise Sequence Similarity

Link: [EMBOSS Stretcher](bash_scripts/emboss_stretcher)

The EMBOSS Stretcher program is a tool used to compute the sequence similarity of two protein sequences using global alignment. I utilized this application to compute all-vs-all pairwise sequence similarity across large protein datasets. To improve efficiency, the full set of pairwise index combinations is divided into multiple pair files, which enables many comparisons to run in parallel on the HPC cluster. Each script processes a subset of sequence pairs, extracts the corresponding sequences from FASTA files, runs Stretcher, and parses the output to record the resulting similarity percentages.

### AlphaFold2

Link: [AlphaFold2](bash_scripts/alphafold2_hpc_cluster)

AlphaFold2 is a protein structure prediction tool that accurately predicts the 3D structure of a protein from primary amino acid sequence. To accelerate large numbers of predictions, I developed a workflow that utilizes a Slurm job array, assigning each array index to a specific sequence in the input FASTA file. This allows multiple sequences to be predicted in parallel.






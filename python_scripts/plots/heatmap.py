# Emily Proctor
# Slusky Lab

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

mcc_scores = []
bal_acc_scores = []
prec_scores = []
cc_scores = []
sep_values = []
with open("round0_train/IIAB_confmatrix_results.tsv", "r") as file:
    next(file)
    for line in file:
        line = line.split("\t")
        mcc_scores.append(float(line[3]))
        bal_acc_scores.append(float(line[4]))
        cc_scores.append(float(line[0]))
        sep_values.append(int(line[1]))
        prec_scores.append(float(line[5]))

data = {
    "CC Score" : cc_scores,
    "Separation Value" : sep_values,
    # "mcc" : mcc_scores
    # "bal acc" : bal_acc_scores,
    "precision" : prec_scores
}

df = pd.DataFrame(data)
heatmap_data = df.pivot(index='CC Score', columns='Separation Value', values='precision')

ax = sns.heatmap(heatmap_data, annot=True)
cbar = ax.collections[0].colorbar
cbar.set_label("Precision")
cbar.set_ticks([])
cbar.outline.set_edgecolor('None')

plt.savefig("precision_heatmap.png", bbox_inches='tight', dpi=300)
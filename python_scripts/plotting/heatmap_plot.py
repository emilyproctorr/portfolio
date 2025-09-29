# Emily Proctor

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# load data
df = pd.read_csv("round0_train/IIAB_confmatrix_results.tsv", sep="\t")
df.columns = ["cc_score", "separation", "barrel", "mcc", "bal_acc", "precision"]

# reformat
heatmap_data = df.pivot(index='cc_score', columns='separation', values='precision')
# plot
ax = sns.heatmap(heatmap_data, annot=True)

# color bar
cbar = ax.collections[0].colorbar
cbar.set_label("Precision")
cbar.set_ticks([])
cbar.outline.set_edgecolor('None')

plt.savefig("precision_heatmap.png", bbox_inches='tight', dpi=300)
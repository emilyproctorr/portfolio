# Emily Proctor

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("organism", type=str, help="organism name -> escherichia_coli, neisseria_gonorrhoeae, or campylobacter_jejuni")
parser.add_argument("data_filepath", type=str, help="path to file with pI values")
parser.add_argument("plot_color", type=str, default="blue", help="color for the plot")
parser.add_argument("rug_offset", type=float, help="offset for rugplot")
args = parser.parse_args()

organism = args.organism
data_filepath = args.data_filepath
plot_color = args.plot_color
rug_offset = args.rug_offset

with open(data_filepath, "r") as file:
    pi_values = [float(line.split("\t")[1]) for line in file if line.strip()]

plt.figure(figsize=(12, 8))
pi_values = np.array(pi_values)

axes = sns.kdeplot(data=pi_values, color=plot_color, fill=True, label=f"n={len(pi_values)}")
axes.scatter(x=pi_values, y=np.full(len(pi_values), rug_offset), color=plot_color, marker="|", alpha=0.6, s=100)
axes.axhline(y=0, color="black", linewidth=1)

axes.set_xlabel("pI", fontsize=20)
axes.set_ylabel("Density", fontsize=20)

axes.set_xlim(3.5, 12.5)
plt.ylim(-0.08, 0.6)

axes.set_yticks([tick for tick in axes.get_yticks() if tick >= 0])
axes.set_title(f"{organism.replace('_', ' ').title()}", fontsize=15, pad=20)
axes.tick_params(axis="both", labelsize=20)
axes.legend(fontsize=20, loc='upper left', bbox_to_anchor=(1, 1.05), frameon=False)

fig = axes.get_figure()
fig.savefig(f"{organism}_pI_kde_rug.png", dpi=600, transparent=True, bbox_inches='tight')

    


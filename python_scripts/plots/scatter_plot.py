# Emily Proctor
# Slusky Lab

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
	
percent_pair_sim = []
i = 0
while i < 100:
	percent_pair_sim.append(i)
	i += 5

percent_same_IIAB = []
with open(f"IIAB_bacteria_balanced_z_18/bin_percent.txt", "r") as file:
	for line in file:
		line = line.split()
		percent_same_IIAB.append(float(line[-1].strip())*100)

bacteria_percent_same = []
with open("bacteria_percent_same.txt", "r") as file:
	for line in file:
		line = line.split()
		bacteria_percent_same.append(float(line[-1].strip())*100)

counts = []
with open(f"IIAB_bacteria_balanced_z_18/bin_counts.txt", "r") as file:
	next(file)
	for line in file:
		line = line.split()
		counts.append(float(line[2].strip()))

oep = []
non_oep = []
with open(f"IIAB_bacteria_balanced_z_18/balanced_results_z_18.tsv", "r") as file:
	next(file)
	for line in file:
		line = line.strip().split("\t")
		if float(line[4]) > 0:
			oep.append(line)
		if float(line[4]) == 0:
			non_oep.append(line)

fig, ax = plt.subplots()
ax.scatter(percent_pair_sim, percent_same_IIAB, color="mediumseagreen")
ax.plot(percent_pair_sim, percent_same_IIAB, color="mediumseagreen", label="chloroplast")
ax.scatter(percent_pair_sim, bacteria_percent_same, color="blue")
ax.plot(percent_pair_sim, bacteria_percent_same, color="blue", label="bacteria")
ax.grid(True)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.tick_params(labelsize=16)
ax.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", fontsize=15, frameon=False)
ax.set_xlabel("% Pairwise Similarity", fontsize=16)
ax.set_ylabel("% Same IIAB Prediction", fontsize=16)


ax.annotate(f"OEP = {len(oep)}\nnon-OEP = {len(non_oep)}", xy=(0.65,1.05),xycoords='axes fraction', fontsize=16)

# used to create custom tick labels
# x = tick value, pos = tick position
def exponent_formatter(x, pos):
	return f"{int(np.log10(x))}"

ax2 = ax.twinx()
ax2.scatter(percent_pair_sim, counts, color="gray", alpha=0.5)
ax2.plot(percent_pair_sim, counts, color="gray", alpha=0.5)
ax2.set_ylabel("log10 (Number of Comparisons)", fontsize=16, color="gray")
ax2.set_yscale('log')
ax2.set_ylim(10**4, 10**7)

# referring to y axis, set_major_formatter = sets major ticks (large ticks) using custom function
# FuncFormatter(exponent_formatter) = create instance of FuncFormatter and uses exponent_formatter to take in what the original label
	# is and creates a new one
# internally handles passing parameters
ax2.yaxis.set_major_formatter(FuncFormatter(exponent_formatter))
ax2.tick_params(labelsize=16)

ax.legend(fontsize=15)
plt.savefig(f"plot.png", dpi=300, bbox_inches='tight')
plt.show()
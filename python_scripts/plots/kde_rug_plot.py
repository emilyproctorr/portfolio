# Emily Proctor
# Slusky Lab

# two KDE plots with rug plots beneath

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pos_num_hairpins = []
with open("pos_num_hairpins.txt", "r") as file:
    for line in file:
        line = line.split()
        pos_num_hairpins.append(int(line[1]))

neg_num_hairpins = []
with open("neg_num_hairpins.txt", "r") as file:
    for line in file:
        line = line.split()
        neg_num_hairpins.append(int(line[1]))


colormap1 = plt.cm.get_cmap("Reds")
colormap2 = plt.cm.get_cmap("Blues")

sns.kdeplot(data=pos_num_hairpins, label="positive set (141 seq)", color="blue", fill=True)
sns.kdeplot(data=neg_num_hairpins, label="negative set (254 seq)", color="red", fill=True)
# this is code for rug plot
plt.scatter(x=neg_num_hairpins, y=np.full(len(neg_num_hairpins), -0.016), marker="o", color="red", alpha=0.05)
plt.scatter(x=pos_num_hairpins, y=np.full(len(pos_num_hairpins), -0.032), marker="o", color="blue", alpha=0.05)
# makes a horizontal black line at y = 0 for cleaner look 
plt.axhline(y=0, color="black")
lo = min([min(pos_num_hairpins), min(neg_num_hairpins)])
hi = max([max(pos_num_hairpins), max(neg_num_hairpins)])
plt.xlim([lo, hi])
plt.ylim([-0.05, 0.35])
plt.legend(fontsize=11)
plt.xlabel("Number of Hairpins", fontsize=15)
plt.ylabel("Density", fontsize=15)
plt.savefig("num_hairpins_kde.png", dpi=300)

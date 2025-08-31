#!/usr/bin/env python3
"""
Script to reproduce the issue with dataLims getting replaced by inf 
for charts with twinx if ax1 is a stackplot
"""

import matplotlib.pyplot as plt
import numpy as np

def print_datalim(*ax):
    for ax_ in ax:
        print(ax_.dataLim.intervaly, end=' / ')
    print()

# Data from the issue
df1_index = ['16 May', '17 May']  # == df2_index
df1_values = [-22.717708333333402, 26.584999999999937]
df2_values = [-0.08501399999999998, -2.9833019999999966]

print("Reproducing the issue:")
fig, ax1 = plt.subplots()

ax1.stackplot(df1_index, df1_values)
print("After stackplot on ax1:", end=" ")
print_datalim(ax1)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
print("After creating twinx:", end=" ")
print_datalim(ax1, ax2)

ax2.plot(df1_index, df2_values)
print("After plot on ax2:", end=" ")
print_datalim(ax1, ax2)

# Let's also test the reverse scenario mentioned in the issue
print("\nTesting reverse scenario (plot first, then stackplot):")
fig2, ax3 = plt.subplots()

ax3.plot(df1_index, df2_values)
print("After plot on ax3:", end=" ")
print_datalim(ax3)

ax4 = ax3.twinx()
print("After creating twinx:", end=" ")
print_datalim(ax3, ax4)

ax4.stackplot(df1_index, df1_values)
print("After stackplot on ax4:", end=" ")
print_datalim(ax3, ax4)

plt.close('all')
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import os

# Set font
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 12

# Read Excel file
file_path = './data/Existing-ET-P.xlsx'
df_pmean = pd.read_excel(file_path, sheet_name='P')
df_etmean = pd.read_excel(file_path, sheet_name='ET')

# MDT values (hardcoded)
MDT_P_MEAN = 637.37
MDT_P_STD = 42.18
MDT_ET_MEAN = 293.44
MDT_ET_STD = 42.18

# Color mappings
p_colors = {
    "Numerical Models": "#1f77b4",
    "Remote sensing": "#ff7f0e",
    "Fusion product": "#2ca02c",
    "Gauge-based": "#d62728"
}

et_colors = {
    "Energy Balance Models": "#d62728",
    "Complementary Relationship Models": "#ff7f0e",
    "Penman-Monteith Models": "#2ca02c",
    "Numerical Models": "#9467bd",
    "Other Models": "#8b4513"
}

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=300)
fig.subplots_adjust(wspace=0.2)

# --- Plot a: P_mean + MDT_P ---
ax1.hlines(y=MDT_P_MEAN, xmin=2000, xmax=2018, color='black', linewidth=3, linestyle='--')
ax1.fill_between([2000, 2018], MDT_P_MEAN - MDT_P_STD, MDT_P_MEAN + MDT_P_STD,
                 color='gray', edgecolor='none', alpha=0.2)
ax1.text(2005, 635, 'MDT mean ± std: 637.37 ± 42.18', ha='center', va='top', fontsize=12,
         color='black', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

for typ, color in p_colors.items():
    subset = df_pmean[df_pmean['Type'] == typ]
    used_x_positions = set()
    for j, (_, row) in enumerate(subset.iterrows()):
        x_pos = (row['Start_Year'] + row['End_Year']) / 2
        while x_pos in used_x_positions:
            x_pos += 0.5
        used_x_positions.add(x_pos)
        y_offset = (-15 if j % 2 == 0 else 15)
        linestyle = '--' if row['Name'] in ['PREC1', 'PREC2', 'PREC3'] else '-'
        linewidth = 1.5 if row['Name'] in ['PREC1', 'PREC2', 'PREC3'] else 0.5
        ax1.hlines(y=row['Value'], xmin=row['Start_Year'], xmax=row['End_Year'],
                   color=color, linewidth=linewidth, linestyle=linestyle)
        ax1.text(x_pos, row['Value'] + y_offset, row['Name'], ha='center', va='center', fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

# --- Plot b: ET_mean + MDT_ET ---
ax2.hlines(y=MDT_ET_MEAN, xmin=2000, xmax=2018, color='black', linewidth=3, linestyle='--')
ax2.fill_between([2000, 2018], MDT_ET_MEAN - MDT_ET_STD, MDT_ET_MEAN + MDT_ET_STD,
                 color='gray', edgecolor='none', alpha=0.2)
ax2.text(2012, 305, 'MDT mean ± std: 293.44 ± 42.18', ha='center', va='top', fontsize=12,
         color='black', fontweight='bold',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

for typ, color in et_colors.items():
    subset = df_etmean[df_etmean['Type'] == typ]
    used_x_positions = set()
    for j, (_, row) in enumerate(subset.iterrows()):
        x_pos = (row['Start_Year'] + row['End_Year']) / 2
        while x_pos in used_x_positions:
            x_pos += 0.5
        used_x_positions.add(x_pos)
        y_offset = (-15 if j % 2 == 0 else 15)
        ax2.hlines(y=row['Value'], xmin=row['Start_Year'], xmax=row['End_Year'],
                   color=color, linewidth=0.5, linestyle='-')
        ax2.text(x_pos, row['Value'] + y_offset, row['Name'], ha='center', va='center', fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

# Axis settings
ax1.set_xlim(2000, 2018)
ax1.xaxis.set_major_locator(MultipleLocator(4))
ax1.set_ylim(300, 820)
ax1.yaxis.set_major_locator(MultipleLocator(100))
ax1.set_ylabel('Annual mean value (mm/yr)', fontsize=16, fontweight='bold')
ax1.set_title('b. P', loc='left', fontsize=20, fontweight='bold')

ax2.set_xlim(2000, 2018)
ax2.xaxis.set_major_locator(MultipleLocator(4))
ax2.set_ylim(200, 620)
ax2.yaxis.set_major_locator(MultipleLocator(100))
ax2.set_ylabel('Annual mean value (mm/yr)', fontsize=16, fontweight='bold')
ax2.set_title('c. ET', loc='left', fontsize=20, fontweight='bold')

for ax in [ax1, ax2]:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=12)

# Save figure
save_dir = './figures'
os.makedirs(save_dir, exist_ok=True)
save_path = os.path.join(save_dir, 'Fig3_b_c.jpg')
plt.savefig(save_path, bbox_inches='tight', dpi=300)
plt.close()

print(f"Figure saved to: {save_path}")

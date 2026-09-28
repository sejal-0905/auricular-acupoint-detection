"""
Compares feature values across patient groups using t-test (2 groups) or
ANOVA (3 groups). Replace the example lists with real values once you have
real feature data per group.

Usage:
    python compare_groups.py
"""

from scipy import stats
import numpy as np

# --- EXAMPLE DATA - replace with real values ---
healthy_group = [140, 135, 152, 148, 142, 138, 145, 139, 151, 144]
hypertension_group = [178, 182, 165, 190, 171, 188, 175, 180, 169, 185]
diabetes_group = [160, 158, 172, 165, 168, 155, 163, 170, 159, 166]

print("t-test: Healthy vs Hypertension")
t_stat, p_value = stats.ttest_ind(healthy_group, hypertension_group)
print(f"  t={t_stat:.3f}, p={p_value:.4f} -> {'SIGNIFICANT' if p_value < 0.05 else 'not significant'}")

print("\nt-test: Healthy vs Diabetes")
t_stat2, p_value2 = stats.ttest_ind(healthy_group, diabetes_group)
print(f"  t={t_stat2:.3f}, p={p_value2:.4f} -> {'SIGNIFICANT' if p_value2 < 0.05 else 'not significant'}")

print("\nANOVA: Healthy vs Hypertension vs Diabetes (use for shared points: Endocrine, ShenMen)")
f_stat, p_value3 = stats.f_oneway(healthy_group, hypertension_group, diabetes_group)
print(f"  F={f_stat:.3f}, p={p_value3:.4f} -> {'SIGNIFICANT' if p_value3 < 0.05 else 'not significant'}")

print(f"\nBonferroni-corrected threshold for 8 points: p < {0.05/8:.5f}")

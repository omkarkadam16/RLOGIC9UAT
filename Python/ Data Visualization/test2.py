# Example: Scatter Plot Analysis with Seaborn

import seaborn as sns
import matplotlib.pyplot as plt

# Load the 'tips' dataset
tips = sns.load_dataset("tips")

# Create a scatter plot
plt.figure(figsize=(6, 4))
sns.scatterplot(x="total_bill", y="tip", data=tips, hue="time", style="time")
plt.title("Total Bill vs Tip")
plt.xlabel("Total Bill")
plt.ylabel("Tip")
plt.show()

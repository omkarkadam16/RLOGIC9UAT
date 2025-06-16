# Examples: Visualizing Spread and Outliers
import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    "Category": ["A"] * 10 + ["B"] * 10,
    "Value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}

df = pd.DataFrame(data)

# Box plot
df.boxplot(by="Category")
plt.title("Box Plot Example")
plt.suptitle("")
plt.xlabel("Category")
plt.ylabel("Value")
plt.show()

import pandas as pd
from matplotlib import pyplot as plt

# Set style theme
plt.style.use('seaborn-v0_8-pastel')

# Read CSV into DataFrame
df = pd.read_csv('class-data-v1.csv')
print(df.info()) 
# NOTE: some cols need type converted (object -> boolean, datetime)

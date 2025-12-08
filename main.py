import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Set style theme
plt.style.use('seaborn-v0_8-pastel')

# Read CSV into DataFrame
df = pd.read_csv('class-data-v1.csv')
df = df.head(8) # Limit to first 8 rows for our class

# NOTE: some cols need type converted (object -> datetime, boolean)
df['Birthdate'] = pd.to_datetime(df['Birthdate']) 
df['Wakeup Time Weekday'] = pd.to_datetime(df['Wakeup Time Weekday'], format='%H:%M').dt.time
df['Wakeup Time Weekend'] = pd.to_datetime(df['Wakeup Time Weekend'], format='%H:%M').dt.time
df['Vision Impaired'] = pd.to_numeric(df['Vision Impaired']).fillna(0).astype(bool)
df['Night Owl'] = pd.to_numeric(df['Night Owl']).fillna(0).astype(bool)
print(df.info())

# SCATTER PLOT
plt.scatter(df['Instagram Followers'], df['Instagram Follows'], alpha=0.7)
plt.xlabel('Number of Followers')
plt.ylabel('Number of Accounts Followed')
plt.title('Instagram Follows vs. Followers')
plt.savefig('instagram_scatter.png', bbox_inches='tight')
plt.close()

# BAR CHART
color_counts = df['Color'].value_counts()
colors = color_counts.index.tolist() # Use color names as bar colors
plt.bar(color_counts.index, color_counts.values, color=colors)
plt.xlabel('Color')
plt.ylabel('Number of Students')
plt.title('Number of Students by Favorite Color')
plt.xticks(rotation=45)
plt.savefig('color_bar.png', bbox_inches='tight')
plt.close()

# PIE CHART
zodiac_counts = df['Zodiac Element'].value_counts()
colors = ["#df3b3b","#3389df","#5f8e5f","#c4c4c4"] # Custom colors
plt.pie(zodiac_counts.values, labels=zodiac_counts.index, colors=colors, startangle=90, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
plt.title('Distribution of Zodiac Elements')
plt.axis('equal')
plt.savefig('zodiac_element_pie.png', bbox_inches='tight')
plt.close()

# Calculate how many MINUTES students wake up (before 8:15 school start)
df['Wakeup Time in Minutes'] = df['Wakeup Time Weekday'].apply(lambda t: t.hour * 60 + t.minute)
df['Wakeup Before School'] = (8 * 60 + 15) - df['Wakeup Time in Minutes']

# SCATTER PLOT + LINE OF BEST FIT
plt.scatter(df['Commute Time Minutes'], df['Wakeup Before School'])
plt.ylabel('Wakeup Before School [mins]')
plt.xlabel('Commute Time [mins]')
plt.title('How Early Students Wake Up vs Commute Time')
# Calculate line of best fit 
m, b = np.polyfit(df['Commute Time Minutes'].dropna(), df['Wakeup Before School'].dropna(), 1)
# Plot line of best fit
plt.plot(df['Commute Time Minutes'], m*df['Commute Time Minutes'] + b, color='red')
# Add a figure caption below the plot
# The coordinates (0.5, 0.02) place the text near the bottom center of the figure
# ha='center' ensures the text is horizontally centered at x=0.5
# fontsize and color are optional styling parameters
plt.figtext(0.5, 0.02, "Positive linear trend shown between how long people wake up before 8:15AM and the time it takes to get to school.", 
            ha='center', fontsize=10, color='gray') 
plt.savefig('wakeup_scatter.png', bbox_inches='tight')
plt.close()

# HEATMAP (correlation matrix)
bigfive_cols = ['BigFive Neuroticism', 'BigFive Extraversion', 'BigFive Openness', 'BigFive Conscientious', 'BigFive Agreeableness']
bigfive_data = df[bigfive_cols]
correlation_matrix = bigfive_data.corr()

plt.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
plt.colorbar(label='Correlation Coefficient')
plt.xticks(range(len(bigfive_cols)), bigfive_cols, rotation=45, ha='right')
plt.yticks(range(len(bigfive_cols)), bigfive_cols)
plt.title('Correlation Heatmap of Personality Traits')

plt.tight_layout()
plt.savefig('bigfive_heatmap.png', bbox_inches='tight')
plt.close() 

# CATEGORICAL PLOT (grouped bar chart)
barWidth = 0.5
colors = df['Hex Color'].dropna().tolist()
r1 = np.arange(8) * (barWidth * 3.5)  # space each student
r2 = r1 + barWidth
r3 = r2 + barWidth

fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
bars1 = ax.bar(r1, df['Webdev Rating'].dropna(), color=colors, width=barWidth, edgecolor='white', label='WebDev')
bars2 = ax.bar(r2, df['Java Rating'].dropna(), color=colors, width=barWidth, edgecolor='white', label='Java')
bars3 = ax.bar(r3, df['Python Rating'].dropna(), color=colors, width=barWidth, edgecolor='white', label='Python')

ax.set_xticks(r1 + barWidth)
ax.set_xticklabels(df['Name'].head(8))
plt.title('Programming Language Ratings by Student')

# Add icons above each bar group
icon_paths = ['webdev-emoji.png', 'java-emoji.png', 'python-emoji.png']
for bars, icon in zip([bars1, bars2, bars3], icon_paths):
    for bar in bars:
        img = plt.imread(icon)
        ax.add_artist(AnnotationBbox(OffsetImage(img, zoom=0.02), 
                                      (bar.get_x() + bar.get_width()/2, bar.get_height()), 
                                      xybox=(0, 10), boxcoords="offset points", frameon=False))

plt.savefig('rating_bar.png', bbox_inches='tight')
plt.close()
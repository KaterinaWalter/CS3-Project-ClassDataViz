import pandas as pd
from matplotlib import pyplot as plt

# Set style theme
plt.style.use('seaborn-v0_8-pastel')

# Read CSV into DataFrame
df = pd.read_csv('class-data-v1.csv')

# NOTE: some cols need type converted (object -> datetime, boolean)
df['Birthdate'] = pd.to_datetime(df['Birthdate']) 
df['Wakeup Time Weekday'] = pd.to_datetime(df['Wakeup Time Weekday'], format='%H:%M').dt.time
df['Wakeup Time Weekend'] = pd.to_datetime(df['Wakeup Time Weekend'], format='%H:%M').dt.time
df['Vision Impaired'] = pd.to_numeric(df['Vision Impaired']).fillna(0).astype(bool)
df['Night Owl'] = pd.to_numeric(df['Night Owl']).fillna(0).astype(bool)
print(df.info())

# SCATTER PLOT
plt.scatter(df['BigFive Extraversion'], df['BigFive Agreeableness'])
plt.ylabel('Agreeableness Score')
plt.xlabel('Extraversion Score')
plt.title('BigFive Extraversion vs Agreeableness')
plt.savefig('bigfive_scatter.png', bbox_inches='tight')
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
colors = ["#df3b3b","#3389df","#5f8e5f","#c4c4c4"]  # Custom colors for each element
plt.pie(zodiac_counts.values, labels=zodiac_counts.index, colors=colors, startangle=90, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
plt.title('Distribution of Zodiac Elements')
plt.axis('equal')
plt.savefig('zodiac_element_pie.png', bbox_inches='tight')
plt.close()

# Calculate how many MINUTES students wake up (before 8:15 school start)
df['Wakeup Time in Minutes'] = df['Wakeup Time Weekday'].apply(lambda t: t.hour * 60 + t.minute)
df['Wakeup Before School'] = (8 * 60 + 15) - df['Wakeup Time in Minutes']

# SCATTER PLOT
plt.scatter(df['Commute Time Minutes'], df['Wakeup Before School'])
plt.ylabel('Wakeup Before School [mins]')
plt.xlabel('Commute Time [mins]')
plt.title('How Early Students Wake Up vs Commute Time')
plt.savefig('wakeup_scatter.png', bbox_inches='tight')
plt.close()
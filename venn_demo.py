from matplotlib_venn import venn2, venn2_circles
import matplotlib.pyplot as plt

# Sample Data (lists with duplicates)
list_a = ['apple', 'banana', 'cherry', 'date', 'apple']
list_b = ['banana', 'date', 'elderberry', 'fig']

# Convert to sets for uniqueness
set_a = set(list_a)  # {'apple', 'banana', 'cherry', 'date'}
set_b = set(list_b)  # {'banana', 'date', 'elderberry', 'fig'}

# Calculate intersections and differences for labels
only_a = set_a - set_b # {'apple', 'cherry'}
only_b = set_b - set_a # {'elderberry', 'fig'}
both = set_a & set_b   # {'banana', 'date'}

# Create the plot
plt.figure(figsize=(8, 6))
v = venn2([set_a, set_b], set_labels=('Set A', 'Set B'))

# Add text for unique items
v.get_label_by_id('10').set_text('\n'.join(only_a))
v.get_label_by_id('01').set_text('\n'.join(only_b))
v.get_label_by_id('11').set_text('\n'.join(both))

# Add a title and display the plot
plt.title("2-Set Venn Diagram")
plt.savefig("venn.png", bbox_inches='tight')
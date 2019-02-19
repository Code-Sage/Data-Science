from pylab import plot, show, savefig, xlim, figure, \
                hold, ylim, legend, boxplot, setp, axes

# Some fake data to plot
A= [[1, 2, 5,],  [7, 2]]
B = [[5, 7, 2, 2, 5], [7, 2, 5]]
C = [[3,2,5,7], [6, 7, 3]]

fig = figure()
ax = axes()
hold(True)

# first boxplot pair
bp = boxplot(A, positions = [1, 2], widths = 0.4)

# second boxplot pair
bp = boxplot(B, positions = [4, 5], widths = 0.4)


# thrid boxplot pair
bp = boxplot(C, positions = [7, 8], widths = 0.4)


# set axes limits and labels
xlim(0,9)
ylim(0,9)
ax.set_xticklabels(['A', 'B', 'C'])
ax.set_xticks([1.5, 4.5, 7.5])



savefig('boxcompare.png')
show()

#  [1]  https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
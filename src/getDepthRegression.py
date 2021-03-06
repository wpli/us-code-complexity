import csv
import numpy
import scipy.stats
import pandas
import pylab

data_elements = pandas.DataFrame.from_csv('results/table_title_elements.csv', parse_dates=False, header=None)
data_depth = pandas.DataFrame.from_csv('results/table_title_depth.csv', parse_dates=False, header=None)
element_count = data_elements.ix[:, 1].apply(numpy.log10)
title_depth = data_depth.ix[:, 1]
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(element_count, title_depth)

# Plot the base scatter
pylab.figure()
pylab.scatter(element_count, title_depth)

# Get x-min/x-max
x0 = min(element_count)
y0 = slope * x0 + intercept
x1 = max(element_count)
y1 = slope * x1 + intercept
pylab.plot([x0, x1], [y0, y1], 'k--', lw=1)

# Show
pylab.xlabel('log10(elements)')
pylab.ylabel('Mean depth')
pylab.savefig('log10_elements_title_depth_regression.jpg', figsize=(8,6))

print((slope, intercept, r_value, p_value, std_err))

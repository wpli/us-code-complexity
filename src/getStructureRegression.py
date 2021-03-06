import csv
import numpy
import scipy.stats
import pandas
import pylab

data = pandas.DataFrame.from_csv('results/table_title_elements.csv', parse_dates=False, header=None)
print(data.head())
section_count = data.ix[:, 3].apply(numpy.log10)
element_count = data.ix[:, 1].apply(numpy.log10)
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(element_count, section_count)

# Plot the base scatter
pylab.figure()
pylab.scatter(element_count, section_count)

# Get x-min/x-max
x0 = min(element_count)
y0 = slope * x0 + intercept
x1 = max(element_count)
y1 = slope * x1 + intercept
pylab.plot([x0, x1], [y0, y1], 'k--', lw=1)

# Show
pylab.xlabel('log10(elements)')
pylab.ylabel('log10(sections)')
pylab.savefig('log10_elements_section_regression.jpg', figsize=(8,6))

print((slope, intercept, r_value, p_value, std_err))

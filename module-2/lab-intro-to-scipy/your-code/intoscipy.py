# -*- coding: utf-8 -*-
"""intoscipy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eUMDYsmEV27kriI7z5altwPz4F7gXQ-e

# Before your start:
- Read the README.md file
- Comment as much as you can and use the resources (README.md file)
- Happy learning!
"""

#import numpy and pandas

import numpy as np
import pandas as pd

"""# Challenge 1 - The `stats` Submodule

This submodule contains statistical functions for conducting hypothesis tests, producing various distributions and other useful tools. Let's examine this submodule using the KickStarter dataset. We will load the dataset below.
"""

# Run this code:

from google.colab import drive 
drive.mount('/content/gdrive')


kickstarter=pd.read_csv('gdrive/My Drive/ks-projects-201801.csv')

"""Now print the `head` function to examine the dataset."""

# Your code here:

kickstarter.head()

"""Import the `mode` function from `scipy.stats` and find the mode of the `country` and `currency` column."""

# Your code here:
from scipy.stats import mode

mode(kickstarter[['country', 'currency']])

"""The trimmed mean is a function that computes the mean of the data with observations removed. The most common way to compute a trimmed mean is by specifying a percentage and then removing elements from both ends. However, we can also specify a threshold on both ends. The goal of this function is to create a more robust method of computing the mean that is less influenced by outliers. SciPy contains a function called `tmean` for computing the trimmed mean. 

In the cell below, import the `tmean` function and then find the 75th percentile of the `goal` column. Compute the trimmed mean between 0 and the 75th percentile of the column. Read more about the `tmean` function [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.tmean.html#scipy.stats.tmean).
"""

# Your code here:
from scipy.stats import tmean

tmean(kickstarter.goal, (0,kickstarter.goal.quantile(0.75)))

"""#### SciPy contains various statistical tests. One of the tests is Fisher's exact test. This test is used for contingency tables. 

The test originates from the "Lady Tasting Tea" experiment. In 1935, Fisher published the results of the experiment in his book. The experiment was based on a claim by Muriel Bristol that she can taste whether tea or milk was first poured into the cup. Fisher devised this test to disprove her claim. The null hypothesis is that the treatments do not affect outcomes, while the alternative hypothesis is that the treatment does affect outcome. To read more about Fisher's exact test, click [here](https://en.wikipedia.org/wiki/Fisher%27s_exact_test).

Let's perform Fisher's exact test on our KickStarter data. We intend to test the hypothesis that the choice of currency has an impact on meeting the pledge goal. We'll start by creating two derived columns in our dataframe. The first will contain 1 if the amount of money in `usd_pledged_real` is greater than the amount of money in `usd_goal_real`. We can compute this by using the `np.where` function. If the amount in one column is greater than the other, enter a value of 1, otherwise enter a value of zero. Add this column to the dataframe and name it `goal_met`.
"""

# Your code here:

kickstarter['goal_met'] = np.where(kickstarter.usd_pledged_real>kickstarter.usd_goal_real, 1, 0)
kickstarter.goal_met.value_counts()

"""Next, create a column that checks whether the currency of the project is in US Dollars. Create a column called `usd` using the `np.where` function where if the currency is US Dollars, assign a value of 1 to the row and 0 otherwise."""

# Your code here:

kickstarter['usd'] = np.where(kickstarter.currency=='USD', 1, 0)
kickstarter.usd

"""Now create a contingency table using the `pd.crosstab` function in the cell below to compare the `goal_met` and `usd` columns.

Import the `fisher_exact` function from `scipy.stats` and conduct the hypothesis test on the contingency table that you have generated above. You can read more about the `fisher_exact` function [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html#scipy.stats.fisher_exact). The output of the function should be the odds ratio and the p-value. The p-value will provide you with the outcome of the test.
"""

# Your code here:
pd.crosstab(kickstarter['goal_met'], kickstarter['usd'])

from scipy.stats import fisher_exact
fisher_exact(pd.crosstab(kickstarter['goal_met'], kickstarter['usd']))

"""# Challenge 2 - The `linalg` submodule

This submodule allows us to perform various linear algebra calculations. 

Using the solve function, find the solution of the equation system 5x + 2y = 3 and 3x + y = 2 in the cell below.
"""

# Your code here:

from numpy import linalg

a = np.array([[5, 2], [3, 1]])
b = np.array([3, 2])

linalg.solve(a, b)

"""# Challenge 3 - The `interpolate` submodule

This submodule allows us to interpolate between two points and create a continuous distribution based on the observed data.

In the cell below, import the `interp1d` function and first take a sample of 10 rows from `kickstarter`.
"""

# Your code here:

from scipy.interpolate import interp1d

samples = kickstarter.sample(n=10, random_state=4)
samples

"""Next, create a linear interpolation of the backers as a function of `usd_pledged_real`. Create a function `f` that generates a linear interpolation of backers as predicted by the amount of real pledged dollars."""

# Your code here:

samples.usd_pledged_real

f = interp1d(samples.backers.sort_values(), samples.usd_pledged_real.sort_values())

"""Now create a new variable called `x_new`. This variable will contain all integers between the minimum number of backers in our sample and the maximum number of backers. The goal here is to take the dataset that contains few obeservations due to sampling and fill all observations with a value using the interpolation function. 

Hint: one option is the `np.arange` function.
"""

# Your code here:
x_new = np.arange(samples.backers.min(), samples.backers.max())
x_new

"""Plot function f for all values of `x_new`. Run the code below."""

# Commented out IPython magic to ensure Python compatibility.
# Run this code:

# %matplotlib inline
import matplotlib.pyplot as plt

plt.plot(x_new, f(x_new))

"""Next create a function that will generate a cubic interpolation function. Name the function `g`"""

# Your code here:
g = interp1d(samples.backers.sort_values(), samples.usd_pledged_real.sort_values(), kind='cubic')

# Run this code:

plt.plot(x_new, g(x_new))

"""# Bonus Challenge - The Binomial Distribution

The binomial distribution allows us to calculate the probability of k successes in n trials for a random variable with two possible outcomes (which we typically label success and failure).  

The probability of success is typically denoted by p and the probability of failure is denoted by 1-p.

The `scipy.stats` submodule contains a `binom` function for computing the probabilites of a random variable with the binomial distribution. You may read more about the binomial distribution [here](https://en.wikipedia.org/wiki/Binomial_distribution) and about the `binom` function [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html#scipy.stats.binom).

In the cell below, compute the probability that a die lands on 5 exactly 3 times in 8 tries.

Hint: the probability of rolling a 5 is 1/6.
"""

# Your code here:


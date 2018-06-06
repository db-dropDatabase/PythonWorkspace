import pandas as pd
from scipy import stats

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]

for city in CITIES:
    reviews = pd.read_csv("./processed/weather/" + city + ".csv")
    cross = pd.crosstab(reviews["stars"], reviews["weather"])
    cross_copy = cross.copy()
    chi2, p, dof, expected = stats.chi2_contingency(cross)

    for x in range(len(expected)):
        for y in range(len(expected[x])):
            cross_copy.iloc[x, y] = expected[x, y]

    cross.to_csv("./processed/weathercounts/" + city + "_observed.csv")
    cross_copy.to_csv("./processed/weathercounts/" + city + "_expected.csv")
    
    print(city)
    print("Chi2: " + str(chi2))
    print("P: " + str(p))
    print("DOF: " + str(dof))
    #print("Expected: " + ", ".join([" ".join([str(val) for val in arr]) for arr in expected]))
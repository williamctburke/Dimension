import xlwings as xw
import warnings
from distributions import DISTRIBUTIONS
import scipy.stats as st
import numpy as np
import sys
def fit_all():
    sht = xw.Book.caller().sheets[0]
    dim_range = sht.range('D3:I3').options(ndim=2, expand='down') # expand allows the range to dynamically include any number of rows
    sht3 = xw.Book.caller().sheets[2] # dimension actual measurements sheet, populated by the user for fitting distributions
    error_rng = sht.range('A1')
    error_rng.value = 'Running'
    for ind in range(0,len(dim_range.value)):
        if dim_range.value[ind][4] != 'fit':
            continue
        data = sht3.range((5,ind+2)).expand('down').value
        if data == None or None in data or len(data) < 2:
            error_rng.value = "Missing data for dimension %d, check 'Dimension Data' sheet column %s" % (ind, chr(ord('B')+ind))
            sys.exit()
        else:
            results = fit(data)
            string = ""
            for i in results:
                string = string + "%f"%i + ","
            sht3.range((2, ind+2)).value = string[:-1]
            sht3.range((3, ind+2)).value = DISTRIBUTIONS[results[0]].name
            ind += 1
    error_rng.value = 'Ready'

def fit(rng):
    bin_count = round(rng[0])
    data = rng[1:]
    y, x = np.histogram(data, bins=bin_count, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0 # get the midpoint of each bin


    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:
        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (DISTRIBUTIONS.index(best_distribution),) + best_params

if __name__ == "__main__":
    # Used when running from Python
    xw.Book('Dimension_standalone.xlsm').set_mock_caller()
    # Used for frozen executable
    fit_all()
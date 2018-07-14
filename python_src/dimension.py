import xlwings as xw
import numpy as np
import warnings
import scipy.stats as st

class Dimension:
    sample_count = 100000
    def __init__(self, name, dim, tol, sigma=3, dist = "normal", shift = 0):
        # basic attributes
        self.name = name
        self.dim = dim
        self.tol = tol
        if sigma == None:
            sigma = 3
        self.sigma = sigma
        self.stddev = self.tol / self.sigma
        if dist == None:
            dist = "normal"
        self.dist = dist
        if shift == None:
            shift = 0
        self.shift = shift
    def __str__(self):
        return str("Dimension Object Named: " + self.name)
    def set_sample(self,n):
        Dimension.sample_count = n
        if self.dist == "normal":
            s = st.norm.rvs(loc = self.dim, scale = self.stddev, size = n)
        elif self.dist == "fit":
            s = best_fit_distribution(data)
        self.s = tuple(s)
        self.shifted = [e + self.shift*self.sigma for e in self.s]
    def set_shift(self, shift=1.5):
        self.shift = shift
        self.set_sample()
    def get_sample(self):
        return self.shifted
    def get_noshift_sample(self):
        return self.s

    # Create models from data
    def best_fit_distribution(data, n):
        """Model data by finding best fit distribution to data"""
        # Read input from sheet
        sht = xw.Book.caller().sheets[2] # dimension data sheet, filled with observations

        # Get histogram of original data
        y, x = np.histogram(data, bins=bins, density=True)
        x = (x + np.roll(x, -1))[:-1] / 2.0

        # Distributions to check
        DISTRIBUTIONS = [        
            st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
            st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
            st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
            st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
            st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
            st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
            st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
            st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
            st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
            st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
        ]

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

        return best_distribution.rvs(*best_params, size = n)
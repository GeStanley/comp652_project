__author__ = 'geoffrey'


import pymc

from pymc.examples import disaster_model


if __name__ == '__main__':
    print 'starting computation for ...'


    M = pymc.MCMC(disaster_model)

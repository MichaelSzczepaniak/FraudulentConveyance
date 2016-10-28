import numpy as np, pandas as pd, scipy.stats as ss

def compareTwoRegSlopes(x1, y1, x2, y2, alpha=0.05, tail_type="both"):
    """ Performs a simple linear regression of y1 vs. x1 and y2 vs. x2
    and then does a test as to whether the difference in the slopes are
    significant.
    
    Parameters:
    x1 - array of floats or ints representing the independent variable
         of the first regression
    y1 - array of floats or ints representing the dependent variable
         of the first regression
    x2 - array of floats or ints representing the independent variable
         of the second regression
    y2 - array of floats or ints representing the dependent variable
         of the second regression
    alpha - float: type II error rate, (1 - confidence)
    tail_type - string: describes the kind of test to perform.
                acceptable values: "left", "right", "both"
    
    Returns a dictionary with the following keys and their assoc'd values:
    n1 - The number of (x1, y1) pairs.
    n2 - The number of (x2, y2) pairs
    w0_1 - Value of the intercept for the simple linear regression y1 vs. x1
    w0_2 - Value of the intercept for the simple linear regression y2 vs. x2
    w1_1 - Value of the slope for the simple linear regression y1 vs. x1
    w1_2 - Value of the slope for the simple linear regression y2 vs. x2
    sx1 - Std deviation of the x1 array.
    sx2 - Std deviation of the x2 array.
    sy1 - Std deviation of the y1 array.
    sy2 - Std deviation of the y2 array.
    r2_1 - Coefficient of determination for y1 vs. x1 linear regression
    r2_2 - Coefficient of determination for y2 vs. x2 linear regression
    syx1 - Std error of the estimate for y1 vs. x1 linear regression
    syx2 - Std error of the estimate for y2 vs. x2 linear regression
    sw1_1 - Std deviation of slope estimate for y1 vs. x1 linear regression
    sw1_2 - Std deviation of slope estimate for y1 vs. x1 linear regression
    s_slope_diff - Std error of difference in the slopes (w1_1 - w1_2)
    t_stat - t statistic for the dual slope test
    df - degrees of freedom for the slope test = n1 - n2 - 4
    p_val - 
    sig - boolean, True if the slopes are different enough to reject the
          null hypothesis or False if they are not.
          
    Reference: http://www.real-statistics.com/regression/hypothesis-testing-significance-regression-line-slope/comparing-slopes-two-independent-samples/
    """
    result = {}
    result['n1'] = len(x1)
    result['n2'] = len(x2)
    result['w0_1'] = trainLinear(x1, y1)[0][0]
    result['w0_2'] = trainLinear(x2, y2)[0][0]
    result['w1_1'] = trainLinear(x1, y1)[1][0]
    result['w1_2'] = trainLinear(x2, y2)[1][0]
    # result['sx1'] = np.std(x1, ddof=1)
    # result['sx2'] = np.std(x2, ddof=1)
    # result['sy1'] = np.std(y1, ddof=1)
    # result['sy2'] = np.std(y2, ddof=1)
    # result['r2_1'] = np.corrcoef(x1.T, y1.T)[1][0]**2
    # result['r2_2'] = np.corrcoef(x2.T, y2.T)[1][0]**2
    # result['syx1'] = result['sy1'] * np.sqrt((1-result['r2_1'])*
                     # (result['n1']-1)/(result['n1']-2))
    # result['syx2'] = result['sy2'] * np.sqrt((1-result['r2_2'])*
                     # (result['n2']-1)/(result['n2']-2))
    # result['sw1_1'] = result['syx1'] / \
                      # (result['sx1'] * np.sqrt(result['n1']-1))
    # result['sw1_2'] = result['syx2'] / \
                      # (result['sx2'] * np.sqrt(result['n2']-1))
    # result['s_slope_diff'] = np.sqrt(result['sw1_1']**2 + result['sw1_2']**2)
    # result['t_stat'] = (result['w1_1'] - result['w1_2']) / \
                       # result['s_slope_diff']
    # result['df'] = result['n1'] + result['n2'] - 4
    # if tail_type == 'right':
        # result['p_val'] = 1 - ss.t.cdf(abs(result['t_stat'], result['df']))
    # else:
        # result['p_val'] = ss.t.cdf(result['t_stat'], result['df'])
        # if tail_type == 'both':
            # result['p_val'] += result['p_val']
        # result['sig'] = (result['p_val'] <= alpha)
    
    return result
    
def loadTestData():
    test_data = {}
    try:
        men_data = pd.read_csv('https://raw.githubusercontent.com/MichaelSzczepaniak/SlopeInference/master/men_cig_life_exp.csv')
        women_data = pd.read_csv('https://raw.githubusercontent.com/MichaelSzczepaniak/SlopeInference/master/women_cig_life_exp.csv')
    except:
        men_data = pd.read_csv('https://www.dropbox.com/s/te8narzivsj5c8f/men_cig_life_exp.csv?dl=1')
        women_data = pd.read_csv('https://www.dropbox.com/s/ju2g6eetfcomhsc/women_cig_life_exp.csv?dl=1')
        
    test_data['x1'] = np.array(men_data['cig_x'])[:, np.newaxis]
    test_data['y1'] = np.array(men_data['life_exp'])[:, np.newaxis]
    test_data['x2'] = np.array(women_data['cig_x'])[:, np.newaxis]
    test_data['y2'] = np.array(women_data['life_exp'])[:, np.newaxis]
    
    return test_data
    
def trainLinear(X, T):
    """ Returns a (D+1, k) column vector of weights for the linear regression of
    T vs. X.  Parameters:
    X is a n by D matrix of features, n = number of samples, D = dimensions (feature count)
    T is a n by k matrix of targets, n = number of samples, k = number of targets
    """
    X1 = np.hstack((np.ones((len(X), 1)), X))  # N x 1 vector of 1's hstack with X
    w = np.linalg.lstsq(np.dot(X1.T,X1), np.dot(X1.T, T))
    
    return w[0]

def useLinear(x, w, transpose_weights=False):
    """ Returns a (n, k) matrix of linear regression targets.  Where
    x is a n by D matrix of features, n = number of samples, D = dimensions (feature count)
    w is a (D+1, k) matrix of weights
    """
    x1 = np.hstack((np.ones((len(x), 1)), x))  # N x 1 vector of 1's hstack with X
    if(transpose_weights):
        return np.dot(x1, w.T)
    else:
        return np.dot(x1, w)

#if __name__ == '__main__': main()
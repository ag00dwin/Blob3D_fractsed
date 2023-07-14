'''
MODULE: CUMULATIVE VOLUME FRACTION 

plots the cumulative volume fraction plot against grainsize within 
a defined range and with a defined bin size. 
    - fits a cumulative Rosin-Rammler distribution function 
    - fits a cumulative Generalised Gamma distribution function
        [ can print the values of the best fit of these functions ]
    
prerequisites
-----
    numpy
    seaborn

    matplotlib.pyplot

    scipy
        scipy.optimize import least_squares, curve_fit
        scipy.special import gamma, factorial, gammainc
        scipy.stats import gengamma
        

input
-----
    ''_df is a pandas dataframe converted from imported Blob3D excel output''
    ''_df_2 is a pandas dataframe converted from imported Blob3D excel output''
        (1) setting _df_2 == None 
            - this will run the module with just one dataframe as normal
        (2) setting _df_2 == Blob3D excel pandas dataframe 
            - this will try to combine the dataframes using the threshold values, atumatoically assuming 
              everything from the first dataframe '_df' is above the threshold and the second dataframe 
              '_df_2' is from below the threshold. 
                ''threshold'' defines the valued explained above
                ''c_min'' and ''c_max'' define a window to compare the two dataframes. Over this overlap, 
                '_df_2' will be modified by a multiplication factor so that it contains the same number of 
                clasts present in the same window in '_df'. Ideally 'threshold' will lie between 'c_min'
                and 'c_max'   

output
-----
    umulative volume fraction plot against (log) grain diameter

'''

def cumvol_fit(_df,_df_2,c_min,c_max,threshold):

    import numpy as np 
    
    import scipy
    from scipy.optimize import least_squares, curve_fit
    from scipy.special import gamma, factorial, gammainc
    from scipy.stats import gengamma

    import matplotlib.pyplot as plt

    #import warnings
    #warnings.filterwarnings("ignore")

    def clastsieve(D,V, _min, _max, step):

        '''
        clast 'sieve'

        D is a np.array of grain diameters
        V is a np.array of grain volumes

        _min is min clast size to sort 
        _max is max clast size to sort 
        step is the bin width between the _min and _max values
        '''

        import numpy as np

        _min = _min
        _max = _max
        bins = (np.arange(_min, _max, step))
    
        # store output in array
        _totals_ = np.zeros((3,int(len(bins))))
        # rows
        # 0 = mass 
        # 1 = number
        # 2 = list of all sizes
        # 3 = bin names

        # itterate over clasts and sort
        for index, value in enumerate(D): 
            _itt_ = np.zeros((3,int(len(bins))))

            for bottom, name in enumerate(bins):
                if bins[bottom]<=value<(bins[bottom]+step):
                    _itt_[0][bottom] = V[index]
                    _itt_[1][bottom] = 1
                    _itt_[2][bottom] = value
            
            _totals_=np.add(_totals_,_itt_)

        # stack array 
        _totals_ = np.vstack([_totals_, bins])
        # set arrays to export
        freq_vol   = _totals_[0,:]
        sum_vol    = _totals_[1,:]
        grainsizes = _totals_[2,:]
        bins       = _totals_[3,:]

        return freq_vol, sum_vol, grainsizes, bins
    def normalize(data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    # create arrays for volume (v) and clast radius
    v = _df[(_df['Side contact']==0)]['Volume (mm^3)'].values
    R = _df[(_df['Side contact']==0)]['ShapeC (mm)'].values
    r = _df[(_df['Side contact']==0)]['ShapeC (mm)'].values
    
    # remove overlapping values
    r_under_threshold = [i for i,m in enumerate(r) if m > threshold]
    r = np.delete(r,r_under_threshold)
    v = np.delete(v,r_under_threshold)
    
    _min_grainsize   = 0.01 
    _max_grainsize   = 5
    _grainsize_step  = 0.015
    
    vol    = np.array(clastsieve(r,v, _min = _min_grainsize, _max =_max_grainsize, step = _grainsize_step)[0])
    num    = np.array(clastsieve(r,v, _min = _min_grainsize, _max =_max_grainsize, step = _grainsize_step)[1])
    bins   = np.array(clastsieve(r,v, _min = _min_grainsize, _max =_max_grainsize, step = _grainsize_step)[3])

    # estimate overlap
    overlap_value = 0
    for index, value in enumerate(R): 
        if c_min < value <=c_max:
            overlap_value = overlap_value+1
  
    # combine with second dataframe
    # if second dataframe is present
    if type(_df_2) != type(None):
        v_2 = _df_2[(_df_2['Side contact']==0)]['Volume (mm^3)'].values
        r_2 = _df_2[(_df_2['Side contact']==0)]['ShapeC (mm)'].values
  
        overlap_comp_value = 0
        for index, value in enumerate(r_2): 
            if c_min < value <=c_max:
                overlap_comp_value = overlap_comp_value+1  
        # print(overlap_comp_value)
        ratio = overlap_comp_value / overlap_value
        print('ratio= '+str(ratio))

        # remove overlapping values
        r2_over_threshold = [i for i,v in enumerate(r_2) if v <= threshold]
        r_2 = np.delete(r_2,r2_over_threshold)
        v_2 = np.delete(v_2,r2_over_threshold)
        
        # multiply arrays by scaling factor to ensure correct overlap
        vol_2    = np.array(clastsieve(r_2,v_2, _min = _min_grainsize, _max =_max_grainsize, step = _grainsize_step)[0])
        num_2    = np.array(clastsieve(r_2,v_2, _min = _min_grainsize, _max =_max_grainsize, step = _grainsize_step)[1])
        vol = vol*ratio
        num = num*ratio

        # omcbine arrays
        vol = np.add(vol, vol_2)
        num = np.add(num, num_2)

    lowest_numer = 5 # min number of clasts within bin
    low_count = [i for i,m in enumerate(num) if m < lowest_numer]
    # remove bins with fewer than defined numbr of clasts
    vol  = np.delete(vol,low_count)
    bins = np.delete(bins,low_count)
    
    # define x and y values
    # make y cumulative
    Rx = bins   
    Ry = np.cumsum(vol)
    Ry = normalize(Ry)

    ''' --- ROSIN FIT --- '''

    def rosin(x,n,k):
        return 1-np.exp(-1*((x/n)**k))
    def direct_nonlinear_fit(x, y):
        rosin_fit = scipy.optimize.curve_fit(rosin, x, y, [0.1, 1])[0]
        return rosin_fit
    popt = direct_nonlinear_fit(Rx, Ry)
    n = popt[0]
    k = popt[1]

    SSE_rosin    = np.sum((rosin(Rx,n,k) - Ry)**2)
    mean_rosin = n*gamma(1+(1/k)) #median k*(np.log(2)**(1/n))
    var_rosin    = (n**2)*((scipy.special.gamma(1+(2/k), out=None)-(scipy.special.gamma(1+(1/k), out=None)**2))**2) 

    print('rosin',SSE_rosin,n,k,mean_rosin)

    ''' --- GENERALIZED GAMMA FIT --- '''

    def ggamma(x,p,a,c):
        return (gammainc((c/p),((x/a)**p)))/(gamma(c/p))
    def ggamma_fit(x, y):
        gamma_fit = scipy.optimize.curve_fit(ggamma, x, y)[0]
        return gamma_fit

    popt = ggamma_fit(Rx, Ry)
    p = popt[0]
    a = popt[1]
    c = popt[2]

    SSE_ggamma    = np.sum((ggamma(Rx,p,a,c) - Ry)**2)
    mean_ggamma = a*((gamma((c+1)/p))/(gamma(c/p)))
    var_ggamma    = gengamma.var(a, c, loc=0, scale=1)

    print('ggamma',SSE_ggamma,c,p,mean_ggamma, 'a=',a)
    
    # plot
    fig = plt.gcf()
    fig.set_size_inches(8, 4)

    plt.plot(Rx,rosin(Rx,n,k),
                    label=' Rosin',
                    color='green',
                    #linestyle='dashed'
                    zorder=1,
                                        )
    plt.plot(Rx,ggamma(Rx,p,a,c),
                    label=' Generalised Gamma',
                    color='red',
                    #linestyle='dashed'
                    zorder=1,
                                        )

    plt.scatter(Rx,Ry,
                    marker = 'o',
                    s = 5,
                    color='black',
                    zorder=2,
                                        )

    plt.xlabel('Particle radius (mm')
    plt.ylabel('Cumulative volume fraction')

    plt.legend()
    plt.show()

    return None




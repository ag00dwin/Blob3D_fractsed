'''
FRACTUAL PLOT

Log-log cumulative plot of the number of clasts with a diameter d and greater [N(>d)] 
against that clast diameter [d]. Values annotating linear fits are the fractal 
dimension 'D-value'
    
prerequisites
-----
    numpy
    matplotlib.pyplot  

input
-----
    ''_df'' is a pandas dataframe converted from imported Blob3D excel output

output
-----
    Log-log cumulative plot with best-fit of linear gradient denoting the fractal dimension

'''

def fractal_plot(_df):

    import numpy as np
    import matplotlib.pyplot as plt

    def clastsieve(D, V, _min, _max, step):

        '''
        clast 'sieve'

        D is a np.array of clast diameters
        V is a np.array of clast volumes

        _min is min clast size to sort 
        _max is max clast size to sort 
        step is the bin width between the _min and _max values

        outputs array of length dependant on bin width:
            freq_vol, sum_vol, clastsizes, bins
        '''

        import numpy as np

        _min = _min
        _max = _max
        bins = (np.arange(_min, _max, step))
    
        # store output in array
        _totals_ = np.zeros((3,int(len(bins))))
        # rows: 
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
    
    def fractal_dimension(_df,R_min,R_max):

        import numpy as np

        # determine volumen and clast radius
        V = _df[(_df['Side contact']==0)]['Volume (mm^3)'].values
        R = _df[(_df['Side contact']==0)]['ShapeC (mm)'].values
        
        # sieve clasts and create histogram
        _min_   = 0.015
        _max_   = 2.000
        _step_  = 0.015

        total_vol    = np.flip(np.array(clastsieve(R,V, _min = _min_, _max =_max_, step = _step_)[0]))
        num          = np.flip(np.array(clastsieve(R,V, _min = _min_, _max =_max_, step = _step_)[1]))
        bins         = np.flip(np.array(clastsieve(R,V, _min = _min_, _max =_max_, step = _step_)[3]))
        cum          = np.cumsum(num)

        bins    [bins==0] = np.nan
        cum     [cum==0]  = np.nan

        x = np.log10(bins)
        y = np.where(cum != 0, np.log10(cum), 0)

        # constrain plot within given x limits
        # remove values outside of these limits
        indexs = []
        for index,value in enumerate(x):
            if value <= R_min or value >=R_max:
                    indexs.append(index)
        x  = np.delete(x, indexs)
        y  = np.delete(y, indexs)

        # fit line to points
        m,c = coef = np.polyfit(x, y, 1)
        fit_func = np.poly1d(coef) 
        # line parameters
        x_fit = np.linspace(R_min, R_max, num=50)
        y_fit = fit_func(x_fit)
        x_center = np.average(x_fit)
        y_center = np.average(y_fit)
        m = round(m,3)

        return x_fit, y_fit, x_center, y_center, m

    # determine volumen and clast radius
    V = _df[(_df['Side contact']==0)]['Volume (mm^3)'].values
    R = _df[(_df['Side contact']==0)]['ShapeC (mm)'].values

    # sieve clasts and create histogram
    _min_   = 0.015
    _max_   = 3.000
    _step_  = 0.005 

    total_vol    = np.flip(np.array(clastsieve(R,V, _min = _min_, _max =_max_, step = _step_)[0]))
    num          = np.flip(np.array(clastsieve(R,V, _min = _min_, _max =_max_, step = _step_)[1]))
    bins         = np.flip(np.array(clastsieve(R,V, _min = _min_, _max =_max_, step = _step_)[3]))
    
    # cumulative number of particles that are bigger than radius defined by bins
    cum = np.cumsum(num)
    bins[bins==0] = np.nan
    cum[cum==0]   = np.nan

    # define plot
    plot_x = np.log10(bins)
    plot_y = np.where(cum != 0, np.log10(cum), 0)
    # plot
    fig, ax = plt.subplots()
    ax.scatter(plot_x,plot_y)
    ax.set(xlabel='log r', ylabel='log N(>R)')

    # plot fractal dimention [D]
    # straight line of best fit where gradient = D
    ax.plot(fractal_dimension(_df,-1,0)[0],fractal_dimension(_df,-1,0)[1],color='red')
    ax.annotate(fractal_dimension(_df,-1,0)[4], xy=(fractal_dimension(_df,-1,0)[2]+0.02, fractal_dimension(_df,-1,0)[3]), fontsize=6)
    
    plt.show(block=True)

    return None


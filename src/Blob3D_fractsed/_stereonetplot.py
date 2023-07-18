'''
STEREONET OF ORIENTATIONS

plots a stereonet of orientation based on sphericity and minimum clast diameter
    
prerequisites
-----
    math
    numpy
    mplstereonet
    matplotlib.pyplot
        

input
-----
    ''_df'' is a pandas dataframe converted from imported Blob3D excel output
    ''st'' is the maximum clast sphericity that is plotted
    ''min_size'' is the minimum clast diameter that is plotted
output
-----
    steronet with kamb contours

'''

def stereonetplot(_df,st,min_size):

    import math
    import numpy as np
    import mplstereonet
    import matplotlib.pyplot as plt

    def plunge_process (L,M,N):
        
        _trend  = []
        _plunge = []

        for index, value in enumerate(L):
            
            _L = L[index]
            _M = M[index]
            _N = N[index]

            plunge = np.rad2deg(-np.arcsin(_N))
            trend = np.rad2deg(np.arccos(_L/np.cos(np.arcsin(_N))))

            if plunge > 0:
                trend = trend-180
                plunge = -plunge
            if trend < 0:
                trend = trend+360
            
            _trend.append(trend)
            _plunge.append(plunge)
        
        _trend = np.nan_to_num(_trend)      
        _plunge= np.nan_to_num(_plunge)

        return _trend, _plunge

    # ensure no zero values
    _df = _df[_df['PEllipsoid X (mm)'] != 0]
    # threshold based on minimum clast size and maximum sphericity
    _df = _df[(_df['Side contact']==0) & (_df['Sphericity']<st) & (_df['ShapeC (mm)']>=min_size)]

    # extract components
    Xl = _df['PEllipsoid X1 (dmls)'].values
    Xm = _df['PEllipsoid X2 (dmls)'].values
    Xn = _df['PEllipsoid X3 (dmls)'].values

    Yl = _df['PEllipsoid Y1 (dmls)'].values
    Ym = _df['PEllipsoid Y2 (dmls)'].values
    Yn = _df['PEllipsoid Y3 (dmls)'].values

    Zl = _df['PEllipsoid Z1 (dmls)'].values
    Zm = _df['PEllipsoid Z2 (dmls)'].values
    Zn = _df['PEllipsoid Z3 (dmls)'].values

    # plot stereonet of orientations
    fig = plt.figure()
    fig.suptitle('no.:'+str(len(Xl)), fontsize=8)
    ax = fig.add_subplot(111, projection='stereonet')
    ax.grid()
    ax.pole(plunge_process(Xl,Xm,Xn)[0]+90,90+plunge_process(Xl,Xm,Xn)[1],'x',color='black')
    ax.density_contourf(plunge_process(Xl,Xm,Xn)[0]+90,90+plunge_process(Xl,Xm,Xn)[1], measurement='poles', cmap='Blues')

    plt.show(block=True)

    return None

'''
CLASTSHAPE [ZINGG] PLOT

plots a Zingg (1935) diagram that shows the relative dimensions of the long, short, and
intermediate axes of a particle

prerequisites
-----
    numpy
    pandas
    seaborn

    matplotlib.pyplot

input
-----
    ''_df'' is a pandas dataframe converted from imported Blob3D excel output
    ''min_size'' is the a threshold of smallest size included in the plot

output
-----
    a Zinng diagram with contours and mean plotted for the dataset

'''

def zingg_diagram(_df,min_size):

    import numpy as np
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt

    # import shape factors 
        # longest particle dimension (ShapeA)
        # longest caliper dimension orthogonal to that (Shape B)
        # caliper dimension orthogonal to those (ShapeC)
        # (projected area and shape calculations)
         
    A_ = _df[(_df['Side contact']==0) & (_df['ShapeC (mm)']>=min_size)]['ShapeA (mm)'].values
    B_ = _df[(_df['Side contact']==0) & (_df['ShapeC (mm)']>=min_size)]['ShapeB (mm)'].values
    C_ = _df[(_df['Side contact']==0) & (_df['ShapeC (mm)']>=min_size)]['ShapeC (mm)'].values
    # combine arrays into a pandas dataframe
    _x = C_/B_
    _y = B_/A_
    df_shape = pd.DataFrame.from_dict(np.array([_x,_y]).T)
    df_shape.columns = ['X','Y']

    # set number of clasts
    number_grains = len(A_)

    # calculate ratios for the zinng diagram
    S_I = np.average(C_/B_)
    I_L = np.average(B_/A_)
    # print average values
    print(' S/I: '+str(S_I)+' I/L: '+str(I_L)+' no: '+str(len(A_)))
    # plot
    sns.kdeplot(   
                    df_shape['X'],  # short/intermed
                    df_shape['Y'],  # intermed/long
                    cmap = "Reds",  # contour colour
                    cbar = True,    # show colour map for contours
                    #shade=True,
                    #bw_adjust=0.5,
                    #levels = np.arange(0,1,0.05)  # 5% intervals
                                        )
    # plot mean
    plt.scatter(S_I,I_L, color = 'black')
    # add lines to denote particle shape boundaries
    plt.axvline(0.67, 0,1, color = 'black',linestyle='dashed')
    plt.axhline(0.67, 0,1, color = 'black',linestyle='dashed')
    # set title
    plt.title(' |min size: '+str(min_size)+' |no.: '+str(number_grains))
    # set plot limits
    plt.xlim(0,1)
    plt.xlabel('S/I', fontsize=16) 
    plt.ylim(0,1)
    plt.ylabel('I/L', fontsize=16)
    plt.gca().set_aspect('equal', adjustable='box')  

    # figure settings
    plt.tight_layout()
    plt.show(block=True)

    return None




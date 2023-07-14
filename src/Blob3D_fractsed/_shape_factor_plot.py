'''
MODULE: GRAINSHAPE [ ZINGG]

plots shape factor as defined by Wilson and Huang (1979): (ShapeB+ShapeC)/2*ShapeA against grain diameter

prerequisites
-----
    numpy
    seaborn

    matplotlib.pyplot

input
-----
    ''_df is a pandas dataframe converted from imported Blob3D excel output''
    ''min_size'' is the a threshold of smallest size included in the plot

output
-----
    a scatter plot of shape factor against (log) grain diameter

'''

def shape_factor_plot(_df1,min_size1):

    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    lab1 = 'A'
    lab2 = 'B'
    
    # plot 1
    varA1_ = _df1[_df1['ShapeC (mm)']>=min_size1]['ShapeC (mm)'].values
    varA2_ = _df1[_df1['ShapeC (mm)']>=min_size1]['Shape Factor(WH79)'].values
    # Calculate the point density
    from scipy.stats import gaussian_kde
    Axy = np.vstack([varA1_,varA2_])
    Az = gaussian_kde(Axy)(Axy)
    # plot
    plt.scatter(varA1_,varA2_,cmap='winter' ,s=10, label=str(lab1),c=Az)
    plt.colorbar(orientation="vertical")
    # set plot limits
    plt.ylim(0.2,1)
    plt.xlim(0.01)
    plt.xscale('log')
    plt.legend(loc='lower right')
    plt.xlabel('Grain diameter (mm)')
    plt.ylabel('Shape factor; Wilson and Huang (1979)')
    # figure settings
    #fig = plt.gcf()
    #fig.set_size_inches(10, 6)
    plt.show(block=True)

    return None




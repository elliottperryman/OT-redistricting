from scipy.ndimage import gaussian_filter

def solve_discrete_gaus(sigma, state: State, centers=None) -> District:
    """
    solve the discrete optimal transport problem
        * df is the dataframe with cols 'pop' and 'geometry'
        * state_geometry is obvious
        * K is number of centers
        * centers are the optional centers
    returns:
        * the sinkhorn results, the agglomerated result, the approximated cost 
    """

    if centers is None:
        centers = sample_rand(state.df, state.num_districts)
    K = state.num_districts
    centroids = state.df['centroid']
    # apply Gaussian smoothing to population density
    a_smooth = gaussian_filter(state.df['pop'].values, sigma=sigma)
    # calculate cost matrix 0.23
    C = np.array([centroids.distance(p) for p in centers]).T
    C /= np.max(C)
    # fill in densities
    a, b = a_smooth, np.ones(K)/K
    # solve sinkhorn
    res = sinkhorn(C, a, b)
    # calculate centroids weighted by population or not!
    x, y = centroids.x.values, centroids.y.values
    normFactor = (state.df['pop'].values.reshape(-1,1)*res).sum(0)
    center_x = np.sum((x * a_smooth).reshape(-1,1) * res / normFactor, 0)
    center_y = np.sum((y * a_smooth).reshape(-1,1) * res / normFactor, 0)
    centers = GeoSeries([Point([a,b]) for a,b in zip(center_x,center_y)])
    district = District(state, res, centers)
    return district
This package can be used for spatial clustering of continuous trajectories. It only needs to provide the latitude and longitude information sorted by positioning time and positioning time to find the dwell point of the trajectory.

The input data is in DataFrame format, and the column names must be ['longitude', 'latitude', 'positioning_time'].

eps is the minimum number of clusters, and min_time is the clustering interval time.
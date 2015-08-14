from osgeo import ogr
import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
from matplotlib import cm
import shapefile
import sys
import matplotlib
import scipy.ndimage as nd
import collections
import pylab as plt
import csv
def main():
    matplotlib.style.use('ggplot')

    mpl.rcParams['font.size'] = 12.
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['axes.labelsize'] = 8
    mpl.rcParams['xtick.labelsize'] = 6.
    mpl.rcParams['ytick.labelsize'] = 6.
     
    fig = plt.figure(figsize=(14.0, 14.0))
    fig.suptitle("Temporal Snapshots of Climate Stations with a 25km Buffer Radius\nwithin New England", fontsize=20)
    # ax = plt.subplot(211)

    #Custom adjust of the subplots
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.5,hspace=0.05)

    map1 = Basemap(projection='merc',llcrnrlat=40.2,urcrnrlat=47.7,\
                llcrnrlon=-74.8,urcrnrlon=-66.5,lat_ts=20,resolution='l')
    


    filesadd = [['pre_1899_dissolve_clip_one.shp', 'new_hampshire.shp', 'Curio_outline.shp'], ['1900_1924_dissolve_clip_one.shp', 'new_hampshire.shp', 'Curio_outline.shp'],
    ['1925_1949_dissolve_clip_one.shp', 'new_hampshire.shp', 'Curio_outline.shp'], ['1950_1974_dissolve_clip_one.shp', 'new_hampshire.shp', 'Curio_outline.shp'],
    ['1975_1999_dissolve_clip_one.shp', 'new_hampshire.shp', 'Curio_outline.shp'], ['after_2000_dissolve_clip_one.shp', 'new_hampshire.shp', 'Curio_outline.shp']]
    count = 0
    count2 = 0
    for hmm in filesadd:
        for testing in hmm:

            # Extract first layer of features from shapefile using OGR
            ds = ogr.Open('shapefiles/' + testing)
            nlay = ds.GetLayerCount()
            lyr = ds.GetLayer(0)

            # Get extent and calculate buffer size
            ext = lyr.GetExtent()
            xoff = (ext[1]-ext[0])/50
            yoff = (ext[3]-ext[2])/50

            if count2 % 3 == 0:
                if count2 == 17:
                    del count
                count += 1
            count2 += 1
            # Prepare figure
            ax = fig.add_subplot(2,3,count)
            plt.subplots_adjust(hspace=0.2)
            ax.set_xlim(ext[0]-xoff,ext[1]+xoff)
            ax.set_ylim(ext[2]-yoff,ext[3]+yoff)


            paths = []
            lyr.ResetReading()

            # Read all features in layer and store as paths
            for feat in lyr:
                for geom in feat.GetGeometryRef():
                    # check if geom is polygon
                    if geom.GetGeometryType() == ogr.wkbPolygon:
                        codes = []
                        all_x = []
                        all_y = []
                        for i in range(geom.GetGeometryCount()):
                            # Read ring geometry and create path
                            r = geom.GetGeometryRef(i)
                            x = [r.GetX(j) for j in range(r.GetPointCount())]
                            y = [r.GetY(j) for j in range(r.GetPointCount())]
                            # skip boundary between individual rings
                            codes += [mpath.Path.MOVETO] + \
                                         (len(x)-1)*[mpath.Path.LINETO]
                            all_x += x
                            all_y += y
                        path = mpath.Path(np.column_stack((all_x,all_y)), codes)
                        paths.append(path)
            
            
            if testing != 'Curio_outline.shp' and testing != 'new_hampshire.shp':
                # Add paths as patches to axes
                for path in paths:
                    patch = mpatches.PathPatch(path, \
                            facecolor='#8da0cb')
                    ax.add_patch(patch)
                ax.set_aspect(1.0)
            else:
                        # Add paths as patches to axes
                for path in paths:
                    patch = mpatches.PathPatch(path, \
                            linewidth=.75, edgecolor='#606060', facecolor='#606060', fill=False, antialiased=1)
                    ax.add_patch(patch)
                ax.set_aspect(1.0)


            fileTitle = ['Pre 1899','1900 to 1924','1925 to 1949','1950 to 1974','1975 to 1999','After 2000']
            plt.title(fileTitle[count -1]) 


        # filename = 'map_only_newEngland2.csv'
        # lats, lons = [], []
        # with open(filename) as f:
        #     reader = csv.reader(f)
        #     next(reader)
        #     for row in reader:
        #         lats.append(float(row[4]))
        #         lons.append(float(row[5]))
        # x,y = map1(lons, lats)
        # map1.plot(x, y, 'ro', markersize=30)


    plt.savefig('Climate_Station_Distribution',dpi=72)
    plt.show()

# def mappingPoint(m):
#     # Open the earthquake data file.
#     filename = 'map_only_newEngland2.csv'

#     # Create empty lists for the latitudes and longitudes.
#     lats, lons = [], []

#     # Read through the entire file, skip the first line,
#     #  and pull out just the lats and lons.
#     with open(filename) as f:
#         # Create a csv reader object.
#         reader = csv.reader(f)
        
#         # Ignore the header row.
#         next(reader)
        
#         # Store the latitudes and longitudes in the appropriate lists.
#         for row in reader:
#             lats.append(float(row[4]))
#             lons.append(float(row[5]))

#     x,y = m(lons, lats)
#     return m.plot(x, y, 'ro', markersize=6)
if __name__ == '__main__':
  main()
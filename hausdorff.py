# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 14:52:36 2020

@author: banbar
"""

import geopandas as gp
from osgeo import ogr
import sys
import numpy as np
import json
from shapely.geometry import Polygon, Point

# Open the shp file
# Second argument tell whether to read (0, default), or to update (1)
# ds stands for "Data Source"

# Source A (OSM):

df_A = gp.read_file('/data/polygonss_hausdorff/A.shp')

df_B = gp.read_file('/data/polygonss_hausdorff/B.shp')
  

def hausdorff(df_A, df_B):
    num_polygons = len(df_A)
    hausdorff = [-1] * num_polygons
    
    for poly_A in range(len(df_A)):
        # Convert the polygon into a geoseries onject
        geoseries_A = gp.GeoSeries(df_A['geometry'][poly_A])
        
        for poly_B in range(len(df_B)):
            # We can hold a VISITED polygon list - we can skip those to improve the run-time
            
            # Both polygons must represent the same object - we focus on 1-1 polygon matches
            if(df_A['id'][poly_A] == df_B['id'][poly_B]):  
                
                print("\n\nSame polygons with id", df_A['id'][poly_A] )
                
                # Convert the polygon into a geoseries onject
                geoseries_B = gp.GeoSeries(df_B['geometry'][poly_B])
                #print(geoseries_B)
                
                # vertices of A  -> to -> polygon B
                # For all the vertices of A:
                print("vertices of A  -> to -> polygon B")
                num_vertices_A = len(df_A['geometry'][poly_A].exterior.coords) # obtain the number of vertices
                num_vertices_B = len(df_B['geometry'][poly_B].exterior.coords) # obtain the number of vertices
                print("Num of vertices A: ", num_vertices_A-1)
                dist_A = 0
                
                min_dist = [9999]*num_vertices_A
                
                for v in range(num_vertices_A):
                    # Convert each vertice to a GeoSeries point object:
                    vertex_A = gp.GeoSeries(Point(df_A['geometry'][poly_A].exterior.coords[v]))
                    closest_dist = min_dist[0]
                    for z in range(num_vertices_B):
                        vertex_B = gp.GeoSeries(Point(df_B['geometry'][poly_B].exterior.coords[z]))
                        
                        # distance between two vertices
                        dist_between_two_vertices = vertex_A.distance(vertex_B)
                        
                        if(dist_between_two_vertices[0] < closest_dist):
                            closest_dist = dist_between_two_vertices[0]
                    
                    min_dist[v] = closest_dist
                
                hausdorff[poly_A] = max(min_dist)
    return hausdorff

h = hausdorff(df_A, df_B)
                
                        
                        
                        




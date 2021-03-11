#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 3 22:48:36 2021

@author: Carlos Gómez-Huélamo

Code to 

Communications are based on ROS (Robot Operating Sytem)

Inputs: 
Outputs: 

Note that 

"""

import math
import numpy as np
import pandas as pd
import os

from argparse import ArgumentParser

# Global variables

N = 100 # Number of pseudoscenarios
STD_DEV = 0.8 # Standard deviation
max_theta_dev = 3/5 # Maximum orientation deviation w.r.t. original angle
uniform = True

def generate_random_parameters(mean_values, folder, name):
    """
    Generate random parameters around the provided mean
    """

    mean_values_dict = dict([tuple(m.strip() for m in mn.split(':')) for mn in mean_values.split(',')])
 
    df = pd.DataFrame(np.zeros((N,len(mean_values_dict))), columns=list(mean_values_dict.keys()))

    for column in df:
        mean_value = float(mean_values_dict[column])
        
        if 'theta' in column:
            if uniform:
                min_value = mean_value - max_theta_dev*math.pi/2
                max_value = mean_value + max_theta_dev*math.pi/2
                df[column] = np.random.uniform(min_value,max_value,N)
            else:
                df[column] = np.random.normal(mean_value, STD_DEV, N)
                df.loc[df[column] > mean_value + max_theta_dev*math.pi/2, column] = mean_value + max_theta_dev*math.pi/2
                df.loc[df[column] < mean_value - max_theta_dev*math.pi/2, column] = mean_value - max_theta_dev*math.pi/2
        else:
            df[column] = np.random.normal(mean_value, STD_DEV, N)

    path = os.path.join(folder + '/' + name + '.csv')
    print("path: ", path)
    df.to_csv(path,index=False)

def main(args):
    """
    """
    generate_random_parameters(args.openscenarioparams, args.folder, args.database_name)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--openscenarioparams', help='Overwrite the specified OpenSCENARIO parameters in ParameterDeclaration')
    parser.add_argument('--database_name', help="Specify the name of the database", default="general-purpose")
    parser.add_argument('--folder', help='Specify the folder to generate the database', default=".")
    
    args = parser.parse_args()
    
    main(args)

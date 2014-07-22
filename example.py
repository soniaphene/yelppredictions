
from __future__ import division
import pico

import argparse
import random
import sqlite3
import json
import operator
import numpy


#             0         1         2      3    4      5       6       7
#format: business_id, name, # checkins, lat, lon, labels, test_id, ratings

CROSS_VALIDATION_NUM = 10
NUM_NEIGHBORS = 30

LAT_RANGE = .01 #the best was .06
LON_RANGE = .01

def calculate(lat,lon,categories):
    global labels_full_abrev
    labels = []
    for line in open('categories.txt'):
        names = line.split('(')
        labels.append(map(lambda x: x.replace(')', '').strip(), names))

    labels_full_abrev = zip(*labels) # [(full_lables),(abrev_labels)]

    c = sqlite3.connect('rating.db')

    with c: #close resources and provide error handling

            cursor = c.cursor()    
            cursor.execute("SELECT * FROM businesses WHERE lat>={0} and lat<={1} and lon>={2} and lon <={3}"
                .format(lat-LAT_RANGE,lat+LAT_RANGE,lon-LON_RANGE,lon+LON_RANGE))

            nearby_businesses = cursor.fetchall()
            labels = map(get_category_id, categories)

            closeness={} #dictionary where key is business_id and value is list of form number of categories in common, ratings
            for b in nearby_businesses:
                b_labels = json.loads(b[5])
                shared=len(filter(lambda x: x in labels, b_labels))
                if(shared!= 0): #they share at least one label
                    closeness[b[0]]=[shared,b[7]] #makes it have a list
                    #a+=1
            # return len(nearby_businesses)
            # return a
            sorts=sorted(closeness.items(),key=lambda x:x[1][0],reverse=True)
            if len(sorts)<NUM_NEIGHBORS:
                top_cats=sorts
            else:
                top_cats=sorts[0:NUM_NEIGHBORS]
            #return len(top_cats)
            if len(top_cats)!=0:
                prediction=evaluate_heuristic(top_cats)
                return "Your result is: " + str(prediction) + ' stars'
            else:
                return "Sorry, there were no similar businesses in the area you chose."



def evaluate_heuristic(top_list):
    max_close=0
    total_ratings=0
    total_businesses=0
    for a in top_list:
        max_close=max(max_close,a[1][1])
    for i in top_list:
        total_ratings += i[1][1]*i[1][0]/max_close
        total_businesses += i[1][0]/max_close

    return float(total_ratings)/total_businesses


#labels_full_abrev = [full_names, nick_names]
#full_names = [list of categories]
def get_category_id(category):
    if category in labels_full_abrev[0]:
        return labels_full_abrev[0].index(category)
    elif category in labels_full_abrev[1]:
        return labels_full_abrev[1].index(category)
    else:
        return -1

def hello():
    print "nooooo"
    return "What up suckers!\ngo home\nyay\n"



def get_stars(mystring,go,array):
    return "why"+mystring+go+str(len(array))



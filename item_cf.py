# Starter code for item-based collaborative filtering
# Complete the function item_based_cf below. Do not change its name, arguments and return variables. 
# Do not change main() function, 

# import modules you need here.
import numpy as np
import numpy.matlib
import csv
import math
import sys
import scipy
import scipy.stats
from q4_new import *


def item_based_cf(datafile, user, movie, metric, K, iFlag, numOfUsers, numOfItems):

    # read in system arguments, first the csv file, max degree fit, number of folds, verbose
    rfile = datafile

    csvfile = open(rfile, 'rb')
    dat = csv.reader(csvfile, delimiter='\t')
    dat = list(dat)
    userID = []
    movieID = []
    ratings = []

    for i, row in enumerate(dat):
        if i >= 0:
            userID.append(int(row[0]))
            movieID.append(int(row[1]))
            ratings.append(int(row[2]))
            # if user == int(row[0]) and movie == int(row[1]):
            #     truerating = int(row[2])
    userID = np.unique(np.array(userID))
    movieID = np.unique(np.array(movieID))
    ratings = np.array(ratings)


    util_matrix = (len(userID) + 1, len(movieID) + 1)
    util_matrix = np.matrix(np.matlib.zeros(util_matrix))

    # print util_matrix.size
    rows = util_matrix.shape[0]
    cols = util_matrix.shape[1]

    util_matrix[0, 0] = 0

    for i in range(1, rows):
        util_matrix[i, 0] = int(userID[i - 1])

    for j in range(1, cols):
        util_matrix[0, j] = int(movieID[j - 1])

    for i, row in enumerate(dat):
        userR = int(row[0])
        movieR = int(row[1])
        pos = np.where(userID == userR)[0][0] + 1
        pos2 = np.where(movieID == movieR)[0][0] + 1

        util_matrix[pos, pos2] = int(row[2])

    # print util_matrix
    #
    # user = 2
    # movie = 2
    # metric = 0
    # K = 10

    user_pos = np.where(userID == user)[0][0] + 1
    movie_pos = np.where(movieID == movie)[0][0] + 1
    # print user_pos
    # print movie_pos

    truerating = util_matrix[user_pos, movie_pos]

    item1_arr = []
    item2_arr = []
    item1_arr = np.array(util_matrix[..., movie_pos])
    # print item1_arr
    #
    # item1 ratings list
    for i in [movie_pos, 0]:  # iterate in order
        item1_arr = np.delete(item1_arr, i)

    # print len(item1_arr)
    # # print "Actual" + str(util_matrix[2,54])

    manhattan_list = {}
    pearson_list = {}

    for i in range(1, cols):

        if i == movie_pos:
            continue
        else:
            item2_arr = np.array(util_matrix[..., i])
            # print item2_arr
            for j in [user_pos, 0]:  # iterate in order
                item2_arr = np.delete(item2_arr, j)
            # print len(item2_arr)

            if metric == 1:
                man_dis = manhattan(item1_arr, item2_arr)
                manhattan_list[util_matrix[0, i]] = man_dis
            else:
                pears_dis = pearson_def(item1_arr, item2_arr)
                pearson_list[util_matrix[0, i]] = pears_dis

    # print manhattan_list
    # print pearson_list
    user_rating = []
    if metric == 1:
        # print len(sorted(manhattan_list.values()))
        for i in sorted(manhattan_list.values())[0:K]:
            movie_key = manhattan_list.keys()[int(i)]
            rating = util_matrix[np.where(user == userID), np.where(movie_key == movieID)[0][0] + 1]
            user_rating.append(rating)
    else:
        # print sorted(pearson_list.values())
        for i in sorted(pearson_list.values())[0:K]:
            movie_key = pearson_list.keys()[int(i)]
            rating = util_matrix[np.where(user == userID), np.where(movie_key == movieID)[0][0] + 1]
            user_rating.append(rating)

    user_rating = np.array(user_rating)
    # print user_rating
    predicted_rating = int(mode(user_rating)[0])

    # print pearson_list
    # print truerating
    # print predicted_rating

    return truerating, predicted_rating


def main():
    datafile = sys.argv[1]
    userid = int(sys.argv[2])
    movieid = int(sys.argv[3])
    distance = int(sys.argv[4])
    k = int(sys.argv[5])
    i = int(sys.argv[6])
    numOfUsers = 943
    numOfItems = 1682

    trueRating, predictedRating = item_based_cf(datafile, userid, movieid, distance, k, i, numOfUsers, numOfItems)
    print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
    .format(userid, movieid, trueRating, predictedRating, distance, k, i)



if __name__ == "__main__":
    main()

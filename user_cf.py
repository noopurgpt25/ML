# Starter code for uesr-based collaborative filtering
# Complete the function user_based_cf below. Do not change it arguments and return variables. 
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

def user_based_cf(datafile, user, movie, metric, K, iFlag, numOfUsers, numOfItems):

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
    userID = np.unique(np.array(userID))
    movieID = np.unique(np.array(movieID))
    ratings = np.array(ratings)
    # data = np.column_stack((userID,movieID,ratings))
    # print len(np.unique(userID))
    # print len(np.unique(movieID))

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
    truerating = util_matrix[user_pos, movie_pos]

    user1_arr = []
    user2_arr = []
    user1_arr = np.array(util_matrix[user_pos])
    # print user1_arr

    # user1 ratings list
    for i in [movie_pos, 0]:  # iterate in order
        user1_arr = np.delete(user1_arr, i)
    # print user1_arr
    # print "Actual" + str(util_matrix[2,54])

    manhattan_list = {}
    pearson_list = {}

    for i in range(1, rows):

        if i == user_pos:
            continue
        else:
            user2_arr = np.array(util_matrix[i])
            for j in [movie_pos, 0]:  # iterate in order
                user2_arr = np.delete(user2_arr, j)
            # print user2_arr

            if metric == 1:
                man_dis = manhattan(user1_arr, user2_arr)
                manhattan_list[util_matrix[i, 0]] = man_dis
            else:
                pears_dis = pearson_def(user1_arr, user2_arr)
                pearson_list[util_matrix[i, 0]] = pears_dis

    user_rating = []
    if metric == 1:
        for i in sorted(manhattan_list.values())[0:K]:
            user_key = manhattan_list.keys()[int(i)]
            rating = util_matrix[np.where(user_key == userID)[0][0] + 1, np.where(movie == movieID)]
            user_rating.append(rating)
    else:
        #print sorted(pearson_list.values())[0:K]
        for i in sorted(pearson_list.values())[0:K]:
            user_key = pearson_list.keys()[int(i)]
            rating = util_matrix[np.where(user_key == userID)[0][0] + 1, np.where(movie == movieID)]
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
    
    trueRating, predictedRating = user_based_cf(datafile, userid, movieid, distance, k, i, numOfUsers, numOfItems)
    print 'userID:{} movieID:{} trueRating:{} predictedRating:{} distance:{} K:{} I:{}'\
    .format(userid, movieid, trueRating, predictedRating, distance, k, i)




if __name__ == "__main__":
    main()
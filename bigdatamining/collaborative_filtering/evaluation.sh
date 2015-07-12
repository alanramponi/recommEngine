#!/usr/bin/bash
###############################################################################
# @authors          Alan Ramponi (151369), Davide Martintoni (171076)
# @courses          Data Mining / Big Data and Social Networks
# @description      A user-based collaborative filtering algorithm
#
# A preprocessing script that indicates the command sequence to execute
###############################################################################


###############################################################################
# STEP 1: SHUFFLE THE ORIGINAL DATASET TO AVOID BAD PARTITIONING.
###############################################################################

PATH="Scrivania/k-fold" # PATH THAT CONTAINS THE DATASET
NAME="reviews_Clothing\,_Shoes_\&_Jewelry.txt" # DATASET TO SPLIT

cd ${PATH} # go to the path
shuf ${NAME} --output=dataset_shuffled.txt # shuffle the dataset lines

wc -l reviews_Clothing\,_Shoes_\&_Jewelry.txt # count lines
# 5752454 reviews_Clothing,_Shoes_&_Jewelry.txt

wc -l dataset_shuffled.txt # count lines
# 5752454 dataset_shuffled.txt


###############################################################################
# STEP 2: CLEAN DATASET FROM ITEMS WITH REVIEWS R < 20.
###############################################################################

python preprocessing_items.py # clean items not relevant
# and then compress again the resulted .txt


###############################################################################
# STEP 3: CLEAN DATASET FROM USERS WITH REVIEWS R < 10.
###############################################################################

python preprocessing_users.py # clean users not relevant


###############################################################################
# STEP 4: SPLIT THE RESULTED DATASET INTO K FOLDS.
###############################################################################

split -l 1150491 dataset_preprocessed.txt dataset_subsample.txt # split into k-folds, with k=5

wc -l dataset_subsample.txtaa # count lines
# 1150491 dataset_subsample.txtaa
wc -l dataset_subsample.txtab # count lines
# 1150491 dataset_subsample.txtab
wc -l dataset_subsample.txtac # count lines
# 1150491 dataset_subsample.txtac
wc -l dataset_subsample.txtad # count lines
# 1150491 dataset_subsample.txtad
wc -l dataset_subsample.txtae # count lines
# 1150490 dataset_subsample.txtae


###############################################################################
# STEP 5: CREATE EACH TRAINING SET FROM OTHER (K-1)-FOLDS.
###############################################################################

# merge other (k-1)-folds, i.e. create the training set
awk '{print > "train_set_2345.txt"}' dataset_subsample.txtab dataset_subsample.txtac dataset_subsample.txtad dataset_subsample.txtae
wc -l train_set_2345.txt # count lines
# 4601963 train_set_2345.txt

# merge other (k-1)-folds, i.e. create the training set
awk '{print > "train_set_1345.txt"}' dataset_subsample.txtaa dataset_subsample.txtac dataset_subsample.txtad dataset_subsample.txtae
wc -l train_set_1345.txt # count lines
# 4601963 train_set_1345.txt

# merge other (k-1)-folds, i.e. create the training set
awk '{print > "train_set_1245.txt"}' dataset_subsample.txtaa dataset_subsample.txtab dataset_subsample.txtad dataset_subsample.txtae
wc -l train_set_1245.txt # count lines
# 4601963 train_set_1245.txt

# merge other (k-1)-folds, i.e. create the training set
awk '{print > "train_set_1235.txt"}' dataset_subsample.txtaa dataset_subsample.txtab dataset_subsample.txtac dataset_subsample.txtae
wc -l train_set_1235.txt # count lines
# 4601963 train_set_1235.txt

# merge other (k-1)-folds, i.e. create the training set
awk '{print > "train_set_1234.txt"}' dataset_subsample.txtaa dataset_subsample.txtab dataset_subsample.txtac dataset_subsample.txtad
wc -l train_set_1234.txt # count lines
# 4601964 train_set_1234.txt


###############################################################################
# STEP 6: ORGANIZE AND COMPRESS FILES FOR NEXT PROCESSING.
###############################################################################

mkdir data_1 data_2 data_3 data_4 data_5 # create needed directories

# rename and organize files into the appropriate directory
mv train_set_2345.txt data_1
mv dataset_subsample.txtaa test_set_1.txt
mv test_set_1.txt data_1

# rename and organize files into the appropriate directory
mv train_set_1345.txt data_2
mv dataset_subsample.txtab test_set_2.txt
mv test_set_2.txt data_2

# rename and organize files into the appropriate directory
mv train_set_1245.txt data_3
mv dataset_subsample.txtac test_set_3.txt
mv test_set_3.txt data_3

# rename and organize files into the appropriate directory
mv train_set_1235.txt data_4
mv dataset_subsample.txtad test_set_4.txt
mv test_set_4.txt data_4

# rename and organize files into the appropriate directory
mv train_set_1234.txt data_5
mv dataset_subsample.txtae test_set_5.txt
mv test_set_5.txt data_5


###############################################################################
# STEP 7: TEST DISTANCES GOODNESS (RMSE) WITH A DESIGNED SCRIPT.
###############################################################################

python evaluate_results.py ID k n # run the evaluation algorithm for test_1
python evaluate_results.py ID k n # run the evaluation algorithm for test_2
python evaluate_results.py ID k n # run the evaluation algorithm for test_3
python evaluate_results.py ID k n # run the evaluation algorithm for test_4
python evaluate_results.py ID k n # run the evaluation algorithm for test_5


###############################################################################
# STEP 8: PLOT THE FINAL RESULTS.
###############################################################################

python plot_results.py # plot the final results
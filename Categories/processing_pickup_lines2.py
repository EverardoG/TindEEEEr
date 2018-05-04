#Importing libraries
import pickle
import os

#creating a list of pickle files in the same directory as this script
def find_pickled_files():
    """Input:Nothing
       Output: A list of pickle files in the same directory as the script

       This function goes through the directory the script is in and creates a
       list of pickled files in the same directory
       """
    directory = os.listdir()
    pickle_files = []
    for filename in directory:
        if filename[-6:] == "pickle":
            pickle_files.append(filename)
    return pickle_files

#turning all of the pickle files into appropriately named dictionaries
def get_dicts(pickle_files):
    """Input: List of pickled files in the same directory
       Output: Dictionary where each key is a category name and each
       value is a dictionary containing pickup lines for that category

       This function goes through a list of pickled files in the same
       directory as the script and creates an appropriately named dictionary
       for each pickled file
       """
    all_dicts = {}
    for pickle_file in pickle_files:

        name = str(pickle_file)[:-7]
        dictionary = pickle.load(open(pickle_file, 'rb'))
        all_dicts[name] = dictionary
    return all_dicts

#!/usr/bin/python3
# Written by Rohit Shukla (Jaypee University of Information Technology, Waknaghat, Solan).
# 12 August 2021
# Please write your suggetions for improvement at shuklarohit815@gmail.com.

import os
import csv
import operator
import glob
import shutil
import argparse

# Defining the variables for command line argument. Here four parameters are defined: two are required and two are optional.
if __name__ == "__main__":
    print("\n            ########################################################################## \n\
            ##                          pyVSvina                                    ## \n\
            ##         Virtual Screening of Ligands using Autodock Vina             ## \n\
            ##                    @Rohit Shukla, August 2021                        ##  \n\
            ##            https://github.com/shuklarohit815/pyVSvina                ## \n\
            ##                  Email: shuklarohit815@gmail.com                     ##  \n\
            ########################################################################## \n")
    parser = argparse.ArgumentParser(description="The program will run the Vina screening using one or multiple compounds. \
    The user can enter the directory path with the -l option. The user should supply configuration file with the -c option \
        which should have all the grid coordinates. If the grid coordinates or receptor or ligands will not be provided \
            in the proper format, so it will give the error and the program will terminate. Hence please read the help and provide the necessary file. Detailed \
                Information about the Autodock Vina software can be accessed from this weblink: http://vina.scripps.edu/. Please cite the AutodockVina.")
    parser.add_argument("-r","--receptor", metavar="", required=True, help="Receptor pdbqt file") 
    parser.add_argument("-c","--config", metavar="", required=True, help="Configuration file with all the grid co-ordinates")
    parser.add_argument("-l", "--ligand", metavar="", required=True, help="Enter the ligand with .pdbqt file or full path of the directory")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--quiet", action = "store_true", help="print_quiet")
    group.add_argument("-v", "--verbose", action = "store_true", help="print_verbose")
    print("Examples:")
    print("")
    print("python3 pyVSvina.py --receptor receptor.pdbqt --conf configuration.txt --ligand single_ligand or ligand_dir")
    print("")
    print("python3 pyVSvina.py -r receptor.pdbqt -c configuration.txt -l single_ligand or ligand_dir")
    print("")
args = parser.parse_args() # the args has all the command line variable

# Defining the file variable
receptor = args.receptor
ligand =args.ligand
config_file = args.config

# it will check that program will execute for one ligand or for folder.
if ".pdbqt" in ligand:
    Lig_dir = None
else:
    Lig_dir = args.ligand # It will assign the folder name in LigDir

# Create an emply list and getting the current directory.
list_lig_ini = []
cwd = os.getcwd()

# If user input will a folder path so this condition will execute and store all the files in a new list.
if type(Lig_dir) == str:
    os.chdir(Lig_dir)
    temp_lis = glob.glob("*.pdbqt")
    list_lig_ini = temp_lis

# The program will come back to its original folder.
os.chdir(cwd)

# The .pdbqt will be removed from the files and all the file_name will be stored in a new list.
list_lig = []
for items in list_lig_ini:
    c = os.path.splitext(items)[0]
    list_lig.append(c)

# A new dictonary is defined which will later used for screening result storage.
summary = {}
count = 1

# Checking the folder existence.
if not os.path.exists("Results"):
    os.makedirs("Results")
if not os.path.exists("Top_10_Compounds_pdbqt_file"):
    os.mkdir("Top_10_Compounds_pdbqt_file")

# The condition will execute when user will enter only one ligand.
if ".pdbqt" in ligand: 
    split_ligand = os.path.splitext(ligand)[0]
    os.system(f"vina --receptor {receptor} --config {config_file} --ligand {split_ligand}.pdbqt --out result_{split_ligand}.pdbqt --log {split_ligand}_log.txt")

# The condition will execute for multiple ligand with folder location.
elif type(list_lig_ini) == list: # The list_lig_ini has all the ligands.pdbqt information
    
    for count, lig in enumerate(list_lig):
        print(f"The screening is running for {lig}. This is completing the ligand number {count+1}.") 
        os.system(f"vina --receptor {receptor} --config {config_file} --ligand {Lig_dir}/{lig}.pdbqt --out Results/{lig}.pdbqt --log Results/{lig}.txt")

# The code will process the file and write the top energy line (first conformation) in the dictonary (summary).    
        ligand_energy = open(f"Results/{lig}.txt")
        ligand_energy_1 = ligand_energy.readlines()
        for items_1 in ligand_energy_1:
            if items_1.startswith("   1"):
                ligand_energy_2 = items_1
                binding_energy = ligand_energy_2.split(" ")[12]
                summary.update({lig : binding_energy})
               
# This code will be executed if dictonary summary have some values and needs to write 10 top ligand information.
if summary != None:
# Will create new files and then write the ligand name and binding energy inside the Summary file.
    with open ("Summary_file.csv" , "w+") as suma:
        for data, value in zip(summary.keys(), summary.values()):
            suma.write(f"{data}, {value}\n") 
    suma.close()

# It will create a new file summary sorted and write the sorted binding energy in the summary sorted for all the compounds.   
    file1 = open("Summary_file.csv")
    summary_sorted = open("Summary_sorted.csv", "w+", newline ='') # Will create a new csv file for sorting
    csv_1 = csv.reader(file1, delimiter = ",") # It will read the csv

# The sorted function will sort the csv_1 file which is created in above rows and returns a list of all the rows
    sort = sorted(csv_1, key=operator.itemgetter(1), reverse= True) # reverse = True will sort in descending order   

# It will write the sort (list) content in the summary sorted by using csv.writer. 
    with summary_sorted:
        write = csv.writer(summary_sorted)
        write.writerows(sort)
# It will make a new foler with the writing permission which will have top 10 compounds and will open the summary sorted.
    with open('Summary_sorted.csv', 'r') as file:
        f = file.readlines()
# It will define an empty list and fill all the lines of f(summary_sorted.csv) in the ten items. 
    ten_items = []
    
    for items in f:
        ten_items.append(items.split(",")[0])

# It will write top ten values in the list_ligands.
    list_ligands = ten_items[0:10]
 
# This for loop will copy the ten items from Results to Top_10_compounds folder. 
    for item_1 in list_ligands:
        shutil.copy(f"Results/{item_1}.pdbqt", "Top_10_Compounds_pdbqt_file") # I got error and resolved with very much efforts, replaced copyfile with copy

# This will create a new file 
    top_10_file = open("top_10_ligands_summary.txt", "w+")
    top_10_file_lis = f[0:10] # copy the ten items from the f list

# It will write the top binding energy in that file.   
    for top in top_10_file_lis:
        top_10_file.write(top)
    x = top_10_file.read()
    top_10_file.close()

# Finally copy the top_10_ligands_summary to the foler Top_10_compounds.
    shutil.move("top_10_ligands_summary.txt", "Top_10_Compounds_pdbqt_file")

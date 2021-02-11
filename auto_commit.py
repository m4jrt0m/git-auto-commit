#!/usr/bin/env python3

import sys
import os
import hashlib
import time
import subprocess

def main(argv):
    print("Starting auto git commit...")

    folder_path = '.'
    find_pattern = ''
    sleep_timer = 5 # 300 sec are 5 min, sleep accepts seconds

    if len(argv) > 1:
        for i in range( len(argv) ):
            if argv[i] == "--folder" and i + 1 != len(argv) :
                folder_path = argv[i + 1]
            if argv[i] == "--find" and i + 1 != len(argv) :
                find_pattern = argv[i + 1]
            if argv[i] == "--timer" and i + 1 != len(argv) :
                sleep_timer = argv[i + 1]
            if argv[i] == "--help" or argv[i] == '-h':
                show_help_info()
                return

    print(f"Looking at {folder_path}")

    files_hash_list = get_current_files_hash(folder_path, find_pattern)

    while True:
        new_hash_list = get_current_files_hash(folder_path, find_pattern)

        if len( files_hash_list ) != len( new_hash_list ):
            # add. commit and push
            git_add_commit_push(folder_path)
        else:
            for i in range( len(files_hash_list) ):
                if (files_hash_list[i] != new_hash_list[i]):
                    # add. commit and push
                    git_add_commit_push(folder_path)
        files_hash_list = new_hash_list     
        time.sleep(int(sleep_timer))  


def get_current_files_hash(folder_path, find_pattern):
    files_hash_list = []
    directories = os.listdir( folder_path )
    for file in directories:
        filedir = os.path.join(folder_path, file)

        if find_pattern != '' :
            if file.find(find_pattern) > -1:
                with open(filedir,"r",encoding='utf-8') as f:
                    data = f.read()
                    files_hash_list.append(hashlib.md5(data.encode()).hexdigest())
        else :
            with open(filedir,"r",encoding='utf-8') as f:
                data = f.read()
                files_hash_list.append(hashlib.md5(data.encode()).hexdigest())

    return files_hash_list

def git_add_commit_push(folder_path):
    current_wd = os.getcwd()
    os.chdir(folder_path)
    subprocess.run( ["git", "add", "."] )
    subprocess.run( ["git", "commit", "-m", "auto commit"] )
    subprocess.run( ["git", "push"] )
    os.chdir(current_wd)
    print("commit done!")

def show_help_info():
    print("""
Auto Commit will help you automate the git commit add and push when files change inside a folder

Options:
--folder    sets the folder to keep an eye on
--find      sets a find pattern to help filter for a type of file
--timer     sets the sleep timer in seconds

e.g.:
python3 auto_commit.py --file <path to folder> --find <file type> --timer <seconds>""")

main(sys.argv)

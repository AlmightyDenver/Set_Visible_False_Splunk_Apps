#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Python = 3.7
# Created By  : DenverAlmighty
# Created Date: 2022-10-24
# Updated Date : 2022-10-24
# version = '1.0.0'
# ---------------------------------------------------------------------------


import tarfile
import os, sys
from os import listdir
from os.path import isdir, isfile, join
import configparser

# mypath = '/Users/denver/Downloads/viz_apps_copy'
mypath = ''

def init_page():
    mystring = '''                         
                                )  (                   )  
 (            )   (      (   ( /(  )\   (           ( /(  
 )\  (       /((  )\  (  )\  )\())((_) ))\          )\()) 
((_) )\     (_))\((_) )\((_)((_)\  _  /((_)        ((_)\  
 (_)((_)    _)((_)(_)((_)(_)| |(_)| |(_))    ___   /  (_) 
 | |(_-<    \ V / | |(_-<| || '_ \| |/ -_)  |___| | () |  
 |_|/__/_____\_/  |_|/__/|_||_.__/|_|\___|  |___|  \__/   
       |_____|                                            

'''
    print(mystring)

# unzip .tgz file
def unzip_tgz(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    tar.extractall()
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            unzip_tgz(item.name, "./" + item.name[:item.name.rfind('/')])
    try:
        unzip_tgz(sys.argv[1] + '.tgz')
    except:
        name = os.path.basename(sys.argv[0])

# add local dir and apps.conf file
def set_visible_false(path):
    #check local dir exists or not
    local_path = join(mypath, path, 'local')
    
    #if not exists local dir, make dir
    if not os.path.exists(local_path):
        os.mkdir(local_path)
        
    #add apps.conf file
    file_path = join(local_path, 'apps.conf')
    #set config
    config = configparser.ConfigParser()
    config['ui'] = {'is_visible' : 0}
    #save as file
    with open(file_path, 'w') as f:
        config.write(f)


    
if __name__ == "__main__": 
    init_page()
    # Input Dir
    mypath = input('Enter Dir : ')
    print('\n')
    
    # get all file list
    file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # init progress bar
    pb = 0
    total_len = len(file_list)-1
    
    for file in file_list:
        # add progress bar count
        pb += 1
        #unzip tgz file 
        file = join(mypath, file)
        if tarfile.is_tarfile(file):
            try:
                unzip_tgz(file, extract_path=mypath)
            except Exception as e:
                print(e)
            #draw progress bar
            done = int(50 * pb / total_len)
            sys.stdout.write("\r Unzip [%s%s]" % ('=' * done, ' ' * (50-done)) )    
            sys.stdout.flush()
    sys.stdout.write('\n')
    
    # get all dir list
    dir_list = [dir for dir in listdir(mypath) if isdir(join(mypath, dir))]
    
    #init progress bar
    pb = 0
    total_len = len(file_list)-1
    
    # set visible False
    for dir in dir_list: 
        pb += 1
        try:
            set_visible_false(dir)
        except Exception as e:
            print(e)
        #draw progress bar
        done = int(50 * pb / total_len)
        sys.stdout.write("\r Set is_visible = 0 [%s%s]" % ('=' * done, ' ' * (50-done)) )    
        sys.stdout.flush()
    print('\n\nDone!')

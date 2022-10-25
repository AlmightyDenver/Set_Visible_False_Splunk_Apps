#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Python = 3.7
# Created By  : DenverAlmighty
# Created Date: 2022-10-24
# Updated Date : 2022-10-25
# version = '1.0.0'
# ---------------------------------------------------------------------------


import tarfile
import os, sys
from os import listdir
from os.path import isdir, isfile, join
import configparser # .conf
import argparse #input
import re #regtex

# from datetime import datetime, date
import datetime


# mypath = '/Users/denver/Downloads/viz_apps_copy'
flag = [0, 0, 0, 0]


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


# ========== init progress bar ==========
def init_pb(leng):
    pb = 0
    total_len = leng
    return pb, total_len

# ========== draw progress bar ==========
def draw_pb(pb, total_len, title):
    perc = int(pb / total_len * 100)
    done = int(perc / 2)
    sys.stdout.write('\r %02d%% [%s%s] %s' % (perc, '=' * done, ' ' * (50-done), title))   
    sys.stdout.flush()


# ========== input path, settings ==========
def input():
    #input
    parser = argparse.ArgumentParser(description='Unzip .tgz file and edit apps.conf file', add_help=True)
    parser.add_argument('--dir', '-d', dest='dir', help='(required) Enter app directory')
    parser.add_argument('--unzip', '-z', dest='unzip', help='(Optional) Unzip .tgz files or NOT [0|1] (default 1)', default=1, type=int)
    parser.add_argument('--keyword', '-k', dest='keyword', help='(Optional) Enter appname keyworkd (ex viz / visualization ..) (default : set all apps in dir)', default='')
    parser.add_argument('--isvisible', '-v', dest='isvisible', help='(Optional) Set is_visible = [0|1] (default 0)', default=0, type=int)
    parser.add_argument('--update', '-u', dest='update', help='(Optional) Set check_for_updates = [0|1] (default 0)', default=0, type=int)
    args = parser.parse_args()
    global mypath
    mypath = args.dir
    flag[0] = args.unzip
    global keyword
    keyword = args.keyword
    flag[1] = 0 if keyword == '' else 1
    flag[2] = args.isvisible
    flag[3] = args.update

    # check input data
    try:
        if not os.path.exists(mypath):
            raise Exception('%s does not exists \nexit' % mypath)
    except Exception as e:
        sys.stdout.write('ERROR %s' % e)
        sys.exit()
        
    for i in range(3):
        try:
            if flag[i] != 0 and flag[i] != 1:
                raise Exception('flag %d entered %s : Please Enter 0 or 1 \nexit' % (i, str(flag[i])))
        except Exception as e:
            sys.stdout.write('ERROR %s' % e)
            sys.exit()

# ========== make .tgz file list and call 'unzip_tgz_file' func to unzip ==========
def unzip_dir():
    # get all file list
    file_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # init progress bar
    pb, total_len = init_pb(len(file_list))
    
    for file in file_list:
        # add progress bar count
        pb += 1
        #unzip .tgz file 
        file = join(mypath, file)
        if tarfile.is_tarfile(file):
            try:
                unzip_tgz_file(file, extract_path=mypath)
            except Exception as e:
                print(e)
            #draw progress bar
            draw_pb(pb, total_len, 'Unzip')



# ========== unzip .tgz file ==========
def unzip_tgz_file(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    tar.extractall()
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            unzip_tgz_file(item.name, "./" + item.name[:item.name.rfind('/')])
    try:
        unzip_tgz_file(sys.argv[1] + '.tgz')
    except:
        name = os.path.basename(sys.argv[0])


# ========== add local dir and apps.conf file ==========
def set_config(path):
    #check local dir exists or not
    local_path = join(mypath, path, 'local')
    
    #if not exists local dir, make dir
    if not os.path.exists(local_path):
        os.mkdir(local_path)
        
    #add apps.conf file
    file_path = join(local_path, 'apps.conf')
    #set config
    config = configparser.ConfigParser()
    # set visible and update check 
    config['ui'] = {'is_visible' : 0} if flag[2] == 0 else {'is_visible' : 1}
    config['package'] = {'check_for_updates' : 0} if flag[3] == 0 else {'check_for_updates' : 1}

    #save as file
    with open(file_path, 'w') as f:
        config.write(f)


# ========== main ==========    
if __name__ == "__main__": 
    # print ascii art
    init_page()
    # Input Dir
    input()
    
    # unzip 
    if flag[0] == 1:
        unzip_dir()
        sys.stdout.write('\n')
    
    # set apps.conf
    # get all dir list
    if flag[1] == 0:
        dir_list = [dir for dir in listdir(mypath) if isdir(join(mypath, dir))]
    elif flag[1] == 1: 
        dir_list = [dir for dir in listdir(mypath) if isdir(join(mypath, dir)) and len(re.findall(keyword, dir)) > 0]
    # init progress bar
    pb, total_len = init_pb(len(dir_list))
    
    # set apps.conf
    for dir in dir_list: 
        pb += 1
        try:
            set_config(dir)
        except Exception as e:
            print(e)
        # draw progress bar
        draw_pb(pb, total_len, 'Set Config')
        
    
    print('\n\nDone!')


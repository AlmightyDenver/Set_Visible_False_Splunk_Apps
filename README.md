# Set_Visible_False_Splunk_Apps
Set invicible all splunk apps in specific direcoty (Untar apps, create /local/apps.conf file)

# requirements
python3

# How To Use
## args
'--dir', '-d', dest='dir', help='(required) Enter app directory'

'--unzip', '-z', dest='unzip', help='(Optional) Unzip .tgz files or NOT [0|1] (default 1)', default=1, type=int

'--keyword', '-k', dest='keyword', help='(Optional) Enter appname keyworkd (ex viz / visualization ..) (default : set all apps in dir'), default=''

'--isvisible', '-v', dest='isvisible', help='(Optional) Set is_visible = [0|1] (default 0)', default=0, type=int)

'--update', '-u', dest='update', help='(Optional) Set check_for_updates = [0|1] (default 0)', default=0, type=int)


## examples
unzip, set is_visible = 0 and check_for_updates = 0 to all apps in /my/path/dir
python Set_Visible_False.py -d /my/path/dir

set is_visible = 0 and check_for_updates = 0 in all apps in /my/path/dir (pass unzip)
python Set_Visible_False.py -d /my/path/dir -z 0

set is_visible = 0 and check_for_updates = 0 in all '*viz*' apps in /my/path/dir
python Set_Visible_False.py -d /my/path/dir -k viz

set is_visible = 1 and check_for_updates = 0 in all apps in /my/path/dir
python Set_Visible_False.py -d /my/path/dir -v 1

set is_visible = 0 and check_for_updates = 1 in all apps in /my/path/dir
python Set_Visible_False.py -d /my/path/dir -u 1


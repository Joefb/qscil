import os
import time
import item_dict

### Enter the log path to the EQ log file ###
log_path = "/home/home_name/.wine/drive_c/Program Files (x86)/EverQuest/Logs/"
### No need to modify below this line ########################################
##############################################################################


### Get the active toon by checking the current modified file ###
def get_active_toon():
    toon_logs = []
    os.chdir(log_path)
    files_list = os.listdir()
    for file in files_list:
        if file[:6] == 'eqlog_':
            toon_logs.append([file, os.stat(file).st_mtime])
    toon_logs = sorted(toon_logs,key=lambda l:l[1], reverse=True)
    toon = toon_logs[0][0]
    return toon

### Read the log file ###
def read_log(log_loc, last_pos):
    with open(log_loc, "r") as f:
        f.seek(last_pos)
        new_lines = f.readlines()
        last_pos = f.tell()
    return new_lines, last_pos

### init vars ###
def init_vars():
    toon = get_active_toon()
    last_toon = toon
    log_loc = log_path + toon
    file_size = os.path.getsize(log_loc)
    last_pos = file_size
    return toon, last_toon, log_loc, file_size, last_pos

### main init
toon, last_toon, log_loc, file_size, last_pos = init_vars()
looted_item = ""
###last_item = ""

#### Main loop ###
while True:
    ### If active toon changes, re init vars ###
    toon = get_active_toon()
    if toon != last_toon:
        last_toon = toon
        time.sleep(5)
        toon, last_toon, log_loc, file_size, last_pos = init_vars()

    time.sleep(0.5)
    os.system("clear")
    log_loc = log_path + toon
    file_size = os.path.getsize(log_loc)

    if file_size != last_pos:
        new_lines, last_pos = read_log(log_loc, last_pos)
        for line in new_lines:
            line = line.strip()
            for k in item_dict.items:
                if "You have looted" in line and k in line:
                    looted_item = k + " - " + item_dict.items.get(k)
                    break

                if "You say" in line and k in line:
                    looted_item = k + " - " + item_dict.items.get(k)
                    break
            last_pos = file_size
    
    #if item_looted == True:
        #last_item = looted_item
        #looted_item = key + " - " + item_dict.items.get(key)
        #else:
        #    last_item = looted_item
        #    looted_item = "Vendor Trash"

    #last_item = looted_item 
    print(f'''

     QSCIL(Quick Search Cause Im Lazy)
    ==============================================================
     Toon: {toon[6:-16]}
                                                                
     Item: {looted_item}
    ==============================================================
            ''')

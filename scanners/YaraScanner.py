import os
import yara

def yaraScan(file_to_scan):

    dir_name = './rules/'
    
    for file in os.listdir(dir_name):
            
            file_path = dir_name + file
            rules = yara.compile(filepath=file_path)
            matches = rules.match(file_to_scan)

            for match in matches:
                try:
                    if match : return True
                    else: return False
                except:
                    return False
import os
from os import path
# from mymod import get_list

def get_list():
    files = []
    try:
        uploadPath = path.join('.','resources/')
        filelist = os.listdir(uploadPath)
        for file in filelist:
            if path.isfile(path.join(uploadPath,file)):
                files.append(f"/{file}")
            
    except Exception as e:
        print(e)
    finally:
        return files
    
# if __name__ == '__main__':
#     files = get_list()
#     print(files)
    

import ConfigParser
import sys,os

def get_pwd():
    pwd = sys.path[0]
    if os.path.isfile(pwd):
        pwd = os.path.dirname(pwd)
    return pwd

config_file_path = get_pwd()+"/../config.ini"

def read_cfg_file(field, key):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except Exception,e:
        import traceback
        traceback.print_stack()
        traceback.print_exc()
        sys.exit(1)
    return result

def write_cfg_file(field, key, value):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        cf.set(field, key, value)
        cf.write(open(config_file_path,'w'))
    except Exception,e:
        import traceback
        traceback.print_stack()
        traceback.print_exc()
        sys.exit(1)
    return True




import datetime
import os
class FileHelper(object):
    @staticmethod
    def get_save_path():
        #项目路径
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        filename =  datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
        result_path = os.path.join(base_dir, 'data/' + filename)
        return result_path
    @staticmethod
    def append(filepath,content):
        with open(filepath, 'a+') as f:
            f.write(content)
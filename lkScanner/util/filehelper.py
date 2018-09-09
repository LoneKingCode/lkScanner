import datetime

class FileHelper(object):
    @staticmethod
    def get_save_path():
        #项目路径
        BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        filename =  datetime.datetime.strftime('%Y%m%d%H%M%S') + '.txt'
        RESULT_PATH = os.path.join(BASE_DIR, 'data/' + filename)
    @staticmethod
    def append(filepath,content):
        with open(filepath, 'a+') as f:
            f.write(content)
            f.close()



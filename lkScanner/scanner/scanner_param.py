class ScannerParam(object):
    def __init__(self,c,r,tn,t,ip,p,ifile,pfile,save,validator):
        self.connectmode = c
        self.runmode = r
        self.threadnum = tn
        self.timeout = t
        self.ip = ip
        self.port = p
        self.ipfile = ifile
        self.portfile = pfile
        self.save = save
        self.validator=validator



import os, time, datetime
import filetype

class evr_namer:
    filename = ""
    datetime_object = None
    old_filename = ""
    new_filename = ""
	
    def get_date_and_time(self, path):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.filename)
        
        self.datetime_object = datetime.datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")
        self.new_filename = self.datetime_object.strftime("%d%m%Y") + '_' + self.datetime_object.strftime("%H.%M") + '.' + str(filetype.guess(self.filename).extension)
        
        self.old_filename = self.filename.replace(path + '\\', '')
        
        print(self.old_filename)
        
        fileno = 0
        
        try:
            os.rename(self.filename, self.filename.replace(self.old_filename, self.new_filename))
        except:
            fileno+= 1
            self.new_filename = self.new_filename + '_' + str(fileno)

def run_naming():
    fileobj = evr_namer()
    Voice_files_folder = os.getcwd() + "\\Voice_files_folder"
    print(Voice_files_folder)
    for file_name in os.listdir(Voice_files_folder):
        fileobj.filename = Voice_files_folder + "\\" + file_name
        fileobj.get_date_and_time(Voice_files_folder)

if __name__ == '__main__':
    run_naming()
    
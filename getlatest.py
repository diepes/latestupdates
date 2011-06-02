#!/usr/bin/python
# retrieve the file information from a selected folder
# sort the files by last modified date/time and display in order newest file first
# tested with Python24 vegaseat 21jan2006
# Num of files to display set count in main()

import os, glob, time, re, getopt, sys
from os.path import join, getsize

def run(rootdir, count=50):
    prog = re.compile("VTS_|VIDEO_TS|Thumbs.db|\.message|UPDATEinfo.txt")
    msg = "------------ Dir:"+rootdir+"   Updated on:"+\
		time.strftime("%Y-%m-%d", time.localtime(time.time()))+" "
    print msg+'-'*(75-len(msg)),"\r" # just vanity
    date_file_list = []

    for root, dirs, files in os.walk(rootdir):
        for name in files:
            if not( prog.match(name) ):
                fname = join(root, name)
                stats = os.stat(fname)
                # create tuple (year yyyy, month(1-12), day(1-31), hour(0-23), minute(0-59),
                # second(0-59), weekday(0-6, 0 is monday), Julian day(1-366), 
                # daylight flag(-1,0 or 1)) from seconds since epoch
                # note: this tuple can be sorted properly by date and time
                create_date = time.localtime(stats.st_mtime)
                date_file_tuple = create_date, fname, name
                date_file_list.append(date_file_tuple)
            #else:
            #    print "Skip -> ",name

    #print date_file_list # test

    date_file_list.sort()
    date_file_list.reverse() # newest mod date now first

    print "%-12s %s\r" % ("created:", "filename:")
    for file in date_file_list:
      # extract just the filename
      folder, file_name = os.path.split(file[1])
      # convert date tuple to MM/DD/YYYY HH:MM:SS format
      file_date = time.strftime("%Y-%m-%d", file[0])
      print "%-12s %s\r" % (file_date, file[1].split(rootdir)[1])
      count = count - 1
      if count == 0:
         exit(0)
def usage():
    print '''
     -h   help
     -c   count, number of lines to print
     -d   directory
    '''
def main():
    # ...
    # use a folder you have ...
    rootdir = '/srv' # one specific folder
    count = 30
    #
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:d:v", ["help", "count"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-c", "--count"):
	    print "o=",o,"    a=",a
            count = int(a)
	elif o in ("-d"):
	    #print "o=",o,"rootdir=",a
	    rootdir = a
        else:
            assert False, "unhandled option"
    #
    run(rootdir, count)

if __name__ == "__main__":
    main()


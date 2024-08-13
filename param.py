#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt


def test00():
    opts, args = opts,args = getopt.getopt(sys.argv[1:],'h:f:v:',['help','filename=','version='])
    print(opts)
    for opt_name,opt_value in opts:
        if opt_name in ('-h','--help'):
            print("[*] Help info")
            #sys.exit()
        if opt_name in ('-v','--version'):
            ver = opt_value
            print("[*] Version is ",ver)
            #sys.exit()
        if opt_name in ('-f','--filename'):
            fileName = opt_value
            print("[*] Filename is ",fileName)
            # do something
            #sys.exit()
    sys.exit()

def test01():
    try:  
        opts, args = getopt.getopt(sys.argv[1:], "dh:o:", ['directory-prefix=',"help", "output="]) 
        print(opts) 
    except getopt.GetoptError:  
         print(" help information and exit: ")

def test02():
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile>')
   for opt, arg in opts:
      if opt == '-h':
         print( 'test.py -i <inputfile> -o <outputfile>')

      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print( '输入的文件为：', inputfile)
   print( '输出的文件为：', outputfile)

if __name__=="__main__":
    #test00()
    test01()
    #test02()


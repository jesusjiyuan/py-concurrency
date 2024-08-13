import sys
def get_mem_usage():
  module = sys.modules[__name__]
  mem_usage = sys.getsizeof(module)
  return mem_usage

#print("Current module memory usage: ",get_mem_usage())

import psutil
target_process_name = "ffplay.exe"

def monitor_mem_usage():
  process = psutil.process_iter()
  # while True:
  #   mem_usage = process.memory_info().rss
  #   print("Current memory usage: ", mem_usage)
  #print(process)
  mem_count = 0
  proc_count= 0
  for p in process:
    #print(p.name())    
    if p.name() == target_process_name:
      #print(p.name(),p.memory_info().rss)
      mem_count = mem_count + int(p.memory_info().rss)
      proc_count = proc_count +1
  print(str(proc_count),str(mem_count/(1024*1024)))
      
monitor_mem_usage()
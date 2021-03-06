"""
Author: Edgar Zamora Gomez  <edgar.zamora@urv.cat>
"""
import sys

from pyactive.controller import init_host, launch,start_controller, sleep

from time import time

NUM_NODES = 5
NUM_MSGS = 10

class Node():
 
    def __init__(self,id=None,next=None):
        self.id = id
        self.next = next  
        self.cnt = 0

    #@ref
    #@async
    def set_next(self, n2):        
        self.next = n2
        print n2
            
    
    def get_cnt(self):
        return self.cnt
    
    #@sync(1)
    def is_finished(self):
        return self.cnt >= NUM_MSGS
    
    #@async
    def init_token(self):
#        print 'send token',self,'->',self.next
        self.next.take_token()
        
    #@async
    def take_token(self):
        self.cnt += 1
        if (not self.is_finished()):
            self.next.take_token()
        #print 'taken token',self.cnt
    
def testN():
    
    host = init_host()
    
    print 'TEST ',NUM_NODES,' nodes and', NUM_MSGS, "messages."
    
    nf  = host.spawn_id('0','ring3','Node',['nf'])
    
    ni = nf;
    for i in range (1, NUM_NODES-2):    
        ni = host.spawn_id(str(i), 'ring3','Node',[('n',i),ni]) 
    
    n1 = host.spawn_id(str(NUM_NODES -1), 'ring3','Node',['n1',ni]) 
    
    nf.set_next(n1)  
      
    init = time()
      
    n1.init_token()
  
    while(nf.is_finished()):
        pass
        
    end = time()   
    print 'N1', n1
    print ((end - init)*1000),' ms.' 
    
 
def main(argv):
    
    global NUM_NODES, NUM_MSGS
      
    NUM_NODES = int(argv[0])
    NUM_MSGS = int(argv[1])
    start_controller('pyactive_thread')
    launch(testN)
    print 'finish!'
 
if __name__ == "__main__":
    main(sys.argv[1:])   
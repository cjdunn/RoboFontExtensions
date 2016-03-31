from mojo.UI import CurrentSpaceCenter
from mojo.events import addObserver, removeObserver

#run as a startup script in RF to disable draggable sidebearings in Space Center

class disableDragObserver(object):
    
    def __init__(self):
        addObserver(self, 'spaceCenterDidOpenCallback', 'spaceCenterDidOpen')
        addObserver(self, 'fontCloseCallback', 'fontDidClose')

                        
    def deactivateModule(self):
        removeObserver(self, 'spaceCenterDidOpen')        
        removeObserver(self,  'fontDidClose')
        #print 'disableDrag deactivated'
        


    def spaceCenterDidOpenCallback(self, info):
        self.disableDrag()



    def disableDrag(self):
        sp = CurrentSpaceCenter()
        sp.disableDrag(True)
        #print 'disableDrag activated'
              
        
    def fontCloseCallback(self, info):
        self.deactivateModule()

        
            
disableDragObserver()

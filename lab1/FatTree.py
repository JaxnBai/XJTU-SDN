from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
import os
class FatTree( Topo ): 
    def build(self):
        for i in range(4):
            self.addSwitch("s{}".format(i+1))
        for pod in range(4):
            for i in range(4):
                self.addSwitch("pod{}_s{}".format(pod+1,i+1))    
        for i in range(16):    
            self.addHost("h{}".format(i+1))
        
        # Add links
        for pod in range(4):
            for i in range(2):
                self.addLink("pod{}_s{}".format(pod+1,i+1),"s{}".format(2*i+1))
                self.addLink("pod{}_s{}".format(pod+1,i+1),"s{}".format(2*i+2))
                self.addLink("pod{}_s{}".format(pod+1,i+1),"pod{}_s{}".format(pod+1,3))
                self.addLink("pod{}_s{}".format(pod+1,i+1),"pod{}_s{}".format(pod+1,4))
        for pod in range(4):
            for i in range(2,4):
                self.addLink("pod{}_s{}".format(pod+1,i+1),"h{}".format(pod*4+2*i-3))
                self.addLink("pod{}_s{}".format(pod+1,i+1),"h{}".format(pod*4+2*i-2))
def run():
    topo=FatTree()
    net=Mininet(topo=topo,controller=Non)

    net.start()
    for i in range(4):
        os.system("sudo ovs-vsctl set bridge s{} stp_enable=true".format(i+1))
        os.system("sudo ovs-vsctl del-fail-mode s{}".format(i+1))
    for pod in range(4):
        for i in range(4):
            os.system("sudo ovs-vsctl set bridge pod{}_s{} stp_enable=true".format(pod+1,i+1))
            os.system("sudo ovs-vsctl del-fail-mode pod{}_s{}".format(pod+1,i+1))
    CLI(net)
    net.stop()

if __name__=='__main__':
    setLogLevel('info')
    run()
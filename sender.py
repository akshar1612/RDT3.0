from common import *

class sender:
    RTT = 20
    ACK = 0
    SEQ = 0
    def isCorrupted (self, packet):
        '''Checks if a received packet (acknowledgement) has been corrupted
        during transmission.
        Return true if computed checksum is different than packet checksum.
        '''
        calc_cs = checksumCalc(packet)

        if (packet.checksum != calc_cs):

            return True
        else:
            if (packet.ackNum != self.currentSeqNum):
                return True
            return False

    def isDuplicate(self, packet):
        '''checks if an acknowledgement packet is duplicate or not
        similar to the corresponding function in receiver side
        '''

        if (packet.ackNum != self.ACK):

            return False
        else:
            return True

    def getNextSeqNum(self):
        '''generate the next sequence number to be used.
        '''
        self.currentSeqNum += 1
        self.currentSeqNum %= 2
        return self.currentSeqNum

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        '''initialize the sequence number and the packet in transit.
        Initially there is no packet is transit and it should be set to None
        '''
        self.currentSeqNum = 0
        self.currentPacket = Packet(self.currentSeqNum, self.ACK, 0, '')
        return

    def timerInterrupt(self):
        '''This function implements what the sender does in case of timer
        interrupt event.
        This function sends the packet again, restarts the time, and sets
        the timeout to be twice the RTT.
        You never call this function. It is called by the simulator.
        '''
        self.networkSimulator.udtSend(self.entity, self.currentPacket)
        self.networkSimulator.startTimer(self.entity, float(self.RTT*2.0))
        return


    def output(self, message):
        '''prepare a packet and send the packet through the network layer
        by f calling utdSend.
        It also start the timer.
        It must ignore the message if there is one packet in transit
        '''
        self.currentPacket.payload = message.data
        self.currentPacket.ackNum = 0
        self.currentPacket.seqNum = self.currentSeqNum
        
        c = checksumCalc(self.currentPacket)
        
        self.currentPacket.checksum = c
        
        self.networkSimulator.udtSend(self.entity, self.currentPacket)
         
        self.networkSimulator.startTimer(self.entity, 20.0)
        return 

 
    
    def input(self, packet):

        '''If the acknowlegement packet isn't corrupted or duplicate, 
        transmission is complete. Therefore, indicate there is no packet
        in transition.
        The timer should be stopped, and sequence number  should be updated.

        In the case of duplicate or corrupt acknowlegement packet, it does 
        not do anything and the packet will be sent again since the
        timer will be expired and timerInterrupt will be called by the simulator.
        '''
        if ((not self.isCorrupted(packet)) or (not self.isDuplicate(packet))):
            
            self.networkSimulator.stopTimer(self.entity)
            self.currentSeqNum = self.getNextSeqNum()
            return
        self.ACK = (self.ACK+1)%2
        return

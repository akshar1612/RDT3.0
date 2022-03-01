from common import *

class receiver:
    ACK = 0
    SEQ = 0
    def isCorrupted(self, packet):
        ''' Checks if a received packet has been corrupted during transmission.
        Return true if computed checksum is different than packet checksum.'''
        
        calc_cs = checksumCalc(packet)
        return (packet.checksum != calc_cs)
        
   
    def isDuplicate(self, packet):
        return (packet.seqNum == self.SEQ)
    
    def getNextExpectedSeqNum(self):
        if(self.expectedSeqNum==1):
            self.expectedSeqNum = 0
        elif self.expectedSeqNum ==0:
            self.expectedSeqNum = 1
        return self.expectedSeqNum
     
    
    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))


    def init(self): 
        '''initialize expected sequence number'''
        self.expectedSeqNum = 0
        return
         

    def input(self, packet):
        '''This method will be called whenever a packet sent 
        from the sender arrives at the receiver. If the received
        packet is corrupted or duplicate, it sends a packet where
        the ack number is the sequence number of the  last correctly
        received packet. Since there is only 0 and 1 sequence numbers,
        you can use the sequence number that is not expected.
        
        If packet is OK (not a duplicate or corrupted), deliver it to the
        application layer and send an acknowledgement to the sender
        '''
        self.SEQ = self.getNextExpectedSeqNum()

        if (self.isCorrupted(packet) or self.isDuplicate(packet)):

            packet.payload = ''

            if (self.isCorrupted(packet)):
                packet.ackNum = (self.ACK+1) % 2
            else:
                packet.ackNum = packet.seqNum % 2
            packet.checksum = packet.ackNum
            packet.seqNum = 0
            self.networkSimulator.udtSend(self.entity, packet)
            self.SEQ = self.getNextExpectedSeqNum()
        else:
            self.networkSimulator.deliverData(self.entity, packet.payload)

            npacket = Packet(0, self.ACK, 0, '')
            c = checksumCalc(npacket)
            npacket.checksum = c
            self.networkSimulator.udtSend(self.entity, npacket)
            self.ACK = (self.ACK + 1) % 2

        return

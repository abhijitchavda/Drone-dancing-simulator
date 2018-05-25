import grpc
import drone_pb2_grpc
from drone_pb2 import Empty, Response
import sys


class CordiClient():
    def __init__(self, host='0.0.0.0', port=int(sys.argv[1])):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = drone_pb2_grpc.GetcordiStub(self.channel)
    
    def cordi(self):
    	req=Empty()
    	for response in self.stub.getcordinates(req):
    		if response.x==-1 and response.y==-1 and response.z==-1:
    			print("Client id [1] connected to the server")

    		elif response.x==-2 and response.y==-2 and response.z==-2:
    			print("Client id [2] connected to the server")

    		else:
    			print("[received] moving to [{},{},{}]".format(response.x,response.y,response.z))

def test():
    client = CordiClient()
    client.cordi()
    

if __name__ == '__main__':
    test()
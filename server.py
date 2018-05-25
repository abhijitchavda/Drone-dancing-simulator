import time
import grpc
import drone_pb2
import drone_pb2_grpc
import queue
import asyncio
import sys

flag=1
from concurrent import futures
y=0
z=0
dif=0
q = queue.Queue()
q2 = queue.Queue()
class DroneServer(drone_pb2_grpc.GetcordiServicer):
    def getcordinates(self, request, context):
        global flag
        global q
        global q2
        if flag==1 :
            flag=flag+1
            yield drone_pb2.Response(x=-1,y=-1,z=-1)
            while True:
                if not q.empty() :
                    yield drone_pb2.Response(x=q.get(),y=y,z=z)

        elif flag==2 :
            yield drone_pb2.Response(x=-2,y=-2,z=-2)
            while True:
                if not q2.empty() :
                    yield drone_pb2.Response(x=q2.get(),y=y,z=z)


def run(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    drone_pb2_grpc.add_GetcordiServicer_to_server(DroneServer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()
    try:
        print("Server started at...%d" % port)
        global q
        global q2
        global y
        global z
        global dif
        cordi1=sys.argv[1]
        cordi2=sys.argv[2]
        x1,y1,z1=cordi1.split(",")
        x2,y2,z2=cordi2.split(",")
        y=int(y1)
        z=int(z1)
        q.put(int(x1))
        dif=int(x2)-int(x1)
        q2.put(int(x2))
        while True:
            coordiante = input("Enter New Cooridnate[x, y, z] > ")
            x1, y1, z1 = coordiante.split(",")
            y = int(y1) 
            z = int(z1)
            q.put(int(x1))
            q2.put(int(x1)+dif)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
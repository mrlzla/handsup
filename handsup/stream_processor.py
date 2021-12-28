import os
import time
import json
import queue

from threading import Thread

from .video_stream import VideoStream
from .alg import Alg

class StreamProcessor:
    def __init__(self, paths, opts):
        self.video_streams = [VideoStream(path) for path in paths]
        self.queues = [queue.Queue() for _ in range(len(self.video_streams))]
        self.algs = []
        for i, stream in enumerate(self.video_streams):
            size = (stream.width, stream.height)
            alg = Thread(target=Alg, args=(opts, size, self.queues[i], ))
            alg.daemon = True
            alg.start()
            self.algs.append(alg)

    def run(self):
        while True:
            for index, stream in enumerate(self.video_streams):
                ret, frame = stream.run()
                if not ret:
                    break
                if self.queues[index].empty():
                    self.queues[index].put_nowait(frame)
        





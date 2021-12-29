import os
import time
import json
import queue

from threading import Thread

from .video_stream import VideoStream
from .alg import Alg

class StreamProcessor:
    def __init__(self, paths, opts):
        self.video_streams = []
        for path in paths:
            try:
                stream = VideoStream(path)
                self.video_streams.append(stream)
            except Exception as e:
                print(e)

        self.video_streams = [stream for stream in self.video_streams if stream.width > 0]
        self.queues = [queue.Queue() for _ in range(len(self.video_streams))]
        self.algs = []
        for i, stream in enumerate(self.video_streams):
            size = (stream.width, stream.height)
            alg = Thread(target=Alg, args=(opts, size, self.queues[i], ))
            alg.daemon = True
            alg.start()
            self.algs.append(alg)

    def run(self):
        if len(self.video_streams) == 0:
            return
        
        while True:
            for index, stream in enumerate(self.video_streams):
                ret, frame = stream.run()
                if not ret or frame is None:
                    continue
                if self.queues[index].empty():
                    self.queues[index].put_nowait(frame)
        





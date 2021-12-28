import cv2

class VideoStream:
    def __init__(self, path):
        self.path = path
        self.cam = cv2.VideoCapture(self.path)
        self.fps = self.cam.get(5)
        self.width  = int(self.cam.get(3))
        self.height = int(self.cam.get(4))
    
    def run(self):
        return self.cam.read()
    

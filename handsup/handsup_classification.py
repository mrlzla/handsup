class HandsupClassification:
    def __init__(self):
        self.nose_index = 0
        self.right_wrist_index = 9
        self.left_wrist_index = 10

    def process(self, data):
        res = []
        for item in data:
            bbox = item[:4]
            prob = item[4]
            keypoints = item[5:]

            if keypoints[2*self.right_wrist_index + 1] < keypoints[2*self.nose_index + 1] or \
                keypoints[2*self.left_wrist_index + 1] < keypoints[2*self.nose_index + 1]:
                res.append(1)
            else:
                res.append(0)
        return res


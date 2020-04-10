import time


class FPS:
    def __init__(self):
        self.prev_t = time.time()
        self.fps_hist_m = 0
        self.fps_hist_c = 0
    def start(self):
        self.prev_t = time.time()
    def run(self):
        self.fps = 1 / (time.time() - self.prev_t)
        self.fps_hist_c += 1
        self.fps_hist_m += self.fps
        self.prev_t = time.time()
    def pr(self):
        print("NOW:", self.fps, "MED:", self.fps_hist_m / self.fps_hist_c)
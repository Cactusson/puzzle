class Calc:
    """
    Changes obj's alpha value from start to end during duration
    """
    def __init__(self, start, end, duration, obj):
        self.current = start
        self.start = start
        self.end = end
        self.duration = duration
        self.elapsed = 0
        self.active = True
        self.obj = obj
        self.callback = None

    def get_value(self, p):
        if self.end > self.start:
            return self.start + int((self.end - self.start) * p)
        else:
            return self.start - int((self.start - self.end) * p)

    def finish(self):
        self.active = False
        if self.callback:
            self.callback()

    def update(self, dt):
        if not self.active:
            return
        self.elapsed += dt
        p = min(1.0, self.elapsed / self.duration)
        self.current = self.get_value(p)
        self.obj.set_alpha(self.current)
        if p >= 1:
            self.finish()

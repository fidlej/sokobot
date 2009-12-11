
class ColorScale(object):
    """
    Conversion utility from 1d space to RGB space.
    Inspirated from:
    http://www.ks.uiuc.edu/Research/vmd/vmd-1.7.1/ug/node76.html
    http://www.research.ibm.com/people/l/lloydt/color/color.HTM
    """
    def __init__(self, xMin=0.0, xMax=1.0, step=None):
        """Prepares new color scale.
        Values from xMin to xMax will be mapped colors
        starting from green to red.
        """
        MIDPOINT_POS = 0.6
        BOOST_HEIGHT = 0.6
        self.step = step
        self.cMin = 0
        self.cMax = 255
        self.xMin = xMin
        self.xMax = xMax
        if self.step:
            self.xMin //= self.step
            self.xMax //= self.step
        self.xMidpoint = self.xMin + MIDPOINT_POS * (self.xMax - self.xMin)

        cRange = self.cMax - self.cMin
        xRange1 = self.xMidpoint - self.xMin
        xRange2 = self.xMax - self.xMidpoint
        self.slope1 = float(cRange)/xRange1
        self.slope2 = float(cRange)/xRange2
        self.boost = BOOST_HEIGHT * self.cMax

    def to_rgb(self, x):
        """Converts x to rgb.
        The highest x gets red.
        The middle x gets green.
        The lowest x gets blue.
        """
        if self.step:
            x //= self.step
        if x < self.xMidpoint:
            b = (x - self.xMin) * -self.slope1 + self.cMax
            g = (x - self.xMin) * self.slope1 + self.cMin
            r = self.cMin
        else:
            b = self.cMin
            g = (x - self.xMidpoint) * -self.slope2 + self.cMax
            r = self.boost + (x - self.xMidpoint) * self.slope2 + self.cMin
        return self._fit(r), self._fit(g), self._fit(b)

    def _fit(self, c):
        return min(self.cMax, max(self.cMin, int(c)))


if __name__ == "__main__":
    scale = ColorScale(0, 2.0)
    print scale.to_rgb(0.0)
    print scale.to_rgb(1.0)
    print scale.to_rgb(2.0)


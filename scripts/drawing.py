"""Small source renderer for dimensioned monochrome technical figures."""
import argparse
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


VIEWS = {
    'rack': ((.85, .56, 0), (.26, -.35, -.83)),
    'front': ((1, 0, 0), (0, 0, -1)),
    'top': ((1, 0, 0), (0, -1, 0)),
    'side': ((0, 1, 0), (0, 0, -1)),
}


class Drawing:
    def __init__(self, size=(1800, 1250), scale=6, origin=(820, 853.1),
                 view='rack', font_path=None, text_size=34, supersample=2):
        self.size, self.scale, self.origin = size, scale, origin
        self.axes = VIEWS[view] if isinstance(view, str) else view
        self.ss = supersample
        self.image = Image.new('RGB', tuple(round(v*self.ss) for v in size), 'white')
        self.draw = ImageDraw.Draw(self.image)
        candidates = [font_path,
                      str(Path(os.environ.get('WINDIR', 'C:/Windows'))/'Fonts/arial.ttf'),
                      '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                      '/System/Library/Fonts/Supplemental/Arial.ttf']
        selected = next((p for p in candidates if p and Path(p).is_file()), None)
        if selected is None:
            raise FileNotFoundError('Specify a TrueType font with font_path.')
        self.font = ImageFont.truetype(selected, round(text_size*self.ss))

    def p(self, point):
        return tuple(self.origin[i] + self.scale*sum(a*b for a,b in zip(axis, point))
                     for i,axis in enumerate(self.axes))

    def line2(self, points, width=2, dashed=False):
        if dashed:
            for a,b in zip(points, points[1:]):
                dx,dy = b[0]-a[0], b[1]-a[1]
                length = math.hypot(dx,dy)
                if not length:
                    continue
                for n in range(0, math.ceil(length), 20):
                    end = min(n+11, length)
                    self.line2([(a[0]+dx*n/length,a[1]+dy*n/length),
                                (a[0]+dx*end/length,a[1]+dy*end/length)],width)
            return
        self.draw.line([(round(x*self.ss),round(y*self.ss)) for x,y in points],
                       fill='black',width=round(width*self.ss),joint='curve')

    def line(self, points, width=3.4, dashed=False):
        self.line2([self.p(p) for p in points],width,dashed)

    def polygon(self, points, width=3.4):
        projected = [self.p(p) for p in points]
        self.draw.polygon([(round(x*self.ss),round(y*self.ss)) for x,y in projected],
                          fill='white')
        self.line2(projected+[projected[0]],width)

    def label2(self, point, label):
        # U+2300 is absent from the approved Windows Arial font.
        label = str(label).replace('\u2300','\u00d8')
        position = tuple(v*self.ss for v in point)
        box = self.draw.textbbox(position,label,font=self.font,anchor='mm')
        self.draw.rectangle((box[0]-8*self.ss,box[1]-4*self.ss,
                             box[2]+8*self.ss,box[3]+4*self.ss),fill='white')
        self.draw.text(position,label,font=self.font,fill='black',anchor='mm')

    def arrow2(self, tip, other, length=13):
        dx,dy = other[0]-tip[0],other[1]-tip[1]
        distance = math.hypot(dx,dy)
        if distance == 0:
            raise ValueError('Dimension collapses in this view; choose another axis or view.')
        ux,uy = dx/distance,dy/distance
        self.line2([(tip[0]+ux*length-uy*length*.32,
                     tip[1]+uy*length+ux*length*.32),tip,
                    (tip[0]+ux*length+uy*length*.32,
                     tip[1]+uy*length-ux*length*.32)],1.8)

    def dimension2(self, a, b, label, label_at=None):
        self.line2([a,b],1.6)
        self.arrow2(a,b)
        self.arrow2(b,a)
        if label:
            self.label2(label_at or ((a[0]+b[0])/2,(a[1]+b[1])/2),label)

    def dimension(self, a, b, label, label_at=None):
        self.dimension2(self.p(a),self.p(b),label,label_at)

    def extension(self, a, b):
        self.line([a,b],1.3)

    @staticmethod
    def circle_points(center, radius, start=0, end=2*math.pi, samples=400):
        return [(center[0]+radius*math.cos(start+(end-start)*i/samples),
                 center[1]+radius*math.sin(start+(end-start)*i/samples),center[2])
                for i in range(samples+1)]

    def save(self, destination):
        destination = Path(destination)
        destination.parent.mkdir(parents=True,exist_ok=True)
        self.image.resize(self.size,Image.Resampling.LANCZOS).save(destination,dpi=(200,200))
        return destination


def demo_cup(destination):
    drawing = Drawing()
    tangent = math.atan2(.56,.85)
    left,right = tangent+math.pi,tangent

    def point(angle,z):
        return (60*math.cos(angle),60*math.sin(angle),z)

    drawing.line(drawing.circle_points((0,0,95),60))
    drawing.line(drawing.circle_points((0,0,0),60,left,right+2*math.pi))
    for angle in [left,right]:
        drawing.line([point(angle,0),point(angle,95)])
    a,b = drawing.p(point(left,95)),drawing.p(point(right,95))
    for p in [a,b]:
        drawing.line2([p,(p[0],p[1]-262)],1.3)
    drawing.dimension2((a[0],a[1]-245),(b[0],b[1]-245),'Ø120')
    a,b = drawing.p(point(right,0)),drawing.p(point(right,95))
    for p in [a,b]:
        drawing.line2([p,(1400,p[1])],1.3)
    drawing.dimension2((1380,a[1]),(1380,b[1]),'95')
    return drawing.save(destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo',type=Path,required=True,help='Write the reference cup PNG here.')
    args = parser.parse_args()
    print(demo_cup(args.demo))

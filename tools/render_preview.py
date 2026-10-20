"""Optional local PNG renderer for our SVG previews. Requires Pillow, never used by the generator."""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

def render(source,destination,scale=2):
    from PIL import Image,ImageDraw,ImageFont
    root=ET.fromstring(Path(source).read_bytes())
    width,height=int(root.get("width")),int(root.get("height"))
    image=Image.new("RGB",(width*scale,height*scale),"#f1eee5")
    draw=ImageDraw.Draw(image,"RGBA")
    def color(value,opacity=1):
        v=value.lstrip("#")
        return tuple(int(v[i:i+2],16) for i in (0,2,4))+(round(float(opacity)*255),)
    def font(size):
        for name in ("DejaVuSans.ttf","C:/Windows/Fonts/arial.ttf"):
            try:return ImageFont.truetype(name,size)
            except OSError:pass
        return ImageFont.load_default(size=size)
    for node in root.iter():
        tag=node.tag.rsplit("}",1)[-1]
        if tag=="polygon":
            points=[tuple(float(v)*scale for v in point.split(",")) for point in node.get("points").split()]
            draw.polygon(points,fill=color(node.get("fill"),node.get("fill-opacity","1")))
            draw.line(points+[points[0]],fill=color(node.get("stroke","#26302b"),node.get("stroke-opacity",".13")),width=1)
        elif tag=="line":
            points=[float(node.get(key))*scale for key in ("x1","y1","x2","y2")]
            draw.line(points,fill=color(node.get("stroke"),node.get("stroke-opacity","1")),width=1)
        elif tag=="text" and node.text:
            size=round(float(node.get("font-size","15"))*scale)
            draw.text((float(node.get("x"))*scale,(float(node.get("y"))-size/scale)*scale),
                      node.text,font=font(size),fill=node.get("fill","#425047"))
    image=image.resize((width,height),Image.Resampling.LANCZOS)
    image.save(destination)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source");parser.add_argument("destination")
    args=parser.parse_args()
    render(args.source,args.destination)

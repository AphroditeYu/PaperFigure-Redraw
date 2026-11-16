"""Render a manually verified, pixel-coordinate scene as editable PowerPoint.
No automatic classification is claimed. Raster components remain raster.
"""
import argparse,io,json
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE,MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement

def render(scene_path,output):
 scene_path=Path(scene_path);cfg=json.loads(scene_path.read_text(encoding='utf-8-sig'));W,H=cfg['size'];scale=13.33/W
 r=Presentation();r.slide_width=Inches(13.33);r.slide_height=Inches(H*scale);s=r.slides.add_slide(r.slide_layouts[6]);counts={}
 src=None
 for o in cfg['objects']:
  kind=o['kind'];counts[kind]=counts.get(kind,0)+1;x,y,w,h=o['box']
  if min(x,y,w,h)<0 or x+w>W+1 or y+h>H+1:raise ValueError(f'Out of bounds: {o}')
  bounds=[Inches(v*scale) for v in (x,y,w,h)]
  if kind=='raster':
   if src is None:src=Image.open(scene_path.parent/cfg['source']).convert('RGB')
   stream=io.BytesIO();src.crop(o.get('crop',[x,y,x+w,y+h])).save(stream,format='PNG');stream.seek(0);sh=s.shapes.add_picture(stream,*bounds)
  elif kind=='line':
   x2,y2=o.get('end',[x+w,y+h]);sh=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x*scale),Inches(y*scale),Inches(x2*scale),Inches(y2*scale))
   if o.get('arrow'):
    end=OxmlElement('a:tailEnd');end.set('type','triangle');sh.line._get_or_add_ln().append(end)
  else:
   if kind=='text':sh=s.shapes.add_textbox(*bounds)
   elif kind in ('rect','round','ellipse'):
    sh=s.shapes.add_shape({'rect':MSO_SHAPE.RECTANGLE,'round':MSO_SHAPE.ROUNDED_RECTANGLE,'ellipse':MSO_SHAPE.OVAL}[kind],*bounds)
   else:raise ValueError('Unknown object kind: '+kind)
   if kind!='text':
    if o.get('fill'):sh.fill.solid();sh.fill.fore_color.rgb=RGBColor.from_string(o['fill'])
    else:sh.fill.background()
   if 'text' in o:
    tf=sh.text_frame;tf.clear();tf.word_wrap=True;tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0;tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    for i,t in enumerate(o['text'].split('\n')):
     p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=t;p.alignment=PP_ALIGN.CENTER;p.font.name='Arial';p.font.size=Pt(o.get('font',28)*scale*72);p.font.color.rgb=RGBColor.from_string(o.get('color','111111'))
  if kind!='raster':
   if o.get('stroke'):sh.line.color.rgb=RGBColor.from_string(o['stroke']);sh.line.width=Pt(o.get('width',2)*scale*72)
   else:sh.line.fill.background()
  if kind!='raster': sh._element.spPr.append(OxmlElement('a:effectLst'))
  sh.name=o.get('id',f'{kind}_{len(s.shapes)}');sh.rotation=o.get('rotation',0)
 s.notes_slide.notes_text_frame.text='Hybrid recreation. Raster elements are source crops, not editable scientific reconstructions. See scene JSON for object inventory.'
 r.save(output);return counts
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('scene');a.add_argument('output');args=a.parse_args();print(json.dumps(render(args.scene,args.output)))


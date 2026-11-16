import json,tempfile,sys
from pathlib import Path
from pptx import Presentation
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from render_scene import render
with tempfile.TemporaryDirectory() as td:
 p=Path(td);cfg={'size':[1000,600],'objects':[{'kind':'rect','box':[100,100,200,100],'text':'Editable label','fill':'FFFFFF'},{'kind':'line','box':[300,150,100,0],'end':[400,150],'stroke':'000000','arrow':True}]}
 (p/'scene.json').write_text(json.dumps(cfg));render(p/'scene.json',p/'out.pptx');r=Presentation(p/'out.pptx');assert r.slides[0].shapes[0].text=='Editable label';assert len(r.slides[0].shapes)==2
 r.slides[0].shapes[0].text='Modified';r.save(p/'modified.pptx');assert Presentation(p/'modified.pptx').slides[0].shapes[0].text=='Modified'
 cfg['objects'][0]['box']=[900,100,200,100];(p/'bad.json').write_text(json.dumps(cfg))
 try:render(p/'bad.json',p/'bad.pptx')
 except ValueError:pass
 else:raise AssertionError('Out-of-bounds scene accepted')
print('PASS: native text round-trip, connector, editable saved changes, invalid bounds rejected')

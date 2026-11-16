#!/usr/bin/env python3
"""Extract simple vertical filled bars using user-specified axes and bar centers.

Coordinates and labels are supplied in a JSON configuration; this tool does not
identify plots or recover hidden data/error bars. Results require visual review.
"""
import argparse, csv, json
from pathlib import Path
from PIL import Image
import numpy as np
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
import matplotlib.pyplot as plt


def extract(image, cfg):
    arr=np.asarray(image.convert('RGB')).astype(int); h,w=arr.shape[:2]; results=[]
    for panel in cfg['panels']:
        y0,y1=panel['y0'],panel['y1']
        if not (0 <= y1 < y0 < h): raise ValueError('invalid vertical calibration')
        if len(panel['centers']) != len(panel['labels']): raise ValueError('label count differs from center count')
        for label, x in zip(panel['labels'], panel['centers']):
            if not 2 <= x < w-2: raise ValueError('invalid bar center')
            # Majority of a five-pixel horizontal sample rejects narrow error bars.
            block=arr[y1:y0,x-2:x+3,:]
            gray=block.mean(axis=2)
            chroma=block.max(axis=2)-block.min(axis=2)
            colored=((gray>60)&(gray<205)&((chroma<35)|((block[:,:,1]>block[:,:,0]+15)&(block[:,:,1]>block[:,:,2]+5))))
            hit=np.flatnonzero((colored.sum(axis=1)>=3))
            if not len(hit): raise ValueError(f"no fill found: {panel['name']} / {label}")
            splits=np.flatnonzero(np.diff(hit)>4)+1
            runs=np.split(hit,splits)
            # A valid bar fill must connect to the calibrated zero baseline.
            bottom_run=runs[-1]
            if y0-(y1+int(bottom_run[-1]))>8: raise ValueError(f"bar does not reach zero baseline: {panel['name']} / {label}")
            top=y1+int(bottom_run[0]); value=(y0-top)/(y0-y1)
            results.append((panel['name'],label,x,top,round(float(value),4)))
    return results


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('image');ap.add_argument('config');ap.add_argument('--out',required=True);args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);cfg=json.loads(Path(args.config).read_text(encoding='utf-8'))
    rows=extract(Image.open(args.image),cfg)
    with (out/'digitized.csv').open('w',encoding='utf-8',newline='') as f:
        wr=csv.writer(f);wr.writerow(['panel','label','pixel_x','pixel_top','estimated_value']);wr.writerows(rows)
    wb=Workbook();notes=wb.active;notes.title='Read me';notes.append(['Estimates from raster bar heights, not original values. Error bars not extracted. Verify against input.'])
    fig,axs=plt.subplots(1,len(cfg['panels']),figsize=(4*len(cfg['panels']),4),squeeze=False)
    for idx,panel in enumerate(cfg['panels']):
        ws=wb.create_sheet(f'Panel {idx+1}');ws.append(['Model','Estimated F1']); subset=[r for r in rows if r[0]==panel['name']]
        for row in subset:ws.append([row[1],row[4]])
        chart=BarChart();chart.title=panel['name'];chart.y_axis.title='F1 score';chart.x_axis.delete=False;chart.y_axis.delete=False;chart.x_axis.tickLblPos='nextTo';chart.y_axis.tickLblPos='nextTo';chart.add_data(Reference(ws,min_col=2,min_row=1,max_row=ws.max_row),titles_from_data=True);chart.set_categories(Reference(ws,min_col=1,min_row=2,max_row=ws.max_row));ws.add_chart(chart,'D2')
        ax=axs[0,idx];ax.bar([r[1] for r in subset],[r[4] for r in subset],color=['#acafaf']*(len(subset)-1)+['#438654']);ax.set_ylim(0,1.05);ax.set_title(panel['name']);ax.set_ylabel('F1 score');ax.tick_params(axis='x',labelrotation=55)
    fig.tight_layout();fig.savefig(out/'bars.png',dpi=160);fig.savefig(out/'bars.svg');wb.save(out/'editable_data.xlsx')
    print(f'{len(rows)} bars written to {out}')
if __name__=='__main__': main()



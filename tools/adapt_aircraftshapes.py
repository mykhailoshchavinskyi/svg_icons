#!/usr/bin/env python3
"""Adapt inspected AircraftShapesSVG references into monochrome silhouettes."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
from urllib.parse import quote
if __package__:
    from .generate_catalog import GROUPS
else:
    from generate_catalog import GROUPS

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'third_party/aircraftshapes'
REV='0743718760c42a5e91801adc053b5b828a434a5e'
BASE=f'https://github.com/RexKramer1/AircraftShapesSVG/blob/{REV}'
NS='{http://www.w3.org/2000/svg}'


def main():
    sources=json.loads((SOURCE/'selected.json').read_text())
    refs=json.loads((ROOT/'references.json').read_text())
    names={line.split('|')[0]:line.split('|')[1] for rows in GROUPS.values() for line in rows.strip().splitlines()}
    ET.register_namespace('',NS[1:-1])
    for key,source in sources.items():
        root=ET.parse(SOURCE/source['sanitized_file']).getroot()
        def paint(node,accent=False):
            accent=accent or node.get('id') in source['accent_group_ids']
            assert node.tag.rsplit('}',1)[-1] not in {'image','script','foreignObject'}
            style={}
            for declaration in node.get('style','').split(';'):
                if ':' in declaration:
                    prop,value=declaration.split(':',1);style[prop.strip()]=value.strip()
            drawable=node.tag.rsplit('}',1)[-1] in {'path','rect','circle','ellipse','polygon','polyline'}
            if drawable:
                # Source outline paths are unfilled diagrams. Fill their existing
                # boundaries; accent paths stay unfilled, retaining exterior details.
                style['fill']='none' if accent else '#505a64'
            if 'stroke' in style and style['stroke']!='none':style['stroke']='#505a64'
            if style:node.set('style',';'.join(k+':'+v for k,v in style.items()))
            for attr in ('fill','stroke'):
                if node.get(attr) and node.get(attr)!='none':node.set(attr,'#505a64')
            for child in node:paint(child,accent)
        paint(root)
        root.set('viewBox',source['fitted_viewBox'])
        root.set('width','400');root.set('height','400')
        root.set('role','img');root.set('aria-labelledby','title desc')
        path=quote(source['source_file'],safe='/')
        ref={
            'source_page':BASE+'/'+path,
            'image_url':f'https://raw.githubusercontent.com/RexKramer1/AircraftShapesSVG/{REV}/'+path,
            'source_shape':Path(source['source_file']).stem,
            'source_title':source['source_title'],
            'source_format':'Model-specific outline SVG, rendered and inspected at fitted scale before adaptation',
            'local_image':f'reference-artwork/{key}.svg',
            'author':'RexKramer1 / AircraftShapesSVG (BelugaProject)',
            'license':'GPL-3.0-only',
            'license_file':'third_party/aircraftshapes/LICENSE',
            'attribution':f'Aircraft SVG by RexKramer1, AircraftShapesSVG, revision {REV}; adapted under GNU GPL version 3. Original file title: '+source['source_title'],
            'variant':source['source_title'],'view':'top','reviewed':True,
            'review_basis':'Source SVG visually checked against named model and variant before adaptation. Not a manufacturer drawing.',
            'changes':'Source outline filled #505a64; accent paths remain unfilled in the same grey; fitted framing, accessibility and attribution added. Coordinates, transforms and drawing order unchanged; embedded raster/editor content excluded.',
        }
        for tag,text in [('title',names[key]),('desc','Силует за модельним SVG-референсом RexKramer1 / AircraftShapesSVG. Вигляд зверху. GPL-3.0-only.'),('metadata',json.dumps(ref,ensure_ascii=False))]:
            element=ET.Element(NS+tag,{'id':tag} if tag in {'title','desc'} else {});element.text=text;root.insert(0,element)
        (ROOT/'reference-artwork'/(key+'.svg')).write_text(ET.tostring(root,encoding='unicode')+'\n')
        refs[key]=ref
    (ROOT/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
    print(f'Adapted {len(sources)} inspected AircraftShapesSVG references (GPL v3)')


if __name__=='__main__':
    main()

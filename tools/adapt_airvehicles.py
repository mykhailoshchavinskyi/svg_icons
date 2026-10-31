#!/usr/bin/env python3
"""Adapt inspected B-2 and KC-135 SVG references by Jason Wohlgemuth (MIT)."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
if __package__:
    from .generate_catalog import GROUPS
else:
    from generate_catalog import GROUPS

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'third_party/airvehicles'
REV='c559a5094af53a5add2125179685493aa51c3f6c'
BASE=f'https://github.com/jhwohlgemuth/svg-air-vehicles/blob/{REV}'
NS='{http://www.w3.org/2000/svg}'


def main():
    sources=json.loads((SOURCE/'selected.json').read_text())
    refs=json.loads((ROOT/'references.json').read_text())
    names={line.split('|')[0]:line.split('|')[1] for rows in GROUPS.values() for line in rows.strip().splitlines()}
    ET.register_namespace('',NS[1:-1])
    for key,source in sources.items():
        root=ET.parse(SOURCE/source['sanitized_file']).getroot()
        for node in root.iter():
            assert node.tag.rsplit('}',1)[-1] in {'svg','g','path','polygon','rect','circle','ellipse','line','polyline'}
            node.attrib.pop('class',None)
            if node.tag!=NS+'svg':node.set('fill','#505a64')
        root.set('viewBox',source['fitted_viewBox']);root.set('width','400');root.set('height','400')
        root.set('role','img');root.set('aria-labelledby','title desc')
        ref={
            'source_page':BASE+'/air-vehicles.html',
            'image_url':f'https://raw.githubusercontent.com/jhwohlgemuth/svg-air-vehicles/{REV}/air-vehicles.html',
            'source_shape':source['source_selector'],
            'source_format':'Individually identified inline SVG in source HTML; extracted as data without executing page scripts',
            'local_image':f'reference-artwork/{key}.svg',
            'author':'Jason Wohlgemuth',
            'license':'MIT','license_file':'third_party/airvehicles/LICENSE',
            'attribution':'Copyright (c) 2015 Jason Wohlgemuth, svg-air-vehicles. Adapted under the MIT licence.',
            'variant':'KC-135 family; source does not identify engine subtype' if key=='kc135' else 'B-2 Spirit',
            'view':'top','reviewed':True,
            'review_basis':'Named inline SVG extracted and visually inspected before adaptation. KC-135 is a family-level reference, not verification of a particular R/T engine variant.',
            'changes':'Palette unified to #505a64; standalone SVG wrapper, fitted viewBox, accessibility and attribution added. Path/polygon coordinates and drawing order unchanged.',
        }
        for tag,text in [('title',names[key]),('desc','Вигляд зверху за SVG-референсом Jason Wohlgemuth / svg-air-vehicles. MIT. Для KC-135 джерело не визначає підтип двигунів.' if key=='kc135' else 'Вигляд зверху за SVG-референсом Jason Wohlgemuth / svg-air-vehicles. MIT.'),('metadata',json.dumps(ref,ensure_ascii=False))]:
            element=ET.Element(NS+tag,{'id':tag} if tag in {'title','desc'} else {});element.text=text;root.insert(0,element)
        (ROOT/'reference-artwork'/(key+'.svg')).write_text(ET.tostring(root,encoding='unicode')+'\n')
        refs[key]=ref
    (ROOT/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
    print(f'Adapted {len(sources)} inspected svg-air-vehicles references (MIT)')


if __name__=='__main__':
    main()

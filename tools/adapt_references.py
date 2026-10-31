#!/usr/bin/env python3
"""Adapt inspected, model-specific tar1090 SVG references without generic shapes.

Uses data only, never executes the downloaded upstream JavaScript. The original
source, licence, author comments and pinned revision are retained in third_party.
Reference adaptation outputs are separate from hand-drawn draft overrides.
"""
from pathlib import Path
import html
import json
import xml.etree.ElementTree as ET
if __package__:
    from .generate_catalog import GROUPS
else:
    from generate_catalog import GROUPS

ROOT=Path(__file__).resolve().parents[1]
REV='5d59b1ba2c5e30eb23f1161940367b7767f10ad5'
BASE=f'https://github.com/wiedehopf/tar1090/blob/{REV}'
MAPPING={
    'f35':'f35','fa18':'f18','gripen':'sb39','rafale':'rafale',
    'eurofighter':'typhoon','a10':'a10','l159':'l159','miragef1':'miragef1',
    'ah64':'apache','uh60':'blackhawk','ch47':'chinook','s61':'s61',
    'f5':'f5_tiger','hawk':'bae_hawk','a319':'a319','a320':'a320',
    'a321':'a321','b737':'b738','a350':'a359','c17':'c17','c5':'c5',
    'a400m':'a400','p3':'p3_orion','e3':'e3awacs','e7':'e737','p8':'p8',
    'md11':'md11','b52':'b52','u2':'u2','v22':'v22_slow',
    'f15':'md_f15','b1b':'b1b_lancer','c390':'e390','tiger':'tiger',
    'a380':'a380','il62':'il_62','sr22':'cirrus_sr22','tornado':'tornado',
    'b707':'b707',
}
OL_REV='88e6ea19bdd11cb4196ce6a30304282776a50d89'
OL_BASE=f'https://github.com/alkissack/Dump1090-OpenLayers3-html/blob/{OL_REV}'
OL_MAPPING={
    'a300':'a306','a310':'a310','a318':'a318','a330':'a333','a340':'a346',
    'atr72':'at73','b727':'b722','b747':'b744','b757':'b752','b767':'b763',
    'b777':'b77w','b787':'b789','cessna172':'c172','h135':'e135',
}


def adapt_openlayers(names, refs, target):
    data=json.loads((ROOT/'third_party/openlayers/selected-shapes.json').read_text())
    ns='{http://www.w3.org/2000/svg}'
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    for model,shape in OL_MAPPING.items():
        source=data[shape]
        root=ET.fromstring(source['svg'])
        # Retain geometry, groups, transforms and source fill behaviour. The EC135
        # rotor outline is part of its compound path, so never replace it by a disk.
        for element in root.iter():
            if element.tag==ns+'style' and element.text:
                element.text=element.text.replace('black','#505a64')
            if element.get('stroke')=='black':
                element.set('stroke','#505a64')
        for parent in root.iter():
            for child in list(parent):
                if child.tag==ns+'title':
                    parent.remove(child)
        name=names[model]
        root.set('viewBox',source['fitted_viewBox'])
        root.set('width','400');root.set('height','400')
        root.set('role','img');root.set('aria-labelledby','title desc')
        ref={
            'source_page':OL_BASE+'/public_html/plMarkers.js',
            'image_url':f'https://raw.githubusercontent.com/alkissack/Dump1090-OpenLayers3-html/{OL_REV}/public_html/plMarkers.js',
            'source_shape':shape,
            'source_format':'Model-specific embedded SVG, inspected before adaptation',
            'local_image':f'reference-artwork/{model}.svg',
            'author':'Peter Lowden (FlyingPete); Dump1090-OpenLayers3-html contributors',
            'license':'GPL-2.0-only',
            'license_file':'third_party/openlayers/LICENSE',
            'attribution':'Aircraft SVG by Peter Lowden (FlyingPete), plMarkers.js build 6, 13 April 2017; preserved with repository licence and original credits.',
            'variant':{'a300':'Airbus A300-600 (A306)','atr72':'ATR 72 (AT73)','b727':'Boeing 727-200 (B722)','h135':'Eurocopter EC135 / Airbus H135'}.get(model,name),
            'view':'top','reviewed':True,
            'review_basis':'Embedded SVG rendered and inspected before adaptation; specific shape matched to catalogue variant. Not a manufacturer drawing.',
            'changes':'Palette and outline unified to #505a64; fitted viewBox; accessible labels; provenance metadata. Geometry and transforms retained.',
            'source_repairs':source['source_repairs'],
        }
        title=ET.Element(ns+'title',{'id':'title'});title.text=name
        desc=ET.Element(ns+'desc',{'id':'desc'});desc.text='Адаптація SVG-референсу Peter Lowden / Dump1090-OpenLayers3-html. Вигляд зверху; GPL-2.0-only.'
        metadata=ET.Element(ns+'metadata');metadata.text=json.dumps(ref,ensure_ascii=False)
        root.insert(0,title);root.insert(1,desc);root.insert(2,metadata)
        (target/(model+'.svg')).write_text(ET.tostring(root,encoding='unicode')+'\n')
        refs[model]=ref


def main():
    data=json.loads((ROOT/'third_party/tar1090/selected-shapes.json').read_text())
    refs=json.loads((ROOT/'references.json').read_text())
    names={line.split('|')[0]:line.split('|')[1] for rows in GROUPS.values() for line in rows.strip().splitlines()}
    target=ROOT/'reference-artwork'
    target.mkdir(exist_ok=True)
    for model,shape in MAPPING.items():
        source=data[shape]
        name=names[model]
        attribution='tar1090 contributors; modified/developed by Matthias Wirth; based on FlightAware dump1090. Individual source comments retained in third_party/tar1090/markers.js.'
        if shape in {'a319','a320','a321','b738'}:
            attribution+=' Refined A320/B737 SVGs credited upstream to pimlie.'
        ref={
            'source_page':BASE+'/html/markers.js',
            'image_url':f'https://raw.githubusercontent.com/wiedehopf/tar1090/{REV}/html/markers.js',
            'source_shape':shape,
            'source_format':'Model-specific SVG path data in upstream JavaScript; rendered and viewed before adaptation',
            'local_image':f'reference-artwork/{model}.svg',
            'author':'tar1090 contributors (see preserved source credits)',
            'license':'GPL-2.0-or-later',
            'license_file':'third_party/tar1090/LICENSE',
            'attribution':attribution,
            'variant':'F/A-18B Hornet (upstream F18H)' if model=='fa18' else name,
            'view':'top',
            'reviewed':True,
            'review_basis':'Source SVG viewed before adaptation; geometry retained, palette and framing adapted. This is an SVG reference, not an engineering drawing.',
            'changes':'Monochrome #505a64; accessible title/description; licence and provenance metadata. Source path geometry retained.',
        }
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{source["fitted_viewBox"]}" width="400" height="400" role="img" aria-labelledby="title desc">'
             f'<title id="title">{html.escape(name)}</title>'
             '<desc id="desc">Адаптація окремого SVG-референсу tar1090; вигляд зверху. GPL-2.0-or-later. Не технічне креслення.</desc>'
             '<metadata>'+html.escape(json.dumps(ref,ensure_ascii=False))+'</metadata>'
             '<g fill="#505a64">'+''.join(f'<path d="{html.escape(d,quote=True)}"/>' for d in source['paths'])+'</g></svg>\n')
        ET.fromstring(svg)
        (target/(model+'.svg')).write_text(svg)
        refs[model]=ref
    adapt_openlayers(names,refs,target)
    (ROOT/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
    print(f'Adapted {len(MAPPING)} tar1090 + {len(OL_MAPPING)} OpenLayers model-specific references')


if __name__=='__main__':
    main()

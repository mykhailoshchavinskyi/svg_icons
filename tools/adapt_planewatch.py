#!/usr/bin/env python3
"""Adapt inspected vector-only Plane Watch reference silhouettes.

The user approved CC BY-NC-SA artwork. Third-party embedded reference images
are excluded from the saved source vectors and all generated adaptations.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
if __package__:
    from .generate_catalog import GROUPS
else:
    from generate_catalog import GROUPS

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'third_party/planewatch'
REV='338826d35d1e30cca0464713001de5f2723a3aee'
BASE=f'https://github.com/plane-watch/pw-silhouettes/blob/{REV}'
NS='{http://www.w3.org/2000/svg}'
MODELS={
    'aw109','aw119','an124','aw139','an140','an148','an158','aw169',
    'an24','an28','dash8','e190','cessna182','cessna208','da42',
    'kingair350','bell206','bell412','r44','h125','pc12','pc21','pa28',
}


def main():
    sources=json.loads((SOURCE/'selected.json').read_text())
    refs=json.loads((ROOT/'references.json').read_text())
    names={line.split('|')[0]:line.split('|')[1] for rows in GROUPS.values() for line in rows.strip().splitlines()}
    ET.register_namespace('',NS[1:-1])
    for key in sorted(MODELS):
        source=sources[key]
        root=ET.parse(SOURCE/source['sanitized_file']).getroot()
        # Preserve path coordinates, transforms, draw order, stroke width and
        # opacity. Replace only the white/black source palette by the set's grey.
        for node in root.iter():
            assert node.tag.rsplit('}',1)[-1] not in {'image','script','foreignObject'}
            style=node.get('style')
            if style:
                declarations=[]
                for declaration in style.split(';'):
                    if not declaration:continue
                    prop,sep,value=declaration.partition(':')
                    if prop.strip() in {'fill','stroke'} and value.strip() not in {'none','transparent'}:
                        value='#505a64'
                    declarations.append(prop+sep+value)
                node.set('style',';'.join(declarations))
            for attr in ('fill','stroke'):
                if node.get(attr) and node.get(attr) not in {'none','transparent'}:
                    node.set(attr,'#505a64')
        root.set('fill','#505a64')
        root.set('viewBox',source['fitted_viewBox'])
        root.set('width','400');root.set('height','400')
        root.set('role','img');root.set('aria-labelledby','title desc')
        ref={
            'source_page':BASE+'/'+source['source_file'],
            'image_url':f'https://raw.githubusercontent.com/plane-watch/pw-silhouettes/{REV}/'+source['source_file'],
            'source_format':'Model-specific vector silhouette; embedded third-party reference artwork removed before viewing and adaptation',
            'source_shape':Path(source['source_file']).stem,
            'local_image':f'reference-artwork/{key}.svg',
            'author':'Plane Watch Contributors',
            'license':'CC-BY-NC-SA-4.0',
            'license_url':'https://creativecommons.org/licenses/by-nc-sa/4.0/',
            'license_file':'third_party/planewatch/LICENSE',
            'attribution':f"Aircraft silhouette by Plane Watch Contributors, pw-silhouettes, revision {REV}; adapted under CC BY-NC-SA 4.0.",
            'variant':names[key],
            'view':'top','reviewed':True,
            'review_basis':'Sanitized model-specific source SVG rendered and visually inspected before adaptation; geometry, transforms and static rotor/propeller frame retained.',
            'changes':'Embedded reference images and editor-only/hidden content removed; palette unified to #505a64; framing, accessibility and attribution added. No changes to vector coordinates.',
            'embedded_images_removed':source['embedded_images_removed'],
            'variant_note':source.get('variant_note',''),
        }
        for tag,text in [('title',names[key]),('desc','Вигляд зверху за SVG-референсом Plane Watch. Адаптація CC BY-NC-SA 4.0; лише некомерційне використання.'),('metadata',json.dumps(ref,ensure_ascii=False))]:
            element=ET.Element(NS+tag,{'id':tag} if tag in {'title','desc'} else {})
            element.text=text
            root.insert(0,element)
        (ROOT/'reference-artwork'/(key+'.svg')).write_text(ET.tostring(root,encoding='unicode')+'\n')
        refs[key]=ref
    (ROOT/'references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
    print(f'Adapted {len(MODELS)} inspected Plane Watch silhouettes (CC BY-NC-SA 4.0)')


if __name__=='__main__':
    main()

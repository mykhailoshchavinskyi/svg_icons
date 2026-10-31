#!/usr/bin/env python3
"""Rebuild original schematic SVG additions and the searchable offline catalog."""
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
COLOR = '#505a64'

# name | span/rotor diameter (m) | length (m) | planform | engines/blades
# Dimensions select approximate proportions, not engineering geometry.
GROUPS = {
    'Винищувачі та штурмовики': '''
f4|McDonnell Douglas F-4 Phantom II|11.7|19.2|swept|2
f5|Northrop F-5 Tiger II|8.1|14.5|swept|2
f14|Grumman F-14 Tomcat (крила розгорнуті)|19.5|19.1|swept|2
f15|McDonnell Douglas F-15 Eagle|13.1|19.4|swept|2
f16|General Dynamics F-16 Fighting Falcon|10|15|swept|1
fa18|McDonnell Douglas F/A-18 Hornet|11.4|17.1|swept|2
fa18e|Boeing F/A-18E Super Hornet|13.6|18.3|swept|2
f22|Lockheed Martin F-22 Raptor|13.6|18.9|stealth|2
f35|Lockheed Martin F-35 Lightning II|10.7|15.7|stealth|1
a10|Fairchild Republic A-10 Thunderbolt II|17.5|16.3|a10|2
av8b|McDonnell Douglas AV-8B Harrier II|9.3|14.1|swept|1
eurofighter|Eurofighter Typhoon|11|16|canard|2
rafale|Dassault Rafale|10.9|15.3|canard|2
gripen|Saab JAS 39 Gripen|8.4|14.1|canard|1
viggen|Saab 37 Viggen|10.6|16.4|canard|1
draken|Saab 35 Draken|9.4|15.4|double_delta|1
mirage2000|Dassault Mirage 2000|9.1|14.4|delta|1
mirage3|Dassault Mirage IIIE|8.2|15|delta|1
miragef1|Dassault Mirage F1|8.4|15.3|swept|1
jaguar|SEPECAT Jaguar|8.7|16.8|swept|2
tornado|Panavia Tornado (крила розгорнуті)|13.9|16.7|swept|2
mig15|МіГ-15|10.1|10.1|swept|1
mig17|МіГ-17|9.6|11.3|swept|1
mig19|МіГ-19|9|12.5|swept|2
mig23|МіГ-23 (крила розгорнуті)|14|16.7|swept|1
mig35|МіГ-35|12|17.3|swept|2
su7|Су-7|9.3|16.8|swept|1
su17|Су-17 (крила розгорнуті)|13.7|19|swept|1
su33|Су-33|14.7|21.2|canard|2
su37|Су-37|14.7|21.9|canard|2
j7|Chengdu J-7|8.3|14.9|delta|1
j10|Chengdu J-10|9.8|16.9|canard|1
j20|Chengdu J-20|13|20.4|stealth_canard|2
jf17|PAC / Chengdu JF-17 Thunder|9.5|14.9|swept|1
tejas|HAL Tejas|8.2|13.2|delta|1
kf21|KAI KF-21 Boramae|11.2|16.9|stealth|2
f104|Lockheed F-104 Starfighter|6.7|16.7|stub|1
f86|North American F-86 Sabre|11.3|11.4|swept|1
f100|North American F-100 Super Sabre|11.8|15.2|swept|1
f117|Lockheed F-117 Nighthawk|13.2|20.1|faceted|2
''',
    'Бомбардувальники та спеціальна авіація': '''
b1b|Rockwell B-1B Lancer (крила розгорнуті)|41.8|44.5|bomber|4
b2|Northrop Grumman B-2 Spirit|52.4|21|flyingwing|2
b52|Boeing B-52 Stratofortress|56.4|48.5|b52|8
b21|Northrop Grumman B-21 Raider (умовний силует)|40|16|flyingwing|2
tu16|Ту-16|33|34.8|bomber|2
tu22|Ту-22|23.2|41.6|bomber|2
h6|Xian H-6|33|34.8|bomber|2
e2|Grumman E-2 Hawkeye|24.6|17.6|awacs_prop|2
e3|Boeing E-3 Sentry|44.4|46.6|awacs|4
e7|Boeing E-7 Wedgetail|35.8|33.6|wedgetail|2
p3|Lockheed P-3 Orion|30.4|35.6|prop|4
p8|Boeing P-8 Poseidon|37.6|39.5|jet|2
kc135|Boeing KC-135 Stratotanker|39.9|41.5|jet|4
kc46|Boeing KC-46 Pegasus|47.6|50.5|jet|2
u2|Lockheed U-2|31.4|19.2|glider|1
sr71|Lockheed SR-71 Blackbird|16.9|32.7|sr71|2
be200|Берєв Бе-200|32.8|32|amphibian|2
cl415|Canadair CL-415|28.6|19.8|amphibian_prop|2
''',
    'Транспортні та вантажні літаки': '''
c5|Lockheed C-5 Galaxy|67.9|75.3|transport|4
c17|Boeing C-17 Globemaster III|51.8|53|transport|4
c130|Lockheed Martin C-130J-30 Super Hercules|40.4|34.4|prop|4
c27j|Leonardo C-27J Spartan|28.7|22.7|prop|2
c295|Airbus C295 Persuader|25.8|24.5|prop|2
a400m|Airbus A400M Atlas|42.4|45.1|prop|4
an2|Ан-2|18.2|12.7|biplane|1
an24|Ан-24|29.2|23.5|prop|2
an28|Ан-28|22|13.1|prop|2
an32|Ан-32|29.2|23.8|prop|2
an70|Ан-70|44.1|40.7|prop|4
an124|Ан-124 Руслан|73.3|69.1|transport|4
an140|Ан-140|25.5|22.6|prop|2
an148|Ан-148|28.9|29.1|transport|2
an158|Ан-158|28.9|31.6|transport|2
an178|Ан-178|30.6|32.9|transport|2
an225|Ан-225 Мрія|88.4|84|twin_tail_transport|6
il112|Іл-112В|27.6|24.2|prop|2
il114|Іл-114|30|26.9|prop|2
c390|Embraer C-390 Millennium|35.1|35.2|transport|2
y20|Xian Y-20|45|47|transport|4
do228|Dornier 228|17|16.6|prop|2
dhc6|De Havilland Canada DHC-6 Twin Otter|19.8|15.8|prop|2
''',
    'Пасажирські літаки': '''
a220|Airbus A220-300|35.1|38.7|jet|2
a300|Airbus A300|44.8|54.1|jet|2
a310|Airbus A310|43.9|46.7|jet|2
a318|Airbus A318|34.1|31.4|jet|2
a319|Airbus A319|34.1|33.8|jet|2
a320|Airbus A320|35.8|37.6|jet|2
a321|Airbus A321|35.8|44.5|jet|2
a330|Airbus A330-300|60.3|63.7|jet|2
a340|Airbus A340-600|63.5|75.4|jet|4
a350|Airbus A350-900|64.8|66.8|jet|2
a380|Airbus A380|79.8|72.7|jet|4
b707|Boeing 707|44.4|46.6|jet|4
b717|Boeing 717-200|28.4|37.8|rearjet|2
b727|Boeing 727|32.9|46.7|trijet|3
b737|Boeing 737-800|35.8|39.5|jet|2
b747|Boeing 747-400|64.4|70.7|jumbo|4
b757|Boeing 757-200|38.1|47.3|jet|2
b767|Boeing 767-300|47.6|54.9|jet|2
b777|Boeing 777-300ER|64.8|73.9|jet|2
b787|Boeing 787-9|60.1|62.8|jet|2
atr42|ATR 42-500|24.6|22.7|prop|2
atr72|ATR 72|27.1|27.2|prop|2
dash8|De Havilland Canada Dash 8-400|28.4|32.8|prop|2
crj900|Bombardier CRJ900|24.9|36.2|rearjet|2
e175|Embraer E175|26|31.7|jet|2
e190|Embraer E190|28.7|36.2|jet|2
e195e2|Embraer E195-E2|35.1|41.5|jet|2
ssj100|Sukhoi Superjet 100|27.8|29.9|jet|2
ms21|МC-21|35.9|42.2|jet|2
c919|COMAC C919|35.8|38.9|jet|2
arj21|COMAC ARJ21|27.3|33.5|rearjet|2
tu134|Ту-134|29|37.1|rearjet|2
tu154|Ту-154|37.6|47.9|trijet|3
tu204|Ту-204-100|41.8|46.1|jet|2
il62|Іл-62|43.2|53.1|rearjet|4
il86|Іл-86|48.1|59.5|jet|4
il96|Іл-96|60.1|55.3|jet|4
yak40|Як-40|25|20.4|trijet|3
yak42|Як-42|34.9|36.4|trijet|3
dc3|Douglas DC-3|29|19.7|prop|2
dc9|McDonnell Douglas DC-9|28.4|36.4|rearjet|2
dc10|McDonnell Douglas DC-10|50.4|55.5|wide_trijet|3
md11|McDonnell Douglas MD-11|51.7|61.2|wide_trijet|3
concorde|Aérospatiale / BAC Concorde|25.6|61.7|concorde|4
tu144|Ту-144|28.8|65.5|concorde_canard|4
''',
    'Легка, навчальна та ділова авіація': '''
cessna172|Cessna 172 Skyhawk|11|8.3|light|1
cessna182|Cessna 182 Skylane|11|8.8|light|1
cessna208|Cessna 208 Caravan|15.9|12.7|light|1
pc12|Pilatus PC-12|16.3|14.4|light|1
pc21|Pilatus PC-21|9.1|11.2|trainer_prop|1
tbm940|Daher TBM 940|12.8|10.7|light|1
sr22|Cirrus SR22|11.7|7.9|light|1
pa28|Piper PA-28 Cherokee|10.7|7.2|light|1
da40|Diamond DA40|11.9|8.1|light|1
da42|Diamond DA42 Twin Star|13.4|8.6|light_twin|2
kingair350|Beechcraft King Air 350|17.7|14.2|prop|2
learjet75|Bombardier Learjet 75|15.5|17.7|rearjet|2
challenger650|Bombardier Challenger 650|19.6|20.9|rearjet|2
global7500|Bombardier Global 7500|31.8|33.8|rearjet|2
g650|Gulfstream G650|30.4|30.4|rearjet|2
falcon7x|Dassault Falcon 7X|26.2|23.4|trijet|3
citationx|Cessna Citation X|19.4|22|rearjet|2
hondajet|HondaJet HA-420|12.1|13|overwing|2
l39|Aero L-39 Albatros|9.5|12.1|trainer|1
l159|Aero L-159 ALCA|9.5|12.7|trainer|1
yak130|Як-130|9.8|11.5|trainer|2
m346|Leonardo M-346 Master|9.7|11.5|trainer|2
t50|KAI T-50 Golden Eagle|9.5|13.1|swept|1
hawk|BAE Systems Hawk|9.4|12.4|trainer|1
t6|Beechcraft T-6 Texan II|10.2|10.2|trainer_prop|1
super_tucano|Embraer A-29 Super Tucano|11.1|11.3|trainer_prop|1
spitfire|Supermarine Spitfire|11.2|9.1|elliptic|1
p51|North American P-51 Mustang|11.3|9.8|trainer_prop|1
bf109|Messerschmitt Bf 109|9.9|9|trainer_prop|1
po2|По-2|11.4|8.2|biplane|1
''',
    'Гелікоптери та конвертоплани': '''
ah1|Bell AH-1 Cobra|13.4|13.6|attack_heli|2
ah64|Boeing AH-64 Apache|14.6|15.1|attack_heli|4
rah66|Boeing–Sikorsky RAH-66 Comanche|11.9|14.3|attack_heli|5
uh1|Bell UH-1 Iroquois|14.6|12.7|heli|2
uh60|Sikorsky UH-60 Black Hawk|16.4|15.3|heli|4
sh60|Sikorsky SH-60 Seahawk|16.4|15.3|naval_heli|4
ch47|Boeing CH-47 Chinook|18.3|16|tandem|3
ch46|Boeing Vertol CH-46 Sea Knight|15.5|13.9|tandem|3
ch53|Sikorsky CH-53E Super Stallion|24.1|22.4|heavy_heli|7
ch53k|Sikorsky CH-53K King Stallion|24.1|22.3|heavy_heli|7
s61|Sikorsky S-61 Sea King|18.9|17|naval_heli|5
s76|Sikorsky S-76|13.4|13.2|heli|4
s92|Sikorsky S-92|17.2|17.1|heli|4
bell47|Bell 47|10.7|9.6|bubble_heli|2
bell206|Bell 206 JetRanger|10.2|10|heli|2
bell212|Bell 212|14.6|12.9|heli|2
bell412|Bell 412|14|12.9|heli|4
bell429|Bell 429 GlobalRanger|11|11.7|heli|4
bell505|Bell 505 Jet Ranger X|10.2|10.5|bubble_heli|2
r22|Robinson R22|7.7|6.6|bubble_heli|2
r44|Robinson R44|10.1|9|bubble_heli|2
r66|Robinson R66|10.1|9|bubble_heli|2
h125|Airbus H125 / AS350 Écureuil|10.7|10.9|heli|3
h130|Airbus H130|10.7|10.7|fenestron|3
h135|Airbus H135|10.2|10.2|fenestron|4
h145|Airbus H145 (п’ятилопатевий)|10.8|11.7|fenestron|5
h155|Airbus H155 / EC155|12.6|12.7|fenestron|5
h160|Airbus H160|12|13.9|fenestron|5
h175|Airbus H175|14.8|15.7|heli|5
h225|Airbus H225 Super Puma|16.2|16.8|heli|5
as532|Airbus AS532 Cougar|15.6|15.5|heli|4
as565|Airbus AS565 Panther|11.9|11.4|fenestron|4
tiger|Airbus Tiger|13|14.1|attack_heli|4
nh90|NHIndustries NH90|16.3|16.1|heli|4
aw101|Leonardo AW101 Merlin|18.6|19.5|heavy_heli|5
aw109|Leonardo AW109|10.8|11.4|heli|4
aw119|Leonardo AW119 Koala|10.8|11.4|heli|4
aw129|Agusta A129 Mangusta|11.9|12.3|attack_heli|4
aw139|Leonardo AW139|13.8|13.8|heli|5
aw169|Leonardo AW169|12.1|12.2|heli|5
aw189|Leonardo AW189|14.6|14.6|heli|5
aw609|Leonardo AW609|10|13.4|tiltrotor|3
mi2|Мі-2|14.5|11.4|heli|3
mi4|Мі-4|21|16.8|heli|4
mi6|Мі-6|35|33.2|heavy_heli|5
mi14|Мі-14|21.3|18.4|naval_heli|5
mi17|Мі-17|21.3|18.4|heli|5
mi35|Мі-35М|17.2|17.5|attack_heli|5
mi38|Мі-38|21.1|19.9|heli|6
ka27|Ка-27|15.9|11.3|coaxial|3
ka29|Ка-29|15.9|11.3|coaxial_attack|3
ka31|Ка-31|15.9|11.6|coaxial_radar|3
ka32|Ка-32|15.9|11.3|coaxial|3
ka50|Ка-50|14.5|13.5|coaxial_attack|3
ka226|Ка-226|13|8.1|coaxial|3
ansat|Казань Ансат|11.5|11.5|heli|4
dhruv|HAL Dhruv|13.2|13.5|heli|4
prachand|HAL Prachand|13.2|15.8|attack_heli|4
z10|CAIC Z-10|13|14.2|attack_heli|5
z19|Harbin Z-19|11.9|12|fenestron_attack|4
z20|Harbin Z-20|16|15|heli|5
v22|Bell Boeing V-22 Osprey|11.6|17.5|tiltrotor|3
v280|Bell V-280 Valor|10.7|15.4|tiltrotor|3
kmax|Kaman K-MAX|14.7|12.7|intermeshing|2
''',
}


def polygon(points, **attrs):
    return '<polygon points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in points) + '"' + ''.join(f' {k}="{v}"' for k, v in attrs.items()) + '/>'


def aircraft(span, length, kind, engines, model):
    s = min(280 / span, 352 / length)
    half, height = span * s / 2, length * s
    top = (400 - height) / 2
    def pt(x, y):
        return (160 + x * half, top + y * height)
    out = []
    def poly(coords):
        out.append(polygon([pt(x, y) for x, y in coords]))
    def pair(coords):
        poly(coords)
        poly([(-x, y) for x, y in coords])
    def ellipse(x, y, rx, ry, extra=''):
        cx, cy = pt(x, y)
        out.append(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx * half:.2f}" ry="{ry * height:.2f}" {extra}/>')
    if kind == 'flyingwing':
        poly([(0, 0), (1, .79), (.62, .72), (.48, .88), (.3, .79), (.17, 1), (0, .89), (-.17, 1), (-.3, .79), (-.48, .88), (-.62, .72), (-1, .79)])
        return ''.join(out)
    fighter = kind in {'swept', 'stealth', 'canard', 'delta', 'double_delta', 'stealth_canard', 'stub', 'faceted', 'sr71'}
    width = .10 if fighter else .075
    if kind in {'light', 'light_twin', 'trainer_prop', 'elliptic', 'biplane', 'trainer'}:
        width = .08
    if kind == 'faceted':
        poly([(0, 0), (.16, .24), (1, .75), (.48, .87), (.35, 1), (0, .88), (-.35, 1), (-.48, .87), (-1, .75), (-.16, .24)])
        return ''.join(out)
    # Smooth fuselage with nose facing upwards.
    x, y = pt(0, 0)
    out.append(f'<path d="M{x:.2f} {y:.2f} C{160-width*half:.2f} {top+height*.06:.2f} {160-width*half:.2f} {top+height*.13:.2f} {160-width*half:.2f} {top+height*.27:.2f} L{160-width*half:.2f} {top+height*.73:.2f} Q{160-width*half*.6:.2f} {top+height*.95:.2f} 160 {top+height:.2f} Q{160+width*half*.6:.2f} {top+height*.95:.2f} {160+width*half:.2f} {top+height*.73:.2f} L{160+width*half:.2f} {top+height*.27:.2f} C{160+width*half:.2f} {top+height*.13:.2f} {160+width*half:.2f} {top+height*.06:.2f} {x:.2f} {y:.2f}Z"/>')
    straight = kind in {'prop', 'light', 'light_twin', 'trainer_prop', 'biplane', 'awacs_prop', 'glider', 'amphibian_prop', 'a10'}
    wings = {
        'f14': [(.07,.38),(.48,.42),(1,.50),(.97,.59),(.35,.61),(.07,.68)],
        'f15': [(.10,.35),(.50,.43),(1,.63),(.90,.69),(.27,.67),(.10,.61)],
        'f16': [(.07,.38),(.34,.44),(1,.64),(.97,.71),(.14,.64)],
        'fa18': [(.07,.29),(.20,.46),(1,.62),(.95,.73),(.15,.65)],
        'fa18e': [(.07,.28),(.26,.45),(1,.60),(1,.73),(.19,.66)],
        'f22': [(.10,.33),(1,.61),(.65,.76),(.13,.65)],
        'f35': [(.12,.36),(1,.61),(.92,.73),(.14,.65)],
        'f4': [(.09,.36),(.73,.56),(1,.59),(.97,.69),(.18,.66)],
        'f5': [(.08,.44),(1,.61),(.90,.69),(.08,.62)],
        'av8b': [(.08,.34),(1,.47),(.95,.57),(.08,.53)],
        'mig15': [(.07,.33),(1,.52),(.97,.66),(.07,.55)],
        'mig17': [(.07,.29),(1,.55),(.96,.67),(.07,.55)],
        'mig19': [(.07,.32),(1,.62),(.93,.72),(.07,.58)],
        'mig23': [(.08,.37),(.45,.43),(1,.48),(.98,.57),(.12,.62)],
        'tornado': [(.08,.37),(.43,.42),(1,.52),(.97,.62),(.12,.66)],
        'j20': [(.10,.35),(1,.67),(.85,.82),(.13,.72)],
        'su33': [(.09,.32),(.36,.47),(1,.69),(.94,.76),(.15,.67)],
        'su37': [(.09,.31),(.35,.46),(1,.68),(.94,.76),(.15,.66)],
        'kf21': [(.10,.36),(1,.62),(.83,.74),(.13,.65)],
    }
    if model in wings:
        pair(wings[model])
    elif kind == 'elliptic':
        for sign in [-1, 1]:
            a, b = pt(.06*sign, .37)
            c, d = pt(sign, .33)
            e, f = pt(sign, .55)
            g, h = pt(.06*sign, .59)
            out.append(f'<path d="M{a:.2f} {b:.2f} Q{c:.2f} {d:.2f} {e:.2f} {f:.2f} Q{e:.2f} {h:.2f} {g:.2f} {h:.2f}Z"/>')
    elif kind in {'delta', 'canard', 'stealth_canard', 'double_delta', 'concorde', 'concorde_canard', 'sr71'}:
        leading = .25 if kind in {'delta', 'concorde', 'concorde_canard', 'sr71'} else .36
        coords = [(.07, leading), (1, .79), (.94, .85), (.07, .81)]
        if kind == 'double_delta':
            coords = [(.06, .2), (.48, .47), (1, .74), (.92, .84), (.06, .8)]
        pair(coords)
    elif kind == 'stub':
        pair([(.07, .48), (1, .55), (1, .65), (.07, .64)])
    elif straight:
        pair([(.06, .4), (1, .43), (.98, .53), (.06, .57)])
    else:
        pair([(.06, .34), (1, .61), (.97, .72), (.06, .58)])
    if kind == 'biplane':
        pair([(.06, .56), (.87, .58), (.87, .66), (.06, .68)])
    tailless = kind in {'delta', 'double_delta', 'canard', 'stealth_canard', 'concorde', 'concorde_canard'}
    if not tailless:
        pair([(.025, .79), (.38, .91), (.36, .98), (.025, .93)])
    if kind in {'canard', 'stealth_canard', 'concorde_canard'}:
        pair([(.06, .24), (.38, .31), (.32, .36), (.06, .33)])
    if model in {'f14','f15','fa18','fa18e','f22','f35','mig35','su33','su37','j20','kf21'}:
        # Broad aft body, paired fins and engine nozzles distinguish twin-tail jets.
        pair([(.06,.50),(.22,.62),(.21,.91),(.07,.94)])
        pair([(.16,.73),(.31,.84),(.30,.94),(.17,.89)])
    if model in {'f22','f35','kf21'}:
        pair([(.08,.78),(.43,.88),(.30,.98),(.08,.91)])
    # Nacelles are positioned by propulsion arrangement.
    rear = kind in {'rearjet', 'trijet', 'a10'}
    underwing = kind in {'jet', 'jumbo', 'transport', 'twin_tail_transport', 'b52', 'bomber', 'awacs', 'wedgetail', 'wide_trijet', 'overwing', 'amphibian'}
    if rear:
        for sign in [-1, 1]:
            ellipse(sign*.2, .76, .065, .09)
            if engines == 4:
                ellipse(sign*.32, .76, .055, .09)
    elif underwing:
        count = 2 if kind == 'wide_trijet' else engines
        if count == 8:
            positions = [.37, .46, .7, .79]
        else:
            positions = {2: [.38], 4: [.35, .67], 6: [.29, .52, .76]}.get(count, [.38])
        for sign in [-1, 1]:
            for pos in positions:
                ellipse(sign*pos, .43+pos*.22, .045 if count>4 else .055, .065)
    elif fighter and engines == 2:
        for sign in [-1, 1]:
            poly([(sign*.045, .57), (sign*.19, .55), (sign*.18, .91), (sign*.045, .91)])
    prop = straight and kind not in {'glider', 'a10'} or kind == 'elliptic'
    if prop:
        positions = [0] if engines == 1 else [-.43, .43] if engines == 2 else [-.7, -.35, .35, .7]
        for pos in positions:
            py = .03 if engines == 1 else .39
            if engines > 1:
                ellipse(pos, .46, .045, .10)
            a, b = pt(pos-.11, py)
            c, d = pt(pos+.11, py+.012)
            out.append(f'<path d="M{a:.2f} {b:.2f} L{c:.2f} {d:.2f}" stroke="{COLOR}" stroke-width="3" stroke-linecap="round"/>')
    if kind in {'trijet', 'wide_trijet'}:
        ellipse(0, .86, .045, .085)
    if kind in {'awacs', 'awacs_prop'}:
        ellipse(0, .59, .28, .075)
        ellipse(0, .59, .24, .052, 'fill="none" stroke="white" stroke-opacity=".45" stroke-width="1.5"')
    if kind == 'wedgetail':
        poly([(-.055, .44), (.055, .44), (.055, .77), (-.055, .77)])
    if kind in {'twin_tail_transport', 'a10'}:
        for sign in [-1, 1]:
            poly([(sign*.25, .85), (sign*.28, .84), (sign*.28, .98), (sign*.25, .98)])
    if kind == 'sr71':
        for sign in [-1, 1]:
            ellipse(sign*.58, .64, .13, .27)
    if kind == 'jumbo':
        ellipse(0, .14, width*.65, .09, 'fill="white" fill-opacity=".2"')
    return ''.join(out)


def helicopter(diameter, length, kind, blades):
    # Reserve full rotor envelopes, including both disks on tandem aircraft.
    tandem = kind == 'tandem'
    tilt = kind == 'tiltrotor'
    scale = min(270/(diameter*(2.15 if tilt else 1.18 if kind=='intermeshing' else 1)), 350/(length+diameter*.7))
    r = diameter*scale/2
    body = length*scale
    front = 200-body*.46
    hub = front+body*.30
    out=[]
    def rotor(cx, cy, radius, phase=0, opacity=1):
        out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{radius:.2f}" fill="{COLOR}" fill-opacity=".10"/>')
        for i in range(blades):
            angle=phase+360*i/blades
            out.append(f'<path d="M{cx-2:.2f} {cy:.2f} L{cx-3:.2f} {cy-radius*.93:.2f} L{cx+3:.2f} {cy-radius*.96:.2f} L{cx+2:.2f} {cy:.2f}Z" transform="rotate({angle:.2f} {cx:.2f} {cy:.2f})" opacity="{opacity}"/>')
        out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="5"/>')
    w=body*(.044 if 'attack' in kind else .08)
    if kind == 'bubble_heli':
        w=body*.09
    end=front+body
    out.append(f'<path d="M160 {front:.2f} Q{160-w:.2f} {front:.2f} {160-w:.2f} {front+body*.18:.2f} L{160-w:.2f} {front+body*.43:.2f} Q{160-w:.2f} {front+body*.55:.2f} 160 {front+body*.58:.2f} Q{160+w:.2f} {front+body*.55:.2f} {160+w:.2f} {front+body*.43:.2f} L{160+w:.2f} {front+body*.18:.2f} Q{160+w:.2f} {front:.2f} 160 {front:.2f}Z"/>')
    out.append(polygon([(160-w*.4,front+body*.50),(160+w*.4,front+body*.50),(163,end),(157,end)]))
    out.append(f'<rect x="{160-body*.14:.2f}" y="{end-body*.12:.2f}" width="{body*.28:.2f}" height="4" rx="1"/>')
    if 'attack' in kind or tilt:
        wing= r*1.1 if tilt else body*.22
        out.append(polygon([(160-wing,hub+body*.08),(160+wing,hub+body*.08),(160+wing,hub+body*.12),(160-wing,hub+body*.12)]))
    if kind in {'heavy_heli','naval_heli'}:
        for sign in [-1,1]:
            out.append(f'<ellipse cx="{160+sign*w*1.25:.2f}" cy="{front+body*.40:.2f}" rx="{w*.6:.2f}" ry="{body*.16:.2f}"/>')
    if tandem:
        # Long cabin bridging the fore and aft rotor masts.
        out.append(f'<rect x="{160-w:.2f}" y="{front+body*.2:.2f}" width="{2*w:.2f}" height="{body*.65:.2f}" rx="{w*.7:.2f}"/>')
        rotor(160,front+body*.18,r,0)
        rotor(160,front+body*.82,r,60)
    elif tilt:
        for sign in [-1,1]:
            cx=160+sign*r*1.1
            out.append(f'<ellipse cx="{cx:.2f}" cy="{hub+body*.05:.2f}" rx="5" ry="{body*.10:.2f}"/>')
            rotor(cx,hub,r,30)
        out.append(polygon([(160-body*.2,end-body*.10),(160,end-body*.18),(160+body*.2,end-body*.10),(160+body*.17,end),(160,end-body*.08),(160-body*.17,end)]))
    elif kind=='intermeshing':
        rotor(160-r*.15,hub,r,0,.85)
        rotor(160+r*.15,hub,r,90,.85)
    else:
        rotor(160,hub,r,15)
        if kind.startswith('coaxial'):
            rotor(160,hub,r*.96,75,.7)
            if kind == 'coaxial_radar':
                out.append(f'<rect x="{160-w*1.8:.2f}" y="{front+body*.6:.2f}" width="{w*3.6:.2f}" height="5"/>')
        elif 'fenestron' in kind:
            out.append(f'<ellipse cx="166" cy="{end-8:.2f}" rx="4" ry="10" fill="none" stroke="{COLOR}" stroke-width="3"/>')
        else:
            out.append(f'<path d="M166 {end-17:.2f} V{end+5:.2f}" stroke="{COLOR}" stroke-width="3" stroke-linecap="round"/>')
    return ''.join(out)


def main():
    existing = {'a50':'А-50', 'an12':'Ан-12', 'an22':'Ан-22 Антей', 'an26':'Ан-26', 'an72':'Ан-72', 'il76':'Іл-76', 'il78':'Іл-78', 'ka52':'Ка-52', 'mi24':'Мі-24', 'mi26':'Мі-26', 'mi28':'Мі-28', 'mi8':'Мі-8', 'mig21':'МіГ-21', 'mig25':'МіГ-25', 'mig27':'МіГ-27', 'mig29':'МіГ-29', 'mig31':'МіГ-31', 'su24':'Су-24', 'su25':'Су-25', 'su27':'Су-27', 'su30':'Су-30', 'su34':'Су-34', 'su35':'Су-35', 'su47':'Су-47', 'su57':'Су-57', 'tu160':'Ту-160', 'tu22m':'Ту-22М', 'tu95':'Ту-95'}
    records=[{'id':key,'name':value,'category':'Початковий набір','file':key+'.svg','original':True,'artwork':'original'} for key,value in existing.items()]
    for category, rows in GROUPS.items():
        for line in rows.strip().splitlines():
            key,name,span,length,kind,count=line.split('|')
            assert key not in {r['id'] for r in records}, key
            span,length,count=float(span),float(length),int(count)
            is_heli=category=='Гелікоптери та конвертоплани'
            drawing=helicopter(span,length,kind,count) if is_heli else aircraft(span,length,kind,count,key)
            title=html.escape(name)
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 400" width="320" height="400" role="img" aria-labelledby="title desc"><title id="title">{title}</title><desc id="desc">Схематичний вигляд зверху; не є точним кресленням.</desc><g fill="{COLOR}">{drawing}</g></svg>\n'
            override = ROOT/'tools'/'overrides'/(key+'.svg')
            if override.is_file():
                svg = override.read_text()
            reference_override=ROOT/'reference-artwork'/(key+'.svg')
            if reference_override.is_file():
                svg=reference_override.read_text()
            ET.fromstring(svg)
            (ROOT/(key+'.svg')).write_text(svg)
            records.append({'id':key,'name':name,'category':category,'file':key+'.svg','original':False,'schematic':True,'span_or_rotor_m':span,'length_m':length,'profile':kind,'engines_or_blades':count})
            records[-1]['artwork'] = ('adaptation' if key in {'su33', 'su37', 'mig35'} else 'individual') if override.is_file() else 'template-draft'
            if records[-1]['artwork'] == 'adaptation':
                records[-1]['adapted_from'] = 'mig29.svg' if key == 'mig35' else 'su27.svg'
            if reference_override.is_file():
                records[-1]['artwork']='reference-adaptation'
    policy=json.loads((ROOT/'catalog-policy.json').read_text())
    references=json.loads((ROOT/'references.json').read_text())
    for record in records:
        ref=references.get(record['id'])
        if ref is not None:
            required={'source_page','image_url','author','license','attribution','variant','view','reviewed'}
            if not required.issubset(ref) or not all(ref[k] for k in required-{'reviewed'}):
                raise ValueError('Incomplete reference: '+record['id'])
            record['reference']=ref
        record['reference_status']='reviewed' if ref and ref.get('reviewed') is True else 'not-reviewed'
    excluded=[]
    for record in records:
        if record['id'] in policy['excluded']:
            record['scope_exclusion']=policy['excluded'][record['id']]
            excluded.append(record)
    records=[r for r in records if r['id'] not in policy['excluded']]
    (ROOT/'catalog-excluded.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    cards='\n'.join(f'<article data-category="{html.escape(r["category"],quote=True)}" data-search="{html.escape((r["id"]+" "+r["name"]).casefold(),quote=True)}"><a href="{r["file"]}"><img loading="lazy" src="{r["file"]}" alt="{html.escape(r["name"],quote=True)}"><span>{html.escape(r["name"])}</span><small>{r["file"]}</small><small>{"Початковий контур" if r["original"] else "Окремий контур" if r.get("artwork")=="individual" else "За SVG-референсом" if r.get("artwork")=="reference-adaptation" else "Адаптація спорідненої моделі" if r.get("artwork")=="adaptation" else "Шаблонна чернетка — потребує переробки"}</small>{"<small>CC BY-NC-SA · некомерційно</small>" if r.get("reference",{}).get("license")=="CC-BY-NC-SA-4.0" else ""}</a></article>' for r in records)
    options=''.join(f'<option>{html.escape(c)}</option>' for c in ['Початковий набір',*GROUPS])
    page='''<!doctype html><html lang="uk"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Каталог авіаційних силуетів</title>
<style>*{box-sizing:border-box}body{margin:0;background:#f1f4f7;color:#24313c;font:16px system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:32px}h1{margin-top:0}p{max-width:850px;line-height:1.6}.filters{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}label{display:flex;flex-direction:column;gap:6px;min-width:0;max-width:100%}input,select{min-width:0;max-width:100%;font:inherit;padding:10px;border:1px solid #aab7c2;border-radius:6px}#grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px}article{background:white;border:1px solid #dde4e9;border-radius:10px}article[hidden]{display:none}a{display:flex;flex-direction:column;align-items:center;padding:16px;text-align:center;color:inherit;text-decoration:none;height:100%}a:hover,a:focus-visible{outline:2px solid #39749e;border-radius:10px}img{width:130px;height:165px;object-fit:contain;margin-bottom:12px}small{color:#61717e;margin-top:6px}#empty{padding:20px}</style>
<main><h1>Авіаційні силуети</h1><p>Військові та цивільні моделі, що експлуатуються. Історичні типи та прототипи виключені з активного каталогу; актуальність решти кандидатів потребує перевірки. QUALITY_NOTE Натисніть картку, щоб відкрити SVG.</p>
<div class="filters"><label>Пошук моделі<input id="search" type="search" placeholder="Наприклад: Airbus, МіГ, UH-60"></label><label>Категорія<select id="category"><option value="">Усі категорії</option>OPTIONS</select></label></div><p id="count" role="status" aria-live="polite"></p><section id="grid" aria-label="Іконки моделей">CARDS</section><p id="empty" hidden>За цим запитом нічого не знайдено.</p></main>
<script>const cards=[...document.querySelectorAll('article')],search=document.getElementById('search'),category=document.getElementById('category');function filter(){const q=search.value.trim().toLowerCase();let n=0;for(const card of cards){card.hidden=!(card.dataset.search.includes(q)&&(!category.value||card.dataset.category===category.value));if(!card.hidden)n++}document.getElementById('count').textContent=`Показано ${n} із ${cards.length}`;document.getElementById('empty').hidden=n!==0}search.addEventListener('input',filter);category.addEventListener('change',filter);filter();</script></html>'''
    (ROOT/'index.html').write_text(page.replace('OPTIONS',options).replace('CARDS',cards).replace('QUALITY_NOTE', f"Актуальні моделі-кандидати: {len(records)}. За переглянутими SVG-референсами: {sum(r['artwork']=='reference-adaptation' for r in records)}. Початкові контури: {sum(r['artwork']=='original' for r in records)}. Окремі контури: {sum(r['artwork']=='individual' for r in records)}. Адаптації споріднених моделей: {sum(r['artwork']=='adaptation' for r in records)}. Шаблонні чернетки: {sum(r['artwork']=='template-draft' for r in records)} — вони потребують переробки й не відтворюють належно конкретні моделі. Нові контури є авторськими інтерпретаціями, не масштабними кресленнями."))
    print(f'{len(records)} catalog candidates; {len(excluded)} excluded from active catalog; SVG files preserved')


if __name__ == '__main__':
    main()

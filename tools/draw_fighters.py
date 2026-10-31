#!/usr/bin/env python3
"""Individually drawn planform studies. Writes only tools/overrides SVGs.

Coordinates are hand-authored per aircraft, in a nose-up frame. These are
interpretive silhouettes, not certified orthographic drawings. Mirroring is
shared; wing, body and tail outlines are specified separately for each model.
"""
from pathlib import Path
import html
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'tools'/'overrides'

# Half outlines, measured in drawing units about the longitudinal centreline.
# Each row supplies its own fuselage edge, wing and horizontal stabilator.
# The two-engine rear body is part of the outline, not an unrelated rectangle.
DRAWINGS = {
 'f4': ('McDonnell Douglas F-4 Phantom II',
 'M0 12 C7 21 12 43 13 65 L14 93 Q18 118 22 129 L29 145 L33 181 L31 256 L28 301 L27 348 L23 372 L5 372 L0 360Z',
 'M28 153 L83 207 L112 210 L118 229 L111 250 L35 263 L26 246Z',
 'M27 291 L71 337 L69 359 L25 344 L7 329Z',
 'M27 115 L36 137 L38 177 L29 182Z'),
 'f5': ('Northrop F-5 Tiger II',
 'M0 10 C4 19 8 37 9 59 L10 89 L12 116 L19 141 L22 179 L21 273 L20 330 L17 373 L3 373 L0 357Z',
 'M20 184 L101 235 L105 255 L96 260 L22 264Z',
 'M19 302 L61 342 L59 363 L18 348 L9 331Z',
 'M10 116 L21 132 L26 166 L20 181Z'),
 'f14': ('Grumman F-14 Tomcat — крила розгорнуті',
 'M0 10 C4 18 9 35 11 57 L12 85 L16 111 L29 139 L43 155 L47 186 L44 233 L40 266 L39 312 L36 368 L14 372 L10 337 L0 327Z',
 'M38 155 L62 160 L187 199 L190 216 L64 239 L44 257Z',
 'M38 280 L86 325 L84 356 L39 348 L17 331Z',
 'M30 248 L48 285 L46 331 L37 321Z'),
 'f15': ('McDonnell Douglas F-15 Eagle',
 'M0 10 C5 16 10 34 12 56 L13 87 L18 111 L33 133 L38 168 L38 251 L35 306 L32 367 L10 370 L7 340 L0 335Z',
 'M34 150 L128 228 L124 245 L62 265 L37 261Z',
 'M35 280 L76 322 L73 356 L34 342 L11 321Z',
 'M30 250 L45 283 L43 329 L34 321Z M20 119 L36 127 L42 157 L36 174 L22 146Z'),
 'fa18': ('McDonnell Douglas F/A-18 Hornet',
 'M0 10 C5 20 10 38 11 60 L12 83 Q14 108 22 126 L32 150 L34 180 L31 267 L27 315 L25 367 L8 369 L5 341 L0 332Z',
 'M28 178 L117 224 L119 250 L110 256 L30 271Z',
 'M26 290 L74 331 L71 359 L24 344 L8 325Z',
 'M12 92 Q23 113 33 139 L38 174 L28 193 L20 151Z M23 252 L47 283 L44 330 L27 316Z'),
 'fa18e': ('Boeing F/A-18E Super Hornet',
 'M0 10 C6 21 11 41 12 65 L13 91 Q16 115 26 132 L37 158 L39 188 L35 272 L31 320 L28 367 L9 370 L6 343 L0 334Z',
 'M33 180 L136 225 L137 257 L122 266 L34 278Z',
 'M29 295 L83 332 L79 362 L28 347 L10 326Z',
 'M13 96 Q31 115 40 145 L44 176 L33 196 L23 148Z M27 254 L53 283 L49 334 L31 318Z'),
 'f22': ('Lockheed Martin F-22 Raptor',
 'M0 10 L8 32 L13 58 L14 86 L25 111 L35 139 L41 180 L39 263 L35 319 L30 362 L9 363 L7 344 L0 341Z',
 'M31 147 L137 229 L90 275 L38 264Z',
 'M33 280 L84 326 L55 367 L27 345 L9 325Z',
 'M30 245 L59 278 L49 331 L33 314Z M16 105 L32 119 L40 161 L29 150Z'),
 'f35': ('Lockheed Martin F-35A Lightning II',
 'M0 10 C6 18 12 35 15 58 L16 85 L24 105 L30 127 L34 165 L33 250 L29 287 L24 324 L18 355 L16 372 L0 376Z',
 'M29 158 L125 235 L113 266 L34 263Z',
 'M27 279 L76 328 L58 361 L21 343 L8 320Z',
 'M25 240 L48 273 L43 319 L28 305Z M18 108 L34 126 L39 165 L29 160Z'),
 'a10': ('Fairchild Republic A-10 Thunderbolt II',
 'M0 12 C10 17 17 30 18 47 L18 88 L20 127 L22 185 L20 244 L15 293 L11 352 L0 366Z',
 'M20 143 L183 153 L186 169 L180 189 L20 203Z',
 'M11 310 L68 314 L70 337 L12 342Z',
 'M30 244 C43 238 49 247 49 263 L48 301 L32 306 L27 291 L27 259Z M58 302 L66 305 L67 348 L58 344Z'),
 'av8b': ('McDonnell Douglas AV-8B Harrier II',
 'M0 12 C6 18 11 36 12 56 L14 87 L24 108 L26 150 L24 207 L16 258 L11 317 L8 362 L0 374Z',
 'M24 133 L118 184 L119 209 L108 214 L23 205Z',
 'M12 283 L58 320 L57 341 L10 327 L4 310Z',
 'M14 91 Q31 100 33 126 L30 155 L23 166 L22 125Z M96 197 L103 196 L106 233 L100 239Z'),
 'eurofighter': ('Eurofighter Typhoon',
 'M0 10 C5 20 10 42 11 63 L12 92 L18 122 L24 158 L27 204 L27 278 L24 336 L20 369 L4 370 L0 347Z',
 'M23 146 L128 284 L123 301 L27 298 L17 278Z',
 '',
 'M13 104 L54 134 L48 157 L17 143Z M24 307 L30 333 L27 351 L21 342Z'),
 'rafale': ('Dassault Rafale',
 'M0 10 C5 17 10 36 11 58 L13 87 L20 116 L26 150 L29 198 L29 280 L26 337 L22 369 L5 370 L0 350Z',
 'M24 151 L133 274 L130 293 L111 300 L27 291Z',
 '',
 'M16 115 L60 144 L57 160 L23 151Z M18 112 L32 125 L36 158 L29 177Z'),
 'gripen': ('Saab JAS 39 Gripen',
 'M0 10 C5 18 10 38 11 60 L12 91 L18 118 L23 145 L25 202 L23 279 L19 333 L15 368 L0 375Z',
 'M21 158 L111 274 L106 288 L24 280Z',
 '',
 'M14 112 L49 133 L47 151 L20 143Z M15 105 L27 122 L30 149 L23 165Z'),
 'viggen': ('Saab 37 Viggen',
 'M0 10 C6 20 12 43 13 67 L14 94 L22 125 L29 161 L30 239 L26 313 L19 365 L0 374Z',
 'M25 162 L126 273 L118 294 L27 290Z',
 '',
 'M16 113 L66 141 L65 166 L25 160Z M19 106 L31 121 L36 158 L28 176Z'),
 'draken': ('Saab 35 Draken',
 'M0 10 C4 18 8 37 10 60 L12 93 L19 139 L24 198 L23 281 L17 346 L13 370 L0 375Z',
 'M12 91 L53 196 L116 276 L116 299 L24 295 L17 270Z',
 '',
 'M16 149 L25 166 L27 207 L21 218Z'),
 'mirage2000': ('Dassault Mirage 2000',
 'M0 10 C4 17 9 36 10 58 L11 90 L17 123 L22 164 L23 229 L21 290 L16 348 L13 370 L0 376Z',
 'M20 145 L116 282 L112 300 L23 296Z',
 '',
 'M13 105 L25 123 L29 157 L23 175Z'),
 'mirage3': ('Dassault Mirage III',
 'M0 10 C3 17 7 37 8 58 L10 91 L14 126 L19 170 L20 250 L17 316 L13 369 L0 375Z',
 'M16 133 L99 274 L96 294 L19 291Z',
 '',
 'M12 110 L23 128 L25 160 L19 175Z'),
 'miragef1': ('Dassault Mirage F1',
 'M0 10 C4 17 8 38 9 60 L11 94 L16 124 L19 171 L20 253 L16 318 L13 369 L0 375Z',
 'M18 164 L100 227 L99 252 L19 258Z',
 'M15 296 L55 337 L54 354 L13 342 L5 325Z',
 'M12 112 L23 129 L26 161 L19 176Z'),
 'jaguar': ('SEPECAT Jaguar',
 'M0 10 C4 17 8 36 10 57 L11 91 L15 120 L23 149 L26 192 L26 269 L23 322 L20 371 L5 372 L0 349Z',
 'M24 156 L95 218 L96 245 L27 248Z',
 'M22 293 L62 337 L58 358 L20 343 L8 324Z',
 'M13 114 L26 129 L31 169 L26 182Z'),
 'tornado': ('Panavia Tornado — крила розгорнуті',
 'M0 10 C5 17 10 37 12 60 L14 95 L21 125 L29 153 L33 192 L31 266 L28 319 L25 371 L7 372 L0 348Z',
 'M29 156 L49 160 L151 203 L153 226 L47 252 L31 258Z',
 'M26 291 L78 328 L76 356 L25 343 L8 321Z',
 'M21 116 L35 132 L39 173 L31 181Z'),
 'mig15': ('МіГ-15',
 'M0 12 Q12 12 17 24 L19 69 L22 119 L23 191 L20 264 L16 321 L13 367 L0 373Z',
 'M21 131 L183 237 L184 259 L169 267 L21 215Z',
 'M16 288 L71 333 L69 354 L14 332Z',
 ''),
 'mig17': ('МіГ-17',
 'M0 12 Q11 12 16 24 L18 73 L21 126 L21 198 L18 269 L14 328 L12 368 L0 374Z',
 'M20 125 L158 241 L159 264 L146 270 L19 221Z',
 'M15 292 L65 337 L63 356 L12 333Z',
 'M16 306 L21 340 L16 355Z'),
 'mig19': ('МіГ-19',
 'M0 12 Q13 12 18 26 L19 77 L24 132 L28 197 L28 266 L24 322 L21 370 L5 370 L0 349Z',
 'M25 132 L129 246 L128 266 L116 274 L26 235Z',
 'M24 290 L68 338 L66 358 L22 337 L9 318Z',
 ''),
 'mig23': ('МіГ-23 — крила розгорнуті',
 'M0 10 C4 17 9 38 10 60 L12 96 L18 124 L27 154 L30 193 L26 264 L21 320 L17 368 L0 375Z',
 'M27 155 L54 165 L155 197 L156 221 L49 250 L27 258Z',
 'M21 291 L72 335 L70 358 L18 339 L7 320Z',
 'M18 117 L33 132 L36 178 L28 184Z'),
 'su7': ('Су-7',
 'M0 10 L9 23 L14 38 L17 74 L19 131 L19 219 L16 294 L12 367 L0 374Z',
 'M18 135 L101 255 L99 276 L89 280 L18 230Z',
 'M15 289 L57 341 L55 358 L12 337Z',
 ''),
 'su17': ('Су-17 — крила розгорнуті',
 'M0 10 L9 24 L14 41 L17 84 L19 143 L20 221 L17 292 L13 368 L0 375Z',
 'M18 144 L58 186 L132 211 L133 234 L52 244 L19 239Z',
 'M16 294 L61 341 L59 360 L13 339Z',
 ''),
 'j7': ('Chengdu J-7',
 'M0 10 L8 24 L13 34 L15 78 L17 137 L18 231 L15 302 L11 368 L0 375Z',
 'M16 140 L101 281 L97 298 L18 280Z',
 'M14 301 L53 344 L51 360 L11 338Z',
 ''),
 'j10': ('Chengdu J-10',
 'M0 10 C4 18 9 39 11 61 L12 94 L17 127 L23 167 L24 233 L21 300 L15 367 L0 375Z',
 'M20 157 L109 280 L105 296 L23 283Z',
 '',
 'M14 109 L49 134 L47 151 L19 143Z'),
 'j20': ('Chengdu J-20',
 'M0 10 L6 28 L11 52 L14 83 L24 114 L31 147 L34 206 L34 279 L29 331 L25 370 L7 371 L0 349Z',
 'M29 177 L117 285 L112 305 L34 287Z',
 '',
 'M18 112 L61 147 L57 165 L27 150Z M29 268 L58 301 L48 345 L29 328Z M19 105 L33 125 L38 162 L29 180Z'),
 'jf17': ('PAC / Chengdu JF-17 Thunder',
 'M0 10 C4 18 9 40 10 61 L12 94 L18 127 L23 164 L24 234 L20 301 L15 368 L0 375Z',
 'M21 165 L117 235 L115 258 L24 271Z',
 'M18 294 L61 336 L58 356 L16 340 L6 324Z',
 'M14 109 L27 130 L31 164 L22 184Z'),
 'tejas': ('HAL Tejas',
 'M0 10 C4 18 9 37 11 60 L13 94 L19 127 L23 168 L23 238 L19 304 L14 367 L0 375Z',
 'M18 143 L48 190 L123 277 L119 295 L22 283Z',
 '',
 'M14 111 L27 129 L31 163 L23 182Z'),
 'kf21': ('KAI KF-21 Boramae',
 'M0 10 L7 28 L12 51 L14 84 L24 116 L33 147 L37 189 L35 269 L30 326 L26 370 L8 371 L0 347Z',
 'M31 160 L126 233 L113 265 L35 264Z',
 'M29 286 L80 333 L57 362 L26 345 L9 323Z',
 'M28 252 L51 282 L45 330 L29 312Z M18 107 L33 127 L40 161 L30 180Z'),
 'f104': ('Lockheed F-104 Starfighter',
 'M0 10 C3 18 7 38 8 60 L10 95 L15 134 L18 185 L18 256 L15 315 L12 368 L0 375Z',
 'M17 197 L72 224 L73 250 L18 245Z',
 'M14 303 L52 335 L51 352 L12 338Z',
 'M12 116 L23 133 L25 169 L18 183Z'),
 'f86': ('North American F-86 Sabre',
 'M0 12 Q12 12 17 25 L19 64 L23 112 L24 186 L21 263 L16 322 L12 368 L0 375Z',
 'M22 123 L177 221 L179 244 L163 257 L22 214Z',
 'M16 286 L72 329 L71 351 L14 331Z',
 ''),
 'f100': ('North American F-100 Super Sabre',
 'M0 12 Q10 12 15 23 L17 65 L20 120 L22 192 L20 263 L16 324 L13 368 L0 375Z',
 'M20 133 L137 239 L136 262 L123 271 L20 225Z',
 'M16 290 L67 335 L65 356 L13 335Z',
 ''),
 'f117': ('Lockheed F-117 Nighthawk',
 'M0 10 L22 78 L37 135 L43 204 L42 275 L31 335 L12 367 L0 357Z',
 'M22 78 L120 283 L88 301 L40 284Z',
 'M28 293 L70 336 L45 371 L10 345Z',
 'M29 256 L52 290 L44 332 L29 314Z'),
}


def write_drawing(key, spec):
    name, body, wing, tail, details = spec
    paths=[]
    for i,d in enumerate((body,wing,tail,details)):
        if not d:
            continue
        paths.append(f'<path id="p{i}" d="{d}"/><use href="#p{i}" transform="scale(-1 1)"/>')
    # M/L/C/Q/Z paths contain x/y coordinate pairs only; fit each individual span.
    xs=[]
    for d in (body,wing,tail,details):
        numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',d)]
        xs.extend(numbers[::2])
    half=max(abs(x) for x in xs)+10
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{210-half:g} 0 {2*half:g} 400" width="{2*half:g}" height="400" role="img" aria-labelledby="title desc">'
         f'<title id="title">{html.escape(name)}</title>'
         '<desc id="desc">Індивідуально побудований силует зверху. Авторська інтерпретація компонування, не масштабне креслення.</desc>'
         '<g fill="#505a64" stroke="#505a64" stroke-width=".4" stroke-linejoin="round" transform="translate(210 0)">'+''.join(paths)+'</g></svg>\n')
    ET.fromstring(svg)
    (OUT/(key+'.svg')).write_text(svg)


def flanker_variant(key, name, canard, fold=False):
    # Preserve the detailed inherited Flanker contour, which these variants share.
    root=ET.parse(ROOT/'su27.svg').getroot()
    ns='{http://www.w3.org/2000/svg}'
    root.set('role','img')
    root.set('aria-labelledby','title desc')
    title=ET.Element(ns+'title',{'id':'title'})
    title.text=name
    desc=ET.Element(ns+'desc',{'id':'desc'})
    desc.text='Адаптація початкового контуру Су-27: переднє горизонтальне оперення; умовне представлення модифікації.'
    root.insert(0,title)
    root.insert(1,desc)
    ET.SubElement(root,ns+'path',{'fill':'#505a64','d':canard})
    if fold:
        # Broader horizontal stabilators and carrier wingtip launch rails.
        ET.SubElement(root,ns+'path',{'fill':'#505a64','d':'M78 241 L34 277 L38 289 L75 284Z M128 241 L172 277 L168 289 L131 284Z'})
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.ElementTree(root).write(OUT/(key+'.svg'),encoding='unicode')


def main():
    OUT.mkdir(exist_ok=True)
    for key,spec in DRAWINGS.items():
        write_drawing(key,spec)
    flanker_variant('su33','Су-33','M82 123 L57 140 L59 147 L78 140Z M124 123 L149 140 L147 147 L128 140Z',True)
    flanker_variant('su37','Су-37','M83 123 L60 139 L62 145 L79 139Z M123 123 L146 139 L144 145 L127 139Z')
    ns='{http://www.w3.org/2000/svg}'
    root=ET.parse(ROOT/'mig29.svg').getroot()
    title=ET.Element(ns+'title',{'id':'title'})
    title.text='МіГ-35 — адаптація початкового контуру МіГ-29'
    root.insert(0,title)
    root.set('role','img')
    root.set('aria-labelledby','title')
    # Same aerodynamic family; preserve real contour rather than invent a new one.
    ET.ElementTree(root).write(OUT/'mig35.svg',encoding='unicode')
    print(f'Wrote {len(DRAWINGS)} individual drawings and 3 adaptations; F-16 retained')


if __name__=='__main__':
    main()

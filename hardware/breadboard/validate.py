"""Check conductive breadboard nets (not electronic behavior)."""
from pathlib import Path
import json, re, xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent
m=json.loads((D/'connections.json').read_text());parent={}
def group(h):
 if re.fullmatch('[a-j][0-9]+',h):
  assert 1<=int(h[1:])<=30,h
  return ('upper' if h[0]<='e' else 'lower')+h[1:]
 if re.fullmatch('[PNpn][0-9]+',h):
  assert 1<=int(h[1:])<=25,h
  return 'rail'+h[0]
 assert h in ['Mega.D8','Mega.5V','Mega.GND'],h
 return h
def find(a):
 parent.setdefault(a,a)
 if parent[a]!=a:parent[a]=find(parent[a])
 return parent[a]
def join(a,b):parent[find(a)]=find(b)
used={}
def use(h,label):
 assert h not in used,f'Hole conflict {h}: {used.get(h)} / {label}'
 used[h]=label
for name,h in m['components'].items():use(h,name);join(name,group(h))
for w in m['jumpers']:
 for h in [w['from'],w['to']]:use(h,w['name'])
 join(group(w['from']),group(w['to']))
expected=[{'Mega.D8','R1.1'},{'Mega.5V','D1.K','BZ1.+'},{'Mega.GND','Q1.E','R2.2'},{'R1.2','Q1.B','R2.1'},{'Q1.C','D1.A','BZ1.-'}]
roots=[]
for net in expected:
 rs={find(group(n) if n.startswith('Mega.') else n) for n in net};assert len(rs)==1,net;roots.extend(rs)
assert len(set(roots))==5,'Unexpected short between nets'
assert [m['components']['Q1.'+n] for n in ['E','B','C']]==['e12','e13','e14']
svg=ET.parse(D/'tabletop-wiring.svg');holes=[e for e in svg.iter() if e.get('fill')=='#50565c'];assert len(holes)==400,len(holes)
report='PASS: 5 expected circuit nets; no cross-net shorts.\nPASS: 400 breadboard holes (300 terminal + 100 rail).\nPASS: all component/jumper endpoints occupy unique holes.\nPASS: owner-confirmed E-B-C at e12/e13/e14.\nPASS: SVG XML parsed.\nScope: static connectivity check, not simulation or physical testing.\n'
(D/'validation.txt').write_text(report,encoding='utf-8');print(report)

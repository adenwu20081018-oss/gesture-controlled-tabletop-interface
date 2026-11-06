"""Generate the editable SVG and connection manifest; no simulation or firmware changes."""
from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape
import json
OUT=Path(__file__).resolve().parent
S=[]
def add(s):S.append(s)
def text(x,y,s,size=18,color='#25364a',anchor='start',weight='normal'):
 add(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>')
def rect(x,y,w,h,fill,rx=0,stroke='none'):
 add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
def circle(x,y,r,fill,stroke='none',sw=1):add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def path(points,color,width=6):
 d='M'+' L'.join(f'{x},{y}' for x,y in points)
 add(f'<path d="{d}" fill="none" stroke="white" stroke-width="{width+4}" stroke-linejoin="round" stroke-linecap="round"/>')
 add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>')
def hole(x,y):rect(x-4,y-4,8,8,'#50565c',2,'#c2c7cb')
rows={k:v for k,v in zip('abcdefghij',[360,388,416,444,472,552,580,608,636,664])}
def pt(h):return (700+28*(int(h[1:])-1),rows[h[0]])
def rail(n,which):return (710+28*(n-1)+28*((n-1)//5),{'P':280,'N':310,'p':720,'n':750}[which])
red='#cf3d3b';black='#242932';blue='#1686c4';purple='#8753b8'
connections=[]
def wire(name,a,b,points,color):
 connections.append({'name':name,'from':a,'to':b,'color':color})
 path(points,color)
 for x,y in [points[0],points[-1]]:circle(x,y,4,'#e8b95d','#353a40',1)
def resistor(a,b,label,bands):
 x1,y1=pt(a);x2,y2=pt(b);cx=(x1+x2)/2
 path([(x1,y1),(x2,y2)],'#a6adb4',3)
 rect(cx-40,y1-11,80,22,'#ddbf87',8,'#947949')
 for dx,c in zip([-25,-10,5,27],bands):rect(cx+dx,y1-11,5,22,c)
 rect(cx-58,y1-39,116,23,'#f4f3ef',3);text(cx,y1-20,label,17,anchor='middle',weight='bold')
add('<svg xmlns="http://www.w3.org/2000/svg" width="1700" height="800" viewBox="0 100 1700 800">')
add('<title>Mega 2560 and 400-point breadboard active buzzer wiring</title><desc>Owner-confirmed E-B-C transistor. Proposed hole placement of tested circuit, not a photograph or simulation.</desc>')
rect(0,100,1700,800,'#ffffff');text(55,160,'Breadboard Prototype',26,weight='bold')
for x,c,t in [(1120,red,'5V'),(1280,black,'GND'),(1450,blue,'D8')]:
 path([(x,153),(x+30,153)],c,4);text(x+42,160,t,17)
text(55,305,'Arduino Mega 2560',22,weight='bold')
# Official Arduino asset, retaining editable vector paths, no raster tracing.
mega=ET.parse(OUT/'mega-2560.svg').getroot();mega.set('x','55');mega.set('y','330');mega.set('width','520');mega.set('height','257')
add(ET.tostring(mega,encoding='unicode'))
scale=520/305.973
D8=(55+136.052*scale,330+7.2*scale);V=(55+125.972*scale,330+144*scale);G=(55+140.372*scale,330+144*scale)
# 30 × 10 terminal holes plus four 25-hole rails = 400.
rect(650,220,1000,585,'#dedfe0',17,'#c4c7cb');rect(657,225,986,570,'#f4f3ef',14)
rect(675,495,950,35,'#d2d3d3',5);rect(680,500,940,25,'#e7e7e3',3)
for k,y in rows.items():
 text(674,y+6,k,16,'#73797e',anchor='middle')
 for n in range(1,31):hole(*pt(k+str(n)))
for n in range(1,31):
 text(pt('a'+str(n))[0],341,str(n),13,'#6c737b',anchor='middle');text(pt('j'+str(n))[0],693,str(n),13,'#6c737b',anchor='middle')
for k in ['P','N','p','n']:
 y=rail(1,k)[1];c=red if k in ['P','p'] else '#465b77';text(677,y+5,'+' if k in ['P','p'] else '−',19,c)
 add(f'<path d="M690 {y-12} H1600" stroke="{c}" stroke-width="2"/>')
 for n in range(1,26):hole(*rail(n,k))
text(1150,251,'400-point half-size breadboard',18,anchor='middle',weight='bold')
wire('D8 to R1','Mega.D8','b4',[D8,(D8[0],270),(610,270),(610,388),pt('b4')],blue)
wire('5V supply','Mega.5V','P1',[V,(V[0],845),(625,845),(625,280),rail(1,'P')],red)
wire('Ground supply','Mega.GND','N1',[G,(G[0],823),(640,823),(640,310),rail(1,'N')],black)
wire('Ground rail bridge','N25','n25',[rail(25,'N'),(1620,310),(1620,750),rail(25,'n')],black)
wire('R2 ground','j18','n16',[pt('j18'),(pt('j18')[0],750),rail(16,'n')],black)
wire('Emitter ground','b12','N10',[pt('b12'),(980,388),(980,310),rail(10,'N')],black)
wire('Base to pull-down','b13','f13',[pt('b13'),(1125,388),(1125,535),(1036,535),pt('f13')],blue)
wire('5V to buzzer branch','P20','c23',[rail(20,'P'),(1316,280),pt('c23')],red)
wire('Collector branch','c14','c27',[pt('c14'),(1160,416),(1160,505),(1428,505),pt('c27')],purple)
wire('Buzzer positive bridge','e23','g23',[pt('e23'),pt('g23')],red)
wire('Buzzer negative bridge','e27','g27',[pt('e27'),pt('g27')],purple)
resistor('a4','a13','R1 470Ω',['#e9ba18','#71358b','#734524','#bf963c'])
resistor('g13','g18','R2 10kΩ',['#734524','#171717','#df8224','#bf963c'])
# Diode cathode at column 23, positive supply.
x1,y=pt('a23');x2,_=pt('a27');path([(x1,y),(x2,y)],'#a6adb4',3);rect(1340,y-13,65,26,'#272d33',5);rect(1347,y-13,8,26,'#d6d9dd');rect(1308,315,128,24,'#f4f3ef',3);text(1372,335,'1N4007',17,anchor='middle',weight='bold')
# TO-92 front elevation at the insertion holes; deliberately identified as front-face drawing.
for n in [12,13,14]:path([(pt('e'+str(n))[0],445),pt('e'+str(n))],'#a6adb4',4)
rect(992,430,88,22,'#34383b',6,'#14171a');rect(992,440,88,12,'#26292c',2);text(1036,444,'PN2222A',12,'#ededee',anchor='middle')
for n,t in [(12,'E'),(13,'B'),(14,'C')]:text(pt('e'+str(n))[0],490,t,14,anchor='middle',weight='bold')
# Buzzer body below its insertion points; explicitly routed external leg bends.
path([pt('f23'),(1288,552),(1288,608),(1333,630)],'#b9bec3',4);path([pt('f27'),(1456,552),(1456,608),(1411,630)],'#b9bec3',4)
circle(1372,654,63,'#252a30','#11161c',3);circle(1372,649,56,'#363c43');circle(1372,638,17,'#12161b');text(1336,654,'+',23,'#eee',anchor='middle');text(1407,654,'−',23,'#eee',anchor='middle');text(1372,780,'5V active buzzer',18,anchor='middle',weight='bold')
add('</svg>');(OUT/'tabletop-wiring.svg').write_text('\n'.join(S),encoding='utf-8')
manifest={'components':{'Q1.E':'e12','Q1.B':'e13','Q1.C':'e14','R1.1':'a4','R1.2':'a13','R2.1':'g13','R2.2':'g18','D1.K':'a23','D1.A':'a27','BZ1.+':'f23','BZ1.-':'f27'},'jumpers':connections,'transistor_view':'flat/text face toward viewer, legs down: E-B-C','terminal_holes':300,'rail_holes':100}
(OUT/'connections.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Wrote SVG and connection manifest')

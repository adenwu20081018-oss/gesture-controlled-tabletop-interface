"""Generate documentation SVGs. Standard library only; not a KiCad export."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/images'
INK, WIRE, RED, SIGNAL, SWITCH = '#172b3a', '#28724f', '#b53c35', '#007d8a', '#76549a'
parts = []

def text(x, y, value, size=18, color=INK, anchor='start'):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>')

def line(points, color=WIRE, width=2.5, arrow=False):
    tail = ' marker-end="url(#arrow)"' if arrow else ''
    parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="{width}"{tail}/>')

def rect(x,y,w,h,fill='white',stroke=INK):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

def dot(x,y,color=WIRE):
    parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')

def start(title, subtitle, ident, height=760):
    parts.clear()
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0 0 L8 4 L0 8 Z" fill="{INK}"/></marker></defs><g font-family="Arial, sans-serif">')
    rect(0,0,1200,height,'#fff','#fff')
    rect(20,20,1160,height-40)
    text(48,62,title,28)
    text(48,91,subtitle,16)
    line('20,113 1180,113',INK,1)
    line(f'20,{height-75} 1180,{height-75}',INK,1)
    text(48,height-45,'INTERACTIVE PROJECTION GUESS WHO',16)
    text(1152,height-45,ident+'  /  REV B  /  DOCUMENTATION',14,anchor='end')

def save(name):
    (OUT / (name+'.svg')).write_text(''.join(parts)+'</g></svg>\n',encoding='utf-8')

def ground(x,y):
    line(f'{x},{y} {x},{y+12}')
    for n,w in enumerate((32,20,8)):
        line(f'{x-w/2},{y+12+n*6} {x+w/2},{y+12+n*6}')

start('Active buzzer · transistor driver','WORKING CIRCUIT — USER TESTED','EE-01')
# Reduced interface, not a replica of the board.
rect(65,270,180,235)
text(85,302,'U1 · MEGA 2560',18)
text(85,327,'Board interface only',14)
for y,label in [(350,'5V'),(410,'D8'),(470,'GND')]:
    text(215,y-9,label,16,anchor='end'); line(f'245,{y} 275,{y}')
line('275,350 300,350 300,180 900,180')
text(625,165,'+5V',18,WIRE)
line('275,410 350,410')
rect(350,400,75,20)
text(350,377,'R1  470 Ω',18)
line('425,410 625,410')
dot(490,410)
line('490,410 490,470')
rect(480,470,20,65)
text(365,505,'R2  10 kΩ',18)
line('490,535 490,580 700,580')
line('275,470 300,470 300,580 490,580')
dot(490,580); ground(700,580)
# Conventional NPN symbol; no package pin mapping.
line('625,370 625,450',INK,3)
line('625,390 700,340 700,320',INK)
line('625,430 700,480 700,580',INK)
line('658,452 690,474',INK,2,True)
text(603,395,'B',16)
text(715,343,'C',16)
text(715,495,'E',16)
text(755,407,'Q1  NPN',20)
text(755,436,'PN2222 / 2N2222A family',16)
text(755,464,'E / B / C = electrical functions',15)
text(755,488,'Wiring confirmed by owner',15,RED)
# Buzzer supply and switched return.
line('700,180 700,225')
rect(670,225,60,65)
parts.append('<path d="M730 238 L747 228 L747 287 L730 277" fill="none" stroke="#172b3a" stroke-width="2"/>')
text(645,244,'+',20); text(645,283,'−',20)
text(765,245,'BZ1',18); text(765,270,'Active buzzer',16)
line('700,290 700,320 900,320 900,275')
line('900,180 900,235')
# Diode anode at bottom, cathode bar at top.
line('880,235 920,235',INK,3)
parts.append('<path d="M880 275 L900 235 L920 275 Z" fill="white" stroke="#172b3a" stroke-width="2"/>')
text(927,220,'K · band',16); text(927,294,'A',16)
text(975,253,'D1',18); text(975,279,'1N4007',18)
dot(700,180); dot(700,320)
text(65,624,'Onboard LED: LED_BUILTIN / D13. No external LED circuit.',17)
text(65,654,'Q1 wiring confirmed working by owner. E/B/C denote electrical functions.',15)
save('buzzer-schematic')

start('Mega 2560 · connection schedule','Functional wiring plan — not a breadboard placement or physical transistor pinout','EE-02',820)
rect(55,155,255,295,'#f7f9fa')
text(75,189,'ELEGOO MEGA 2560',20)
text(75,216,'Relevant connections only',16)
for y,label in [(270,'5V'),(330,'D8'),(390,'GND')]:
    text(280,y-12,label,18,anchor='end')
text(75,430,'D13 LED is onboard',16)
line('55,235 35,235 35,510 310,510',INK,2)
text(65,493,'Laptop USB → board USB socket',15)
# Colored net routes with explicit components and endpoint labels.
line('310,270 380,270 380,190 650,190',RED,3)
text(400,176,'+5V',16,RED)
rect(650,160,470,65)
text(675,186,'BZ1 +     /     D1 cathode K (band)',19)
text(675,211,'Red supply net',14,RED)
line('310,330 360,330',SIGNAL,3)
rect(360,318,100,24,'#f3e6ca')
text(360,306,'R1 · 470 Ω',16)
line('460,330 650,330',SIGNAL,3)
rect(650,300,470,65)
text(675,328,'Q1 base B     /     R2 first end',19)
text(675,352,'Teal control net · after R1',14,SIGNAL)
line('310,390 380,390 380,470 650,470',INK,3)
rect(650,440,470,65)
text(675,468,'Q1 emitter E     /     R2 second end',19)
text(675,492,'Common GND · R2 = 10 kΩ from B to E',14)
line('595,580 650,580',SWITCH,3)
rect(650,550,470,65)
text(675,578,'Q1 collector C / BZ1 − / D1 anode A',18)
text(675,602,'Purple switched return · unbanded diode end',14,SWITCH)
text(55,570,'D1 = 1N4007, across the buzzer.',18)
text(55,600,'Follow identified buzzer polarity.',18)
text(55,650,'E / B / C denote circuit functions. Retain the owner-tested transistor wiring pattern.',16)
text(55,681,'WORKING CIRCUIT — USER TESTED',18,RED)
text(55,710,'USB powers the Mega. Disconnect power before changing circuit connections.',15)
save('arduino-wiring')

start('System architecture','Capture → coordinate mapping → game action → physical feedback','SYS-01',650)
def block(x,y,w,title,sub):
    rect(x,y,w,90,'#f7f9fa'); text(x+16,y+34,title,20); text(x+16,y+63,sub,15)
block(55,185,225,'Camera','Laptop webcam / capture')
block(350,185,330,'Python · OpenCV · MediaPipe','Landmarks → homography → pinch')
block(790,185,350,'Java Swing','Hit test → existing button action')
line('280,230 350,230',INK,2,True); text(294,210,'Frames',13)
line('680,218 790,218',INK,2,True); text(696,181,'TCP / JSON',14)
line('790,250 680,250',INK,2,True); text(708,274,'ACK / INFO',13)
block(55,405,270,'Display / HDMI projector','Laptop now · projection planned')
block(435,405,275,'ELEGOO Mega 2560','USB serial · 9600 baud · 8N1')
block(805,405,335,'Onboard D13 LED','Card-action feedback · tested')
line('840,275 840,335 190,335 190,405',INK,2,True)
text(205,324,'Rendered game → laptop graphics / HDMI',15)
line('1040,275 1040,365 570,365 570,405',INK,2,True)
text(580,385,'Commands / responses',15)

# Display and serial are separate logical interfaces branching from the application.
line('710,450 805,450',INK,2,True)
text(55,530,'D8 buzzer circuit: working, user tested. BUZZ remains a standalone command.',16)
text(55,554,'Future WS2812B strip and concept mounting CAD are separate proposals.',16)
save('system-architecture')

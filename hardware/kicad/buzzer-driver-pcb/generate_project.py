"""Rebuild the Phase 9 PCB design with the Python bundled with KiCad 10.

WARNING: overwrites generated native design files. Q1 and BZ1 are placeholders.
The owner confirmed working transistor wiring; PCB package fit remains a separate check.
"""
from pathlib import Path
import json, re, uuid
import pcbnew as p

HERE = Path(__file__).resolve().parent
KICAD = Path(p.__file__).resolve().parents[2] / 'share/kicad'
if not KICAD.exists():
    KICAD = Path('C:/Program Files/KiCad/10.0/share/kicad')
NAME = 'buzzer-driver'
uid = lambda s: str(uuid.uuid5(uuid.NAMESPACE_URL, 'guess-who/phase9/'+s))
mm = p.FromMM
vec = lambda x,y: p.VECTOR2I(mm(x),mm(y))

# PCB pad mapping must match the tested component wiring at assembly.
parts = {
 'J1': ('Connector_Generic:Conn_01x03','MEGA D8 / 5V / GND','Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',105,112,{'1':'D8','2':'+5V','3':'GND'}),
 'R1': ('Device:R','470R','Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',113,110,{'1':'D8','2':'BASE'}),
 'R2': ('Device:R','10k','Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',116,123,{'1':'BASE','2':'GND'}),
 'Q1': ('Transistor_BJT:Q_NPN_BCE','PN2222 / 2N2222A','Package_TO_SOT_THT:TO-92_Inline_Wide',127,116,{'1':'BASE','2':'SWITCHED','3':'GND'}),
 'D1': ('Device:D','1N4007','Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal',136,125,{'1':'+5V','2':'SWITCHED'}),
 'BZ1': ('Device:Buzzer','5V ACTIVE - PLACEHOLDER','Buzzer_Beeper:Buzzer_12x9.5RM7.6',137,111,{'1':'+5V','2':'SWITCHED'}),
}

# Read complete native library symbol S-expressions, preserving library graphics.
def extract(text, marker):
    start=text.index(marker); depth=0; quoted=False; esc=False
    for i in range(start,len(text)):
        ch=text[i]
        if quoted:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"': quoted=False
        elif ch=='"': quoted=True
        elif ch=='(': depth+=1
        elif ch==')':
            depth-=1
            if depth==0: return text[start:i+1]
    raise ValueError(marker)

symbols={}
for symbol,*_ in parts.values():
    lib,name=symbol.split(':')
    symbols[symbol]=extract((KICAD/'symbols'/f'{lib}.kicad_sym').read_text(encoding='utf-8'),f'(symbol "{name}"')

# Schematic: native symbols with short labeled nets. Avoid guessed graphic pin coordinates.
sch=[f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {uid("root")}) (paper "A4")',
 '(title_block (title "Interactive Guess Who - Buzzer Driver") (date "2026-10-31") (rev "1.0") (comment 1 "PCB Design - Fabrication Not Validated") (comment 2 "Working wired circuit; verify PCB footprint fit before fabrication"))',
 '(lib_symbols '+''.join(s.replace(f'(symbol "{key.split(":")[1]}"',f'(symbol "{key}"',1) for key,s in symbols.items())+')']
positions={'J1':(45.72,55.88),'R1':(88.9,55.88),'R2':(88.9,99.06),'Q1':(139.7,76.2),'BZ1':(190.5,50.8),'D1':(190.5,101.6)}
pin_report={}
for ref,(symbol,value,footprint,*_) in parts.items():
    x,y=positions[ref]
    body=symbols[symbol]
    pins=[]
    for match in re.finditer(r'\(pin (?:passive|input|output|bidirectional|power_in|power_out|open_collector|unspecified)\s',body):
        pin=extract(body[match.start():],'(pin ')
        number=re.search(r'\(number "([^"]+)"',pin)[1]
        at=re.search(r'\(at ([\d.-]+) ([\d.-]+) ([\d.-]+)\)',pin)
        pins.append((number,float(at[1]),float(at[2]),int(at[3])))
    pin_report[ref]=pins
    sch.append(f'(symbol (lib_id "{symbol}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {uid(ref)})')
    for prop,val,py,hide in [('Reference',ref,y-10,False),('Value',value,y-7,False),('Footprint',footprint,y,True)]:
        sx = x+23 if ref in ("R1","R2","Q1") and prop != "Footprint" else x
        if ref in ("R1","R2","Q1") and prop != "Footprint": py = y-2 if prop == "Reference" else y+2
        sch.append(f'(property "{prop}" "{val}" (at {sx} {py} 0) (effects (font (size 1.27 1.27))'+(' (hide yes)' if hide else '')+'))')
    for num,*_ in pins: sch.append(f'(pin "{num}" (uuid {uid(ref+num)}))')
    sch.append(f'(instances (project "{NAME}" (path "/{uid("root")}" (reference "{ref}") (unit 1)))))')
    for num,dx,dy,angle in pins:
        px,py=round(x+dx,4),round(y-dy,4)
        # Pin's angle points INTO symbol; extend wire in the opposite direction.
        step={0:(-7.62,0),180:(7.62,0),90:(0,7.62),270:(0,-7.62)}[angle]
        ex,ey=round(px+step[0],4),round(py+step[1],4)
        net=parts[ref][-1][num]
        sch.append(f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0.1524) (type default)) (uuid {uid(ref+num+"wire")}))')
        sch.append(f'(label "{net}" (at {ex} {ey} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uid(ref+num+"label")}))')
for i,t in enumerate([
 'PCB Design - Fabrication Not Validated',
 'J1: 1=D8, 2=+5V, 3=GND. Daughterboard connects by wires; not a Mega shield.',
 'Q1 PCB pads: 1=B, 2=C, 3=E. Match the tested wiring to this footprint before assembly.',
 'BZ1 placeholder: 12 mm body, 7.6 mm pitch, pad 1=positive. Actual part dimensions are unverified.',
 'D1 cathode (pad 1 / band) connects to +5V. No external D13 LED circuit.',
 'Same-name net labels are electrically connected. BUZZ firmware and all application code are unchanged.',
]):
    sch.append(f'(text "{t}" (at 30.48 {139.7+i*5.08} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uid("note"+str(i))}))')
sch.append('(embedded_fonts no))')
(HERE/f'{NAME}.kicad_sch').write_text('\n'.join(sch),encoding='utf-8')

# Native board, through-hole components, 2 copper layers, 1.6 mm FR4 board design.
b=p.BOARD(); b.SetCopperLayerCount(2)
b.GetDesignSettings().SetBoardThickness(mm(1.6))
nets={}
for name in ['D8','+5V','GND','BASE','SWITCHED']:
    net=p.NETINFO_ITEM(b,"/"+name); b.Add(net); nets[name]=net
fps={}
for ref,(_,value,footprint,x,y,mapping) in parts.items():
    lib,name=footprint.split(':')
    fp=p.FootprintLoad(str(KICAD/'footprints'/(lib+'.pretty')),name)
    if fp is None: raise ValueError(footprint)
    fp.SetFPID(p.LIB_ID(lib,name)); fp.SetReference(ref); fp.SetValue(value); fp.SetPosition(vec(x,y))
    path=p.KIID_PATH();path.push_back(p.KIID(uid('root')));path.push_back(p.KIID(uid(ref)));fp.SetPath(path)
    fp.Value().SetVisible(False)
    fp.Reference().SetTextSize(vec(1,1));fp.Reference().SetTextThickness(mm(.15))
    for pad in fp.Pads():pad.SetNet(nets[mapping[pad.GetNumber()]])
    b.Add(fp);fps[ref]=fp

def track(net,points,layer=p.F_Cu,width=.45):
    for a,z in zip(points,points[1:]):
        t=p.PCB_TRACK(b);t.SetStart(vec(*a));t.SetEnd(vec(*z));t.SetWidth(mm(width));t.SetLayer(layer);t.SetNet(nets[net]);b.Add(t)

# No electrical purpose is served by decorative traces. Each route joins real pads.
track('D8',[(105,112),(109,112),(111,110),(113,110)])
track('BASE',[(123.16,110),(125,111.84),(125,114),(127,116)])
track('BASE',[(127,116),(119,116),(116,119),(116,123)],p.B_Cu)
track('+5V',[(105,114.54),(109,114.54),(111,116.54),(111,128),(133,128),(136,125)],width=.65)
track('+5V',[(136,125),(134,123),(134,114),(137,111)],p.B_Cu,.65)
track('SWITCHED',[(144.6,111),(148,114.4),(148,123.16),(146.16,125)],width=.65)
track('SWITCHED',[(146.16,125),(142,120.84),(134.38,120.84),(129.54,116)],width=.65)
# Explicit ground routes plus bottom copper pour, so connectivity is not dependent on a sliver.
track('GND',[(105,117.08),(105,129),(120.16,129),(126.16,123)],p.B_Cu,.65)
track('GND',[(126.16,123),(128,121.16),(132.08,121.16),(132.08,116)],p.B_Cu,.65)

# 54 x 38 mm board with 2 mm chamfered corners.
outline=[(102,100),(152,100),(154,102),(154,136),(152,138),(102,138),(100,136),(100,102),(102,100)]
for a,z in zip(outline,outline[1:]):
    e=p.PCB_SHAPE();e.SetShape(p.SHAPE_T_SEGMENT);e.SetStart(vec(*a));e.SetEnd(vec(*z));e.SetLayer(p.Edge_Cuts);e.SetWidth(mm(.05));b.Add(e)
zone=p.ZONE(b);zone.SetLayer(p.B_Cu);zone.SetNet(nets['GND']);zone.SetLocalClearance(mm(.3));zone.SetThermalReliefGap(mm(.3));zone.SetThermalReliefSpokeWidth(mm(.4))
zone.SetPadConnection(p.ZONE_CONNECTION_THERMAL)
poly=zone.Outline();poly.NewOutline()
for x,y in [(101,101),(153,101),(153,137),(101,137)]:poly.Append(mm(x),mm(y))
b.Add(zone)

def silk(t,x,y,size=1,layer=p.F_SilkS):
    s=p.PCB_TEXT(b);s.SetText(t);s.SetPosition(vec(x,y));s.SetTextSize(vec(size,size));s.SetTextThickness(mm(.15));s.SetLayer(layer)
    if layer==p.B_SilkS:s.SetMirrored(True)
    b.Add(s)
silk('INTERACTIVE GUESS WHO',127,103,1.35)
silk('BUZZER DRIVER',127,132,1.3)
silk('REV 1.0  |  BUZZER DRIVER',127,135, .9)
for label,y in [('D8',112),('5V',114.54),('GND',117.08)]:silk(label,109, y,.8)
silk('1=B  2=C  3=E',129.54,119,.8)
silk('Q1 B / C / E',126,106,.8)
silk('NOT FABRICATION VALIDATED',127,133,.95,p.B_SilkS)
silk('MEGA D8 / 5V / GND',127,105,1,p.B_SilkS)
# Reference text positions chosen separately from default library placement.
for ref,xy in {'J1':(105,108.5),'R1':(118,107.5),'R2':(121,126),'Q1':(129.5,112.5),'BZ1':(141,119.5),'D1':(141,128)}.items():fps[ref].Reference().SetPosition(vec(*xy))
p.SaveBoard(str(HERE/f'{NAME}.kicad_pcb'),b)
project=json.loads((KICAD/'template/kicad.kicad_pro').read_text(encoding='utf-8'))
project['meta']['filename']=NAME+'.kicad_pro'
project['board']['design_settings']['rules']={'min_clearance':.25,'min_track_width':.25,'min_copper_edge_clearance':.5,'min_through_hole_diameter':.3}
project['net_settings']={'meta':{'version':3},'classes':[{'name':'Default','clearance':.25,'track_width':.45,'via_diameter':.8,'via_drill':.4,'diff_pair_width':.25,'diff_pair_gap':.25,'diff_pair_via_gap':.25}]}
(HERE/f'{NAME}.kicad_pro').write_text(json.dumps(project,indent=2)+'\n',encoding='utf-8')
# Project-local library tables: no changes to the user's global library settings.
for kind,libs,ext,var in [('sym',['Connector_Generic','Device','Transistor_BJT'],'kicad_sym','KICAD10_SYMBOL_DIR'),('fp',['Connector_PinHeader_2.54mm','Resistor_THT','Package_TO_SOT_THT','Diode_THT','Buzzer_Beeper'],'pretty','KICAD10_FOOTPRINT_DIR')]:
    lines=[f'({kind}_lib_table (version 7)']
    for lib in libs:lines.append(f'(lib (name "{lib}") (type "KiCad") (uri "${{{var}}}/{lib}.{ext}") (options "") (descr "KiCad standard library"))')
    (HERE/f'{kind}-lib-table').write_text('\n'.join(lines)+')\n',encoding='utf-8')
print('Created native schematic, board, project and local library tables.')
print('Symbol pins:',pin_report)

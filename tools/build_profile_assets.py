"""Render Afan Atif's original profile artwork. Requires Pillow."""
from pathlib import Path
import math, os
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
S = 2
BG = "#0C141C"
PANEL = "#111E28"
TEXT = "#F4F2EB"
MUTED = "#A2B4BD"
LINE = "#293B46"
MINT = "#B1F0C2"
CYAN = "#79CFDF"
GOLD = "#EFC683"
BLUE = "#A5BDF6"

def font(size, bold=False, mono=False):
    names = (["consolab.ttf" if bold else "consola.ttf", "DejaVuSansMono.ttf"] if mono else
             ["segoeuib.ttf" if bold else "segoeui.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"])
    roots = [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts",
             Path("/usr/share/fonts/truetype/dejavu")]
    for root in roots:
        for name in names:
            if (root / name).exists():
                return ImageFont.truetype(str(root / name), int(size * S))
    return ImageFont.load_default(size=int(size*S))

def canvas(w,h):
    im=Image.new("RGB",(w*S,h*S),BG)
    return im,ImageDraw.Draw(im)
def line(d,points,fill=LINE,width=1):
    d.line([(round(x*S),round(y*S)) for x,y in points],fill=fill,width=round(width*S))
def rect(d,box,fill=PANEL,outline=None,radius=12,width=1):
    d.rounded_rectangle(tuple(round(v*S) for v in box),radius=radius*S,fill=fill,outline=outline,width=width*S)
def dot(d,x,y,r=3,fill=MINT,outline=None,width=1):
    d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=fill,outline=outline,width=width*S)
def text(d,pos,value,size=16,fill=TEXT,bold=False,mono=False):
    d.text((pos[0]*S,pos[1]*S),value,font=font(size,bold,mono),fill=fill)
def save(im,name):
    im.resize((im.width//S,im.height//S),Image.Resampling.LANCZOS).save(ASSETS/name)

def network(d,box,color=MINT,phase=0,mode="nodes"):
    x,y,w,h=box
    layers=[[(x+w*.08,y+h*(.22+i*.28)) for i in range(3)],
            [(x+w*.46,y+h*(.12+i*.23)) for i in range(4)],
            [(x+w*.88,y+h*(.28+i*.4)) for i in range(2)]]
    for a,b in zip(layers,layers[1:]):
        for p in a:
            for q in b: line(d,[p,q],fill="#29404A",width=1)
    for layer in layers:
        for px,py in layer:
            dot(d,px,py,5,fill=BG,outline=color)
            dot(d,px,py,2,fill=color)
    for i,(a,b) in enumerate(zip(layers[0],layers[1][:3])):
        t=(phase+i*.31)%1
        px=a[0]+(b[0]-a[0])*t; py=a[1]+(b[1]-a[1])*t
        dot(d,px,py,2.5,fill=color)

# Header: fixed typography and a subtly animated signal diagram.
im,d=canvas(1200,390)
for x in range(18,1200,26):
    for y in range(18,390,26): dot(d,x,y,.7,fill="#1B2A33")
line(d,[(30,28),(1170,28)],width=1)
text(d,(42,43),"AF / PERSONAL ENGINEERING ATLAS",13,MINT,mono=True)
text(d,(942,43),"ISLAMABAD / PK",12,MUTED,mono=True)
text(d,(39,90),"AFAN ATIF.",76,TEXT,bold=True)
text(d,(44,184),"From intelligent models",27,TEXT)
text(d,(44,221),"to connected systems.",27,TEXT)
text(d,(44,278),"AI ENGINEERING   /   AGENTIC SYSTEMS   /   DATA INFRASTRUCTURE",12,MUTED,mono=True)
line(d,[(44,327),(676,327)])
for x,label in [(44,"RESEARCH"),(242,"ENGINEERING"),(469,"DELIVERY")]:
    dot(d,x+4,351,3,fill=MINT)
    text(d,(x+16,341),label,12,TEXT,mono=True)

rect(d,(750,91,1158,332),fill=PANEL,outline=LINE,radius=15)
text(d,(774,108),"THE SYSTEMS LAB",12,MUTED,mono=True)
line(d,[(774,145),(1135,145)])
text(d,(785,280),"INPUT",11,MUTED,mono=True)
text(d,(923,280),"REASON",11,MUTED,mono=True)
text(d,(1060,280),"BUILD",11,MUTED,mono=True)
base=im
frames=[]
for n in range(80):
    f=base.copy(); fd=ImageDraw.Draw(f)
    phase=n/80
    network(fd,(792,159,330,112),MINT,phase)
    for x in [792,927,1098]:
        radius=5+5*(.5+.5*math.sin(phase*math.tau+(x/100)))
        dot(fd,x,306,radius,fill=None,outline="#294C40")
        dot(fd,x,306,2,fill=MINT)
    glowx=44+632*phase
    line(fd,[(glowx-12,327),(glowx+12,327)],fill=MINT,width=2)
    frames.append(f.resize((1200,390),Image.Resampling.LANCZOS))
frames[0].save(ASSETS/"hero.gif",save_all=True,append_images=frames[1:],duration=85,loop=0,optimize=True,disposal=1)
frames[0].save(ASSETS/"hero.png")

projects=[
("aegisdw","01","AEGISDW","Warehouse architecture",MINT,
 ["Deterministic modeling. Validated artifacts.","Human approval at the deployment boundary."],
 "FASTAPI / POSTGRESQL / SNOWFLAKE / DBT","CAPSTONE / ARCHITECTURE","warehouse"),
("maxfuse","02","MAXFUSE","Multimodal security research",CYAN,
 ["Visual + statistical malware representations.","Cross-modal attention and open-set rejection."],
 "PYTORCH / EFFICIENTNET / MC-DROPOUT","EXPLORE THE REPOSITORY","network"),
("seismic","03","SEISMIC ML","Quantitative interpretation",GOLD,
 ["Wavelet features and cascaded ensembles.","From seismic attributes to rock properties."],
 "XGBOOST / LIGHTGBM / CWT / SSWT","EXPLORE THE REPOSITORY","wave"),
("launchmind","04","LAUNCHMIND","Multi-agent orchestration",BLUE,
 ["Five agents. Structured feedback.","Product, engineering and marketing workflows."],
 "PYTHON / GEMINI / REST INTEGRATIONS","EXPLORE THE REPOSITORY","orbit"),
("edhi","05","EDHICONNECT","Distributed emergency coordination",MINT,
 ["Citizen, driver and headquarters portals.","Shared cloud state and transactional dispatch."],
 "FLUTTER / FIREBASE / MAPS","EXPLORE THE REPOSITORY","dispatch"),
("federated","06","FEDERATED ML","Distributed vision + MLOps",CYAN,
 ["Road-object detection across learning nodes.","Containers, deployment and observability."],
 "YOLOV8 / DOCKER / KUBERNETES","EXPLORE THE REPOSITORY","federated"),
]
for key,num,title,subtitle,color,desc,stack,footer,mode in projects:
    im,d=canvas(580,295)
    rect(d,(1,1,579,294),fill=BG,outline=LINE,radius=16)
    text(d,(25,22),num+" / "+subtitle.upper(),11,color,mono=True)
    text(d,(24,54),title,31,TEXT,bold=True)
    if mode=="network": network(d,(437,54,112,66),color,.28)
    elif mode=="wave":
        for i in range(3):
            points=[(426+j,67+i*21+8*math.sin(j/9+i)*math.cos(j/70)) for j in range(127)]
            line(d,points,fill=color if i==1 else LINE,width=1.4)
    elif mode=="warehouse":
        for i in range(3):
            for j in range(2): rect(d,(434+i*34,61+j*30,459+i*34,83+j*30),fill=PANEL,outline=color if i==1 else LINE,radius=3)
    elif mode=="orbit":
        dot(d,490,85,12,fill=PANEL,outline=color,width=2)
        for a in range(5):
            px=490+44*math.cos(a*math.tau/5); py=85+32*math.sin(a*math.tau/5)
            line(d,[(490,85),(px,py)],fill=LINE)
            dot(d,px,py,5,fill=PANEL,outline=color)
    elif mode=="dispatch":
        for i,(px,py) in enumerate([(435,60),(545,60),(490,114)]):
            line(d,[(490,84),(px,py)],fill=LINE)
            dot(d,px,py,7,fill=PANEL,outline=color)
        dot(d,490,84,13,fill=PANEL,outline=color)
        text(d,(480,72),"+",18,color,bold=True)
    else:
        for px,py in [(439,58),(540,58),(490,112)]:
            line(d,[(490,83),(px,py)],fill=LINE)
            rect(d,(px-9,py-8,px+9,py+8),fill=PANEL,outline=color,radius=3)
        dot(d,490,83,10,fill=PANEL,outline=color)
    for i,v in enumerate(desc): text(d,(25,135+i*26),v,17,MUTED)
    text(d,(25,213),stack,10,color,mono=True)
    line(d,[(25,246),(555,246)])
    text(d,(25,262),footer,10,TEXT,mono=True)
    text(d,(542,257),">",17,color,mono=True)
    save(im,key+".png")

# Original contact graphics, kept local with the rest of the artwork.
for key,title,subtitle in [("linkedin","LINKEDIN","LET'S CONNECT"),("email","EMAIL","START A CONVERSATION")]:
    im,d=canvas(235,46)
    rect(d,(1,1,234,45),fill=PANEL,outline=LINE,radius=9)
    text(d,(15,13),title,12,MINT,bold=True,mono=True)
    text(d,(90,15),subtitle,8,MUTED,mono=True)
    save(im,key+".png")

im,d=canvas(1200,110)
line(d,[(20,10),(1180,10)])
text(d,(37,32),"GOOD MODELS DESERVE GOOD SYSTEMS.",22,TEXT,bold=True)
text(d,(38,72),"RESEARCH WITH INTENT. ENGINEERING WITH EVIDENCE.",11,MUTED,mono=True)
dot(d,1140,60,16,fill=PANEL,outline=MINT,width=2)
text(d,(1129,45),"AF",17,MINT,bold=True,mono=True)
save(im,"footer.png")
print("Rendered original header animation, project cards, contact buttons and footer.")
print("Animated header: "+str((ASSETS/"hero.gif").stat().st_size)+" bytes")

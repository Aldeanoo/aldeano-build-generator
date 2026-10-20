from pathlib import Path
import json,urllib.request,sys
ROOT=Path(__file__).resolve().parents[1]
base="https://raw.githubusercontent.com/PrismarineJS/minecraft-data/201ca802a1b2c968b02e7fa5b31dd74e8bff3d8b/data/bedrock/1.26.30/"
mapping=json.load(urllib.request.urlopen(base+"blocksJ2B.json",timeout=30))
states=json.load(urllib.request.urlopen(base+"blockStates.json",timeout=30))
entries={}
def add(alias,name,properties,color,shape="cube"):
    key="minecraft:"+name+"["+",".join(k+"="+str(v) for k,v in sorted(properties.items()))+"]"
    if key not in mapping:raise ValueError(key)
    bed=mapping[key];bedname,body=bed.removeprefix("minecraft:").split("[")
    props={}
    for piece in body[:-1].split(","):
        if piece:
            k,v=piece.split("=")
            props[k]=True if v=="true" else False if v=="false" else int(v) if v.lstrip("-").isdigit() else v
    matched=[s for s in states if s["name"].removeprefix("minecraft:")==bedname and
             {k:v["value"] for k,v in s["states"].items()}==props]
    if not matched:raise ValueError((alias,bed))
    entries[alias]={"java":name,"properties":properties,"bedrock":bedname,"states":props,
                    "color":color,"shape":shape}
for wood,col in [("oak","#96734b"),("dark_oak","#514031")]:
    for axis in "xyz":add(wood+"_log_"+axis,wood+"_log",{"axis":axis},col)
for material,col in [("deepslate_tile","#3d4c58"),("spruce","#765637"),("stone_brick","#96918a")]:
    for facing in ["north","south","east","west"]:
        add(material+"_stairs_"+facing,material+"_stairs",
            {"facing":facing,"half":"bottom","shape":"straight","waterlogged":"false"},col,"stairs")
for material,col in [("spruce","#765637"),("oak","#b8945f"),("stone_brick","#96918a"),("deepslate_tile","#3d4c58")]:
    for half in ["bottom","top"]:
        add(material+"_slab_"+half,material+"_slab",{"type":half,"waterlogged":"false"},col,"slab")
for facing in ["north","south","east","west"]:
    add("spruce_shutter_"+facing,"spruce_trapdoor",
        {"facing":facing,"half":"bottom","open":"true","powered":"false","waterlogged":"false"},
        "#816240","shutter")
for half in ["lower","upper"]:
    add("spruce_door_"+half,"spruce_door",
        {"facing":"north","half":half,"hinge":"left","open":"false","powered":"false"},
        "#785a39","door")
for hang in ["true","false"]:
    add("lantern_hanging" if hang=="true" else "lantern","lantern",
        {"hanging":hang,"waterlogged":"false"},"#edb65a","lantern")
add("oak_leaves","oak_leaves",{"distance":"7","persistent":"true","waterlogged":"false"},"#6f8c48")
add("spruce_post","spruce_fence",{"east":"false","north":"false","south":"false",
    "waterlogged":"false","west":"false"},"#765637","post")
add("grass_block","grass_block",{"snowy":"false"},"#8f9f62")
for name,col,shape in [("moss_block","#778a4e","cube"),("moss_carpet","#778a4e","carpet"),
                       ("coarse_dirt","#81634c","cube"),("dirt_path","#a28d65","path"),
                       ("flowering_azalea","#7c9155","bush"),("poppy","#c35b4e","flower"),
                       ("dandelion","#e3bf58","flower"),("red_carpet","#993f3e","carpet")]:
    add(name,name,{},col,shape)
# Check that Java IDs and properties exist in both supported versions.
for version in ["26.3","1.21.1"]:
    report=json.load(urllib.request.urlopen(f"https://raw.githubusercontent.com/misode/mcmeta/{version}-summary/blocks/data.json",timeout=30))
    for alias,d in entries.items():
        if d["java"] not in report:raise ValueError((version,alias))
sys.path.insert(0,str(ROOT))
import generator as g
if entries != g.DETAILS:
    raise SystemExit("El catalogo integrado no coincide con los datos de referencia.")
if entries != json.loads((ROOT/"catalog/details.json").read_text(encoding="utf-8")):
    raise SystemExit("catalog/details.json no coincide con los datos de referencia.")
print("Estados detallados contrastados:",len(entries))

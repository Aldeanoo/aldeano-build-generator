"""Architectural components and a curated inn. No external dependencies."""
import math
import random
import re

ARCH_SCHEMA = "aldeano-architecture/v1"
FEATURES = {"garden", "balcony", "chimney", "interior", "dormer"}
THEMES = {
    "medieval": {"wall": "white_terracotta", "wood": "oak_planks",
                 "beam": "dark_oak_log", "roof": "deepslate_tile"},
    "forest": {"wall": "white_terracotta", "wood": "spruce_planks",
               "beam": "oak_log", "roof": "spruce"},
    "cerezo": {"wall": "white_concrete", "wood": "cherry_planks",
               "beam": "oak_log", "roof": "deepslate_tile"},
}


class Builder:
    """Reusable components emit ordinary BuildSpec; no hidden NBT logic."""
    def __init__(self, name, size):
        self.spec = {"schema": "aldeano-build/v1", "name": name, "size": size,
                     "palette": {}, "ops": []}

    def fill(self, low, high, material):
        if any(a > b for a, b in zip(low, high)):
            raise ValueError("Componente con extremos invertidos.")
        if any(a < 0 or b >= limit for a, b, limit in zip(low, high, self.spec["size"])):
            raise ValueError(f"Componente fuera de dimensiones: {low} -> {high}")
        self.spec["palette"][material] = material
        if low == high:
            self.spec["ops"].append({"op": "set", "at": list(low), "block": material})
        else:
            self.spec["ops"].append({"op": "fill", "from": list(low),
                                     "to": list(high), "block": material})

    def point(self, x, y, z, material):
        self.fill([x,y,z], [x,y,z], material)

    def room(self, low, high, material):
        self.fill(low, high, material)
        self.fill([n+1 for n in low], [n-1 for n in high], "air")

    def window(self, x, y, z, width=2, facing="north"):
        # A recessed pane, contrasting sill/lintel, separate open shutters.
        axis = 0 if facing in ("north", "south") else 2
        start, end = [x,y,z], [x,y+2,z]
        end[axis] += width-1
        self.fill(start,end,"glass")
        a,b=start.copy(),end.copy()
        a[1]=b[1]=y-1
        a[axis]-=1;b[axis]+=1
        self.fill(a,b,"stone_brick_slab_bottom")
        a[1]=b[1]=y+3
        self.fill(a,b,"spruce_slab_bottom")
        for offset in (-1,width):
            a,b=start.copy(),end.copy()
            a[axis]+=offset;b[axis]=a[axis]
            self.fill(a,b,"spruce_shutter_"+facing)

    def roof(self, x0,x1,z0,z1,y,material,axis="x"):
        low,high=(x0,x1) if axis=="x" else (z0,z1)
        for step in range((high-low)//2+1):
            for side,coordinate in enumerate(sorted({low+step,high-step})):
                if axis=="x":
                    facing="east" if side==0 else "west"
                    self.fill([coordinate,y+step,z0],[coordinate,y+step,z1],
                              material+"_stairs_"+facing)
                else:
                    facing="south" if side==0 else "north"
                    self.fill([x0,y+step,coordinate],[x1,y+step,coordinate],
                              material+"_stairs_"+facing)
        middle=(low+high)//2
        if axis=="x":
            self.fill([middle,y+(high-low)//2+1,z0],[middle,y+(high-low)//2+1,z1],
                      material+"_slab_bottom")
        else:
            self.fill([x0,y+(high-low)//2+1,middle],[x1,y+(high-low)//2+1,middle],
                      material+"_slab_bottom")


def build_architecture(request):
    expected={"schema","name","template","theme","seed","features"}
    if type(request) is not dict or set(request)!=expected or request["schema"]!=ARCH_SCHEMA:
        raise ValueError("Solicitud: schema, name, template, theme, seed y features.")
    if type(request["name"]) is not str or not re.fullmatch(r"[a-z][a-z0-9_]{0,47}",request["name"]):
        raise ValueError("Nombre de proyecto no valido.")
    if request["template"]!="medieval_inn":
        raise ValueError("La plantilla disponible es medieval_inn; otras construcciones usan BuildSpec.")
    if type(request["theme"]) is not str or request["theme"] not in THEMES:
        raise ValueError("Tema: medieval, forest o cerezo.")
    if type(request["seed"]) is not int or not 0<=request["seed"]<=999999:
        raise ValueError("seed: entero entre 0 y 999999.")
    features=request["features"]
    if (type(features) is not list or any(type(f) is not str or f not in FEATURES for f in features)
            or len(features)!=len(set(features))):
        raise ValueError("features: garden, balcony, chimney, interior, dormer, sin repetir.")
    return _inn(request["name"],THEMES[request["theme"]],set(features),request["seed"])


def _inn(name,theme,features,seed):
    b=Builder(name,[31,32,29])
    f,p=b.fill,b.point
    wall,wood,beam,roof=(theme[k] for k in ("wall","wood","beam","roof"))
    rng=random.Random(seed)

    # Site and entry. The clear approach remains independent of optional decoration.
    f([1,0,1],[29,1,27],"mossy_stone_bricks")
    f([1,2,1],[29,2,27],"grass_block")
    f([14,2,0],[18,2,3],"dirt_path")
    f([13,2,2],[19,2,2],"stone_brick_stairs_south")
    f([13,3,3],[19,3,3],"stone_brick_stairs_south")
    f([10,3,4],[22,4,7],"stone_bricks")
    f([10,4,4],[22,4,7],wood)

    # Main mass: a masonry footing and an overhanging timber upper storey.
    b.room([8,3,8],[24,11,23],wall)
    f([8,3,8],[24,4,23],"stone_bricks")
    f([9,4,9],[23,4,22],wood)
    f([9,5,9],[23,11,22],"air")
    f([7,12,7],[25,12,24],wood)
    b.room([7,13,7],[25,18,24],wall)
    f([8,13,8],[24,18,23],"air")
    for z in (8,23):
        for x in (8,13,19,24):
            f([x,5,z],[x,11,z],beam+"_y")
        for y in (5,11):
            f([8,y,z],[24,y,z],beam+"_x")
    for x in (8,24):
        for y in (5,11):
            f([x,y,8],[x,y,23],beam+"_z")
    for z in (7,24):
        for x in (7,13,19,25):
            f([x,13,z],[x,18,z],beam+"_y")
        for y in (12,18):
            f([7,y,z],[25,y,z],beam+"_x")
    for x in (7,25):
        for y in (12,18):
            f([x,y,7],[x,y,24],beam+"_z")
        for z in (12,18):
            f([x,13,z],[x,18,z],beam+"_y")

    # Rhythm of framed windows, sills, lintels and hinged shutters.
    for z,facing in ((8,"north"),(23,"south")):
        for x in (10,21):
            b.window(x,7,z,facing=facing)
    for z,facing in ((7,"north"),(24,"south")):
        for x in (9,15,21):
            b.window(x,14,z,facing=facing)
    for z in (10,20):
        b.window(25,14,z,facing="east")
    for z in (10,19):
        b.window(24,7,z,facing="east")

    # Actual two-part door, generous clear entry, warm suspended lights.
    f([16,5,8],[16,7,8],"air")
    p(16,5,8,"spruce_door_lower");p(16,6,8,"spruce_door_upper")
    p(16,7,8,"glass")
    f([14,9,7],[18,9,7],beam+"_x")
    for x in (14,18):
        p(x,8,7,"lantern_hanging")

    # A proper pitched, overhanging roof with a timber gable and ridge.
    for step in range(9):
        for z in (7,24):
            f([8+step,19+step,z],[24-step,19+step,z],wall)
    b.roof(6,26,5,26,19,roof)
    for z in (6,25):
        f([7,18,z],[25,18,z],beam+"_x")
        for step in range(10):
            for x in sorted({7+step,25-step}):
                p(x,19+step,z,beam+"_y")
        f([16,19,z],[16,28,z],beam+"_y")
        for x in (13,18):
            f([x,21,z],[x+1,23,z],"glass")
        f([12,20,z],[20,20,z],beam+"_x")
        f([12,24,z],[20,24,z],beam+"_x")

    # Secondary wing changes the silhouette and joins the main room internally.
    b.room([2,3,12],[7,9,22],wall)
    f([2,3,12],[7,4,22],"stone_bricks")
    f([3,4,13],[6,4,21],wood)
    for x in (2,7):
        for z in (12,22):
            f([x,5,z],[x,9,z],beam+"_y")
    b.window(4,6,12,facing="north")
    b.roof(1,7,11,23,10,roof,axis="z")
    f([8,5,15],[8,7,16],"air")
    for x in (1,7):
        f([x,9,12],[x,9,22],beam+"_z")

    # Structural stair access to the upper storey.
    for i,z in enumerate(range(12,20)):
        f([9,5+i,z],[10,5+i,z],"spruce_stairs_south")
    f([9,12,16],[10,12,18],"air")

    if "balcony" in features:
        f([10,12,4],[22,12,6],wood)
        for x in (10,22):
            f([x,5,4],[x,11,4],beam+"_y")
        for x in (10,13,19,22):
            p(x,13,4,"spruce_post")
        f([10,14,4],[22,14,4],"spruce_slab_bottom")
        for x in (10,22):
            f([x,14,4],[x,14,6],"spruce_slab_bottom")
        f([16,13,7],[16,14,7],"air")
        p(16,13,7,"spruce_door_lower");p(16,14,7,"spruce_door_upper")
        for x in (11,21):
            p(x,11,6,"lantern_hanging")
    else:
        for x in (11,21):
            f([x,5,5],[x,8,5],beam+"_y")
        f([11,9,5],[21,9,6],"spruce_slab_bottom")

    if "dormer" in features:
        # Side dormer interrupts the roof and gives the attic a framed window.
        b.room([21,23,11],[24,26,16],wall)
        f([22,24,12],[23,25,15],"air")
        f([24,24,13],[24,25,14],"glass")
        for z in (11,16):
            f([24,23,z],[24,26,z],beam+"_y")
        f([24,26,11],[24,26,16],beam+"_z")
        for step in range(2):
            f([24,27+step,12+step],[24,27+step,15-step],wall)
        b.roof(21,25,10,17,26,roof,axis="z")

    if "chimney" in features:
        f([21,14,19],[22,30,20],"bricks")
        for y in (17,23,29):
            f([21,y,19],[22,y,20],"stone_bricks")
        f([20,31,18],[23,31,21],"stone_brick_slab_bottom")

    if "interior" in features:
        for x in (15,21):
            p(x,5,17,"spruce_post")
            f([x-1,6,16],[x+1,6,18],"oak_slab_top")
            for z in (15,19):
                f([x-1,5,z],[x+1,5,z],
                  "spruce_stairs_south" if z==15 else "spruce_stairs_north")
        f([20,5,11],[22,5,13],"oak_planks")
        f([20,6,11],[22,6,13],"spruce_slab_top")
        f([14,5,10],[17,5,13],"red_carpet")
        for x,z in ((11,10),(22,20)):
            p(x,10,z,"lantern_hanging")
            p(x,11,z,"oak_planks")
        # Upper loft seating kept clear of the stairs and balcony door.
        f([20,13,19],[23,13,19],"spruce_stairs_north")
        f([20,13,21],[23,13,21],"oak_slab_bottom")
        f([7,18,20],[25,18,20],beam+"_x")
        p(21,17,20,"lantern_hanging")

    if "garden" in features:
        # Garden beds, flowering hedges, bench, and coherent small trees.
        for x0,x1,z0,z1 in ((2,7,8,9),(25,28,5,8),(25,28,11,13)):
            f([x0,3,z0],[x1,3,z1],"flowering_azalea")
        for x,z in ((8,3),(9,2),(21,2),(22,3),(26,15),(27,18),(5,10),(3,11)):
            p(x,3,z,"poppy" if rng.random()<.5 else "dandelion")
        f([24,3,3],[28,3,3],"spruce_slab_bottom")
        f([24,4,4],[28,4,4],"spruce_shutter_north")
        for cx,cz,h,radius in ((3,4,6,3),(28,25,5,2)):
            f([cx,3,cz],[cx,3+h,cz],"oak_log_y")
            for dy in range(-2,3):
                r=radius-(1 if abs(dy)==2 else 0)
                for dz in range(-r,r+1):
                    reach=max(0,int(math.sqrt(max(0,r*r-dz*dz))))
                    y=3+h+dy
                    f([cx-reach,y,cz+dz],[cx+reach,y,cz+dz],"oak_leaves")
            p(cx,3+h,cz,"oak_log_y")
        for x,z in ((12,2),(27,10),(27,19)):
            p(x,3,z,"spruce_post");p(x,4,z,"lantern")

    return b.spec

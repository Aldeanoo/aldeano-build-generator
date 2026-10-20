"""Synchronize public catalog and schema with the portable runtime."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import generator as g

def expected_catalog():
    return {m:{"java":g.java_state(m)["id"],
               "java_properties":g.java_state(m).get("properties",{}),
               "bedrock":"minecraft:"+v[0],"bedrock_states":v[1],"color":v[2],
               "preview_shape":g.DETAILS.get(m,{}).get("shape","cube")}
            for m,v in g.MATERIALS.items()}

def main():
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");args=p.parse_args()
    path=ROOT/"catalog/canonical.json";catalog=expected_catalog()
    schema_path=ROOT/"schema/aldeano-build-v1.schema.json"
    original=json.loads(schema_path.read_text(encoding="utf-8"))
    schema=json.loads(json.dumps(original))
    schema["properties"]["palette"]["additionalProperties"]["enum"]=list(g.MATERIALS)
    for file,value in [(path,catalog),(schema_path,schema)]:
        if args.check:
            if json.loads(file.read_text(encoding="utf-8"))!=value:
                raise SystemExit(f"{file.name} no coincide con el runtime")
        else:file.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode())
    print("Catalogo y esquema: "+("verificados" if args.check else "actualizados"))
if __name__=="__main__":main()

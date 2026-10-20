"""Rebuild sample exports. --png additionally needs Pillow."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import generator as g

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--png",action="store_true")
    parser.add_argument("--only")
    args=parser.parse_args()
    sources=sorted((ROOT/"examples").glob("*.json"))
    if args.only:sources=[p for p in sources if p.name==args.only]
    if not sources:raise SystemExit("No hay ejemplos que coincidan.")
    for source in sources:
        request=g.parse_build(source.read_text(encoding="utf-8"))
        outputs,report=g.generate(request)
        folder=ROOT/"samples"/report["name"];folder.mkdir(parents=True,exist_ok=True)
        g.write_outputs(outputs,folder,overwrite=True)
        if args.png:
            from render_preview import render
            render(folder/"preview.svg",folder/"preview_3d.png")
        print(json.dumps({"example":source.name,"blocks":report["placed_blocks"],
                          "folder":str(folder)},ensure_ascii=False))
if __name__=="__main__":main()

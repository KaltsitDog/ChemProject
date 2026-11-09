#全项目唯一的路径出口：代码里不再写绝对路径，换机器/换目录只改这一个文件（或设环境变量）
#用法：notebook 里先 sys.path 加上仓库根，再 import config
#仓库根 = 本文件（config.py）所在目录

from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent

#仓库自带的数据：下载仓库就有
DATA_DH = ROOT / "DH" / "data"
DATA_TDT = ROOT / "TDT" / "data"
SOURCE = DATA_TDT / "source"          #两篇原始文献的数据集（数据溯源要用）

#所有产物统一落在 TDT/out/（已写进 .gitignore，不进版本库）
#想指到别处（比如直接输出到桌面）就设环境变量 CHEM_OUT，不用改代码
OUT = Path(os.environ.get("CHEM_OUT") or ROOT / "TDT" / "out")

def ext(env_name, default):
    #仓库之外的大文件不在版本库里：能用环境变量指过去，就不写死绝对路径
    return Path(os.environ.get(env_name) or default)

#3D 几何（parent_XXXX/conf.xyz 的那 1426 个文件夹）与 xTB 程序都不入库
#换机器就设 CHEM_PARENTS / CHEM_XTB / CHEM_XTB_WORK 三个环境变量
XTB = ext("CHEM_XTB", Path.home() / "miniconda3" / "envs" / "xtb" / "Library" / "bin" / "xtb.exe")
XTB_WORK = ext("CHEM_XTB_WORK", ROOT.parent / "xtb_work")
PARENTS = ext("CHEM_PARENTS", XTB_WORK / "Parents")

if __name__ == "__main__":
    #命令行跑一下 python config.py，看这台机器上各路径通不通
    for name in ["ROOT", "DATA_TDT", "SOURCE", "OUT", "PARENTS", "XTB", "XTB_WORK"]:
        p = globals()[name]
        print(f"{name:<9} 存在={str(p.exists()):<5} {p}")
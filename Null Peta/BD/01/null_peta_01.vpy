import vapoursynth as vs
import fvsfunc as fvf
import lvsfunc as lvf
import kagefunc as kgf
import vardefunc as vrf
import placebo
from NRDB import NRDB
from edi_rpow2 import znedi3_rpow2
from vsutil import depth, get_y, get_w, split, join, iterate
core = vs.core

fsrcnnx_path = "C:/Users/noel/Fansubbing/Encoding/FSRCNNX_x2_56-16-4-1.glsl"

src_path = "B:/raws/NULL_AND_PETA/BDMV/STREAM/00005.m2ts"
tv_path = "B:/raws/NULL_AND_PETA/[HorribleSubs] Null Peta - 01 [1080p].mkv"

op_start = 6330
op_end = op_start + 1485

src = depth(core.lsmas.LWLibavSource(src_path), 16)
src = src[24:-48]

# fix bd error on one scene
tv = depth(core.lsmas.LWLibavSource(tv_path), 16)
tv = tv.resize.Spline36(range_in_s="limited", range_s="full")
fix = fvf.rfs(src, tv, mappings='[427 521]')

# Descale
h = 864
kernel = 'bicubic'
b, c = 0, 1/2
luma = get_y(fix)

descaled = fvf.Resize(depth(luma, 32), get_w(h), h, kernel=kernel, a1=b, a2=c)
fsrcnnx = placebo.shader(descaled, descaled.width * 2, descaled.height * 2, fsrcnnx_path)
znedi = depth(znedi3_rpow2(descaled, 2), 16)
merge = core.std.Merge(fsrcnnx, znedi, 0.75)
rescaled = merge.resize.Spline36(1920, 1080)

mask = vrf.diff_rescale_mask(luma, h, kernel, b, c, 60)
merge = core.std.MaskedMerge(rescaled, luma, mask)
merge = core.std.ShufflePlanes([merge, fix], [0, 1, 2], vs.YUV)

# Edge cleaning

edgefix = core.edgefixer.Continuity(merge, left=2, top=2, right=2, bottom=2)

# Debanding

deband = NRDB(edgefix, deband="core.neo_f3kdb.Deband(clip={clip}, range=16, y=32, cb=24, cr=24, grainy=0, grainc=0)")

out = deband
depth(out, 10).set_output()

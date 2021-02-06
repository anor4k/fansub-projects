import vapoursynth as vs
import fvsfunc as fvf
import lvsfunc as lvf
import kagefunc as kgf
import vardefunc as vrf
import placebo
from cooldegrain import CoolDegrain
from NRDB import NRDB
from edi_rpow2 import znedi3_rpow2
from vsutil import depth, get_y, get_w, split, join
from acsuite import eztrim

core = vs.core

fsrcnnx_path = "C:/Users/noel/Fansubbing/Encoding/FSRCNNX_x2_56-16-4-1.glsl"

src_path = "B:/raws/NULL_AND_PETA/BDMV/STREAM/00005.m2ts"
tv_path = "B:/raws/NULL_AND_PETA/[HorribleSubs] Null Peta - 01 [1080p].mkv"

op_start = 6330
native_1080 = [(op_start+483, op_start+680), (op_start+822, op_start+1086)]

src = core.lsmas.LWLibavSource(src_path)
trim = depth(src[24:-48], 16)

# Audio
out_path = __file__.replace('.vpy', '') + '_audio.wav'
# eztrim(src, (24, -48), src_path, out_path)

# fix bd error on one scene
tv = depth(core.lsmas.LWLibavSource(tv_path), 16)
tv = tv.resize.Spline36(range_in_s="limited", range_s="full")
fix = lvf.rfs(trim, tv, mappings=[(427, 521)])

# Edge cleaning
edgefix = core.edgefixer.Continuity(fix, left=2, top=2, right=2, bottom=2)

# Descale
h = 864
kernel = 'bicubic'
b, c = 0, 1/2
y, u, v = split(edgefix)

descaled = fvf.Resize(depth(y, 32), get_w(h), h, kernel=kernel, a1=b, a2=c)
fsrcnnx = placebo.shader(descaled, descaled.width * 2, descaled.height * 2, fsrcnnx_path)
znedi = depth(znedi3_rpow2(descaled, 2), 16)
merge = core.std.Merge(fsrcnnx, znedi, 0.75)
rescaled = merge.resize.Spline36(1920, 1080)

mask = vrf.diff_rescale_mask(y, h, kernel, b, c, 60)
merge = core.std.MaskedMerge(rescaled, y, mask)
merge = join([merge, u, v])

# Replace native 1080p scenes
replace = lvf.rfs(merge, edgefix, mappings=native_1080)

# Denoise
denoise = CoolDegrain(replace, tr=2, thsad=64)

# Debanding
deband = NRDB(denoise, deband="core.neo_f3kdb.Deband(clip={clip}, range=16, y=32, cb=24, cr=24, grainy=0, grainc=0)")

# Grain
grain = kgf.adaptive_grain(deband, strength=0.15, luma_scaling=10)

# Output
out = grain
depth(out, 10).set_output()

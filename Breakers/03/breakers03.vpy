import vapoursynth as vs
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import kagefunc as kgf
from vsbookmark import generate
core = vs.get_core()

src = lvf.src(r'Breakers - 03 (NHKE).ts')
intele = lvf.decomb(src, TFF=True, decimate=True)
trim = intele[796:13739]
deblock = haf.Deblock_QED(trim)

import acsuite
ac = acsuite.AC()
ac.eztrim(intele, (796,13739), r'Breakers - 03 (NHKE).aac', 'Breakers - 03 (NHKE)_trimmed.aac')
#generate(deblock, r'breakers02')

crop = core.std.CropRel(deblock, left="2", right="2")
edge = core.edgefixer.Continuity(crop, 2, 0, 2, 0)

depth = fvf.Depth(edge, 16)
scaled = core.resize.Spline36(depth, 1280, 720)

dering = haf.EdgeCleaner(scaled, strength=4, rmode=13, smode=1)
sharp = haf.LSFmod(dering, defaults="slow", edgemode=1, strength=60, soft=15)
aa = lvf.nneedi3_clamp(sharp)

denoise = mvf.BM3D(aa, sigma=1)
deband = core.f3kdb.Deband(denoise, range=16, y=32, cb=32, cr=32, grainy=24, grainc=0, output_depth=16)
grain = kgf.adaptive_grain(deband, 0.25, luma_scaling=4)

final = src
out = fvf.Depth(final, 10)
out.set_output()
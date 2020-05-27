import vapoursynth as vs 
import lvsfunc as lvf
import havsfunc as haf
import fvsfunc as fvf
import mvsfunc as mvf
import kagefunc as kgf
from vsbookmark import generate
from acsuite import eztrim
core = vs.core
core.max_cache_size = 16000

file = r'Breakers - 16 (NHKE).d2v'
src = core.d2v.Source(file)
intele = lvf.deinterlace.decomb(src, TFF=True, decimate=True)
trim = intele[821:13765]
deblock = fvf.AutoDeblock(trim)

# eztrim(intele, (821,13765), 'Breakers - 16 (NHKE) T110 stereo 255 kbps DELAY -161 ms.aac')
# generate(deblock, r'breakers16')

crop = core.std.CropRel(deblock, left="2", right="2")
edge = core.edgefixer.Continuity(crop, 2, 0, 2, 0)

depth = fvf.Depth(edge, 16)
scaled = core.resize.Bicubic(depth, 1280, 720, filter_param_a=0, filter_param_b=0)

dering = haf.HQDeringmod(scaled, mrad=5, mthr=100, nrmode=2)
sharp = haf.LSFmod(dering, defaults="slow", edgemode=1, strength=40, soft=15)
dehalo = haf.FineDehalo(sharp)
aa = lvf.aa.nneedi3_clamp(dehalo)

denoise = mvf.BM3D(aa, sigma=0.7)
deband = core.neo_f3kdb.Deband(denoise, range=16, y=32, cb=32, cr=32, grainy=0, grainc=0, output_depth=16)
grain = kgf.adaptive_grain(deband, 0.25, luma_scaling=3)

final = grain
out = fvf.Depth(final, 10)
out.set_output()
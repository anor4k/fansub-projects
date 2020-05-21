from vapoursynth import core
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import mvsfunc as mvf
import kagefunc as kgf
from vsbookmark import generate
from acsuite import eztrim
core.max_cache_size = 16000

file = r'Breakers - 14v2 (NHKE).d2v'
src = lvf.src(file)
#intele = lvf.decomb(src, TFF=True, decimate=True)
intele = haf.ivtc_txt60mc(src,4158, tff=True)
trim = intele[808:13728]
deblock = haf.Deblock_QED(trim)

eztrim(intele, (808,13728), 'Breakers - 14v2 (NHKE) T110 stereo 269 kbps DELAY -136 ms.aac')
generate(deblock, r'breakers14')

crop = core.std.CropRel(deblock, left="2", right="2")
edge = core.edgefixer.Continuity(crop, 2, 0, 2, 0)

depth = fvf.Depth(edge, 16)
scaled = core.resize.Spline36(depth, 1280, 720)

dering = haf.HQDeringmod(scaled, mrad=5, mthr=100, nrmode=2)
sharp = haf.LSFmod(dering, defaults="slow", edgemode=1, strength=40, soft=15)
dehalo = haf.FineDehalo(sharp)
aa = lvf.nneedi3_clamp(dehalo)

denoise = mvf.BM3D(aa, sigma=0.7)
deband = core.neo_f3kdb.Deband(denoise, range=16, y=32, cb=32, cr=32, grainy=0, grainc=0, output_depth=16)
grain = kgf.adaptive_grain(deband, 0.25, luma_scaling=3)

final = grain
out = fvf.Depth(final, 10)
out.set_output()
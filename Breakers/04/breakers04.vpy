import vapoursynth as vs
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import mvsfunc as mvf
import kagefunc as kgf
from acsuite import eztrim
from vsbookmark import generate
core = vs.core
core.max_cache_size = 16000

src = lvf.src(r'Breakers - 04 (NHKE).d2v')
intele = lvf.deinterlace.decomb(src, TFF=True, decimate=True)
trim = intele[809:13753]
deblock = fvf.AutoDeblock(trim)

# eztrim(intele, (809,13753), r'Breakers - 04 (NHKE) T110 stereo 252 kbps DELAY -120 ms.aac')
# generate(deblock, r'breakers04')

crop = core.std.CropRel(deblock, left="2", right="2")
edge = core.edgefixer.Continuity(crop, 2, 0, 2, 0)

depth = fvf.Depth(edge, 16)
scaled = core.resize.Bicubic(depth, 1280, 720, filter_param_a=0, filter_param_b=0)

dering = haf.HQDeringmod(scaled, mrad=5, mthr=100, nrmode=2)
sharp = haf.LSFmod(dering, defaults="slow", edgemode=1, strength=40, soft=15)
dehalo = haf.FineDehalo(sharp)
aa = lvf.aa.nneedi3_clamp(dehalo)

denoise = mvf.BM3D(aa, sigma=1)
deband = core.neo_f3kdb.Deband(denoise, range=16, y=32, cb=32, cr=32, grainy=24, grainc=0, output_depth=16)
grain = kgf.adaptive_grain(deband, 0.25, luma_scaling=4)

final = grain
out = fvf.Depth(final, 10)
out.set_output()
import vapoursynth as vs
import fvsfunc as fvf
import kagefunc as kgf
import lvsfunc as lvf
import mvsfunc as mvf
import havsfunc as haf
import vsTAAmbk as taa
import vsutil
from vsbookmark import generate
core = vs.get_core()
core.set_max_cache_size(12600)

flashbacks = "[3257 3286] [3376 3826] [5232 5391] [5833 5975]"

src = lvf.src("original/[Erai-raws] Null Peta - 11 [1080p][Multiple Subtitle]_Video01.UND.h264")
#generate(src, r'null11')
src = fvf.Depth(src, 32)
planes = kgf.split(src)
op_start = 0
op_length = 1485

planes[0] = kgf.inverse_scale(planes[0], width = vsutil.get_w(864), height = 864, kernel = 'bicubic', b=0, c=1,
 mask_detail=True, descale_mask_zones=f"[{op_start} {op_start+op_length}]")
planes[1], planes[2] = [core.resize.Spline36(p, planes[0].width, planes[0].height, format = planes[0].format,src_left=.25) for p in planes [1:]]
scaled = kgf.join(planes)
scaled = fvf.Depth(scaled, 16)

denoised = mvf.BM3D(scaled, sigma=[4,0.5])

aa = lvf.nneedi3_clamp(denoised)
#aa = taa.TAAmbk(denoised)

deband = core.f3kdb.Deband(aa, range=22, y=24, cb=16, cr=16, grainy=24, grainc=0, output_depth=16)

grain = kgf.adaptive_grain(deband, 0.1, luma_scaling=10)

rep = fvf.rfs(grain, scaled, mappings=flashbacks)


out = rep
final = fvf.Depth(out, 10)
final.set_output()

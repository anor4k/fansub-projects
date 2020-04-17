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

src = lvf.src("original/Null Peta - OVA (Steam 1080p).mkv")
#generate(src, r'null1OVA')
src = fvf.Depth(src, 32)
planes = kgf.split(src)
op_start = 0
op_length = 1485

op = lvf.src("original/op_splice.mkv")

planes[0] = kgf.inverse_scale(planes[0], width = vsutil.get_w(864), height = 864, kernel = 'bicubic', b=0, c=1,
 mask_detail=True, descale_mask_zones=f"[4930 5036]")
planes[1], planes[2] = [core.resize.Spline36(p, planes[0].width, planes[0].height, format = planes[0].format,src_left=.25) for p in planes [1:]]
scaled = kgf.join(planes)
scaled = fvf.Depth(scaled, 16)

denoised = mvf.BM3D(scaled, sigma=[4,0.5])

dering = haf.EdgeCleaner(denoised)

aa = lvf.nneedi3_clamp(dering)

deband = core.f3kdb.Deband(aa, range=24, y=26, cb=18, cr=18, grainy=24, grainc=0, output_depth=16)

grain = kgf.adaptive_grain(deband, 0.1, luma_scaling=10)

out = grain
final = fvf.Depth(out, 10)
final = fvf.rfs(final, op, mappings="[{op_start} {op_lentgh}]")
final.set_output()

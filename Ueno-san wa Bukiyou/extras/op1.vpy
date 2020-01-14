import vapoursynth as vs
import kagefunc as kgf
import fvsfunc as fvf
import lvsfunc as lvf
import mvsfunc as mvf
core = vs.core
core.max_cache_size = 8192

src = core.lsmas.LWLibavSource(r'../BDMV Ueno-san wa Bukiyou/Extras/OP1.m2ts')
src = fvf.Depth(src, 16)
Y, U, V = kgf.split(src)

#Descaling
bilinear = kgf.inverse_scale(src, height=720, kernel='bilinear')
scaled = core.resize.Spline36(bilinear, 1280, 720, format=vs.YUV444P16)

denoised = mvf.BM3D(scaled, sigma=[5,0.5])

out = denoised

final = fvf.Depth(out, 10)
final.set_output()

# encoding options - tune animation, crf 15, preset veryslow
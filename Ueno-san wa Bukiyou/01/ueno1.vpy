import vapoursynth as vs
import kagefunc as kgf
import fvsfunc as fvf
import lvsfunc as lvf
import mvsfunc as mvf
import vsTAAmbk as taa
core = vs.core
core.max_cache_size = 8192


title1 = [25,119]
mid_card = [8152, 8271]
title2 = [8297, 8391]
op = [15104,16544] # until end


src = core.lsmas.LWLibavSource(r'../BDMV Ueno-san wa Bukiyou/Ueno-san wa Bukiyou 01.m2ts')
src = fvf.Depth(src, 16)
Y, U, V = kgf.split(src)

#Descaling
bilinear = kgf.inverse_scale(src, height=720, kernel='bilinear')
scaled = core.resize.Spline36(bilinear, 1280, 720, format=vs.YUV444P16)

denoised = mvf.BM3D(scaled, sigma=[5,0.5])

out = denoised

final = fvf.Depth(out, 10)
src.set_output()

# TODO
# mask native 1080p elements from descaling

# encoding options - tune animation, crf 15, preset veryslow
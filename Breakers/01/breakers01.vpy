import vapoursynth as vs
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf
import kagefunc as kgf
core = vs.get_core()

src = lvf.src(r'Breakers - 01 (NHKE 1440x1080 MPEG2 AAC).ts')
intele = lvf.decomb(src, TFF=True, decimate=True)
deblock = haf.Deblock_QED(intele)

crop = core.std.CropRel(deblock, left="2", right="2")
edge = core.edgefixer.Continuity(crop, 2, 0, 2, 0)

depth = fvf.Depth(edge, 16)
scaled = core.resize.Spline36(depth, 1280, 720)

dering = haf.EdgeCleaner(scaled, strength=4, rmode=13, smode=1)
aa = muf.SharpAAMcmod(dering, dark=0.1)

denoise = mvf.BM3D(aa, sigma=1)
deband = core.f3kdb.Deband(denoise, range=16, y=32, cb=32, cr=32, grainy=24, grainc=0, output_depth=16)
grain = kgf.adaptive_grain(deband, 0.25, luma_scaling=4)

final = scaled
out = fvf.Depth(final, 10)
out.set_output()
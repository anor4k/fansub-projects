import vapoursynth as vs
import lvsfunc as lvf
import havsfunc as haf
import kagefunc as kgf
import fvsfunc as fvf
core = vs.get_core()

src = lvf.source(r'Natsunagu! - 01 (MX).ts')
src = src[977:8169]

deint = fvf.JIVTC(src,0)

clip = fvf.Depth(deint, 32)

deint.set_output()
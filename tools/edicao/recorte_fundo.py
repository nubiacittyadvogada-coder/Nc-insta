import sys, subprocess, numpy as np
from PIL import Image, ImageFilter
from ai_edge_litert.interpreter import Interpreter
src, ss, dur, model, out = sys.argv[1:6]
W,H=1080,1920
it=Interpreter(model_path=model); it.allocate_tensors()
ii=it.get_input_details()[0]['index']; oi=it.get_output_details()[0]['index']
dec=subprocess.Popen(['ffmpeg','-v','error','-ss',ss,'-t',dur,'-i',src,'-vf','fps=30,scale=1080:1920','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','gray','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-crf','12','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
prev=None;n=0
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    im=Image.frombuffer('RGB',(W,H),b)
    x=np.asarray(im.resize((256,256),Image.BILINEAR),np.float32)[None]/255.0
    it.set_tensor(ii,x); it.invoke(); o=it.get_tensor(oi)[0]
    e=np.exp(o-o.max(-1,keepdims=True)); p=e/e.sum(-1,keepdims=True) if not np.allclose(o.sum(-1),1,atol=1e-2) else o
    m=1.0-p[...,0]
    mi=Image.fromarray((np.clip(m,0,1)*255).astype(np.uint8)).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(4))
    a=np.asarray(mi,np.float32)/255.0
    a=np.clip((a-0.3)/0.4,0,1)
    if prev is not None: a=0.55*a+0.45*prev
    prev=a
    enc.stdin.write((a*255).astype(np.uint8).tobytes()); n+=1
enc.stdin.close(); enc.wait(); print('frames',n)

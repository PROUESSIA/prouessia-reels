import os, hashlib, numpy as np, soundfile as sf
TTS_DIR='/tmp/claude-0/-home-claude/69796589-8a45-54ad-b7b1-46400a7df585/scratchpad/tts'
_k=[None]; SR=24000
def _kokoro():
    if _k[0] is None:
        from kokoro_onnx import Kokoro
        _k[0]=Kokoro(f'{TTS_DIR}/kokoro-v1.0.onnx',f'{TTS_DIR}/voices-v1.0.bin')
    return _k[0]
_p=[None]
def _pierre():
    if _p[0] is None:
        import sherpa_onnx
        d=TTS_DIR+'/m/vits-piper-fr_FR-upmc-medium'
        v=sherpa_onnx.OfflineTtsVitsModelConfig(model=d+'/fr_FR-upmc-medium.onnx',tokens=d+'/tokens.txt',data_dir=d+'/espeak-ng-data',noise_scale=0.75,noise_scale_w=0.95,length_scale=1.0)
        _p[0]=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=v,num_threads=4)))
    return _p[0]
def _gen_pierre(texte, vitesse):
    g=_pierre().generate(texte,sid=1,speed=vitesse)
    s=np.array(g.samples,dtype=np.float32)
    if g.sample_rate!=SR:
        from scipy.signal import resample_poly
        s=resample_poly(s,SR,g.sample_rate).astype(np.float32)
    return s,SR
def parler(texte, vitesse=0.98):
    if os.environ.get('VOIX')=='pierre': return _parler_p(texte, vitesse)
    return _parler_k(texte, vitesse)
def _parler_p(texte, vitesse):
    cache=f'{TTS_DIR}/cache'; os.makedirs(cache,exist_ok=True)
    f=f'{cache}/p_'+hashlib.md5(f'{texte}|{vitesse}'.encode()).hexdigest()+'.wav'
    if not os.path.exists(f):
        s,sr=_gen_pierre(texte,vitesse); sf.write(f,s,sr)
    s,sr=sf.read(f); s=s.astype(np.float32)
    a=np.abs(s); idx=np.where(a>0.012)[0]
    if len(idx): s=s[max(0,idx[0]-int(.03*sr)):idx[-1]+int(.08*sr)]
    return s/ max(1e-6,np.max(np.abs(s)))*0.8
def _parler_k(texte, vitesse=0.98):
    cache=f'{TTS_DIR}/cache'; os.makedirs(cache,exist_ok=True)
    f=f'{cache}/'+hashlib.md5(f'{texte}|{vitesse}'.encode()).hexdigest()+'.wav'
    if not os.path.exists(f):
        s,sr=_kokoro().create(texte,voice='ff_siwis',speed=vitesse,lang='fr-fr'); sf.write(f,s,sr)
    s,sr=sf.read(f); s=s.astype(np.float32)
    a=np.abs(s); idx=np.where(a>0.012)[0]
    if len(idx): s=s[max(0,idx[0]-int(.03*sr)):idx[-1]+int(.06*sr)]
    return s
# ---- bruitages synthétiques
def thump(rng):
    n=int(.35*SR); t=np.arange(n)/SR
    f=np.interp(t,[0,.25],[110,48]); ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph)*np.exp(-t*14)+rng.normal(0,1,n)*np.exp(-t*60)*.5
    return (s*0.9).astype(np.float32)
def whoosh(rng):
    n=int(.4*SR); t=np.arange(n)/SR; x=rng.normal(0,1,n)
    k=np.hanning(n)**1.5; y=np.convolve(x,np.ones(40)/40,'same')*k
    return (y*0.55).astype(np.float32)
def tic(rng):
    n=int(.12*SR); t=np.arange(n)/SR
    return (rng.normal(0,1,n)*np.exp(-t*70)*.35).astype(np.float32)
def melange(voix, sfx, dur, chemin):
    rng=np.random.default_rng(4)
    out=np.zeros(int((dur+.5)*SR),np.float32)
    def put(t,s,g):
        i=int(t*SR); j=min(len(out),i+len(s))
        if i<len(out): out[i:j]+=s[:j-i]*g
    for t,s in voix: put(t,s,1.0)
    for t,k in sfx:
        put(t,{'thump':thump,'whoosh':whoosh,'tic':tic}[k](rng),0.38 if k!='tic' else 0.5)
    m=np.max(np.abs(out)); out=out/m*0.89 if m>0.89 else out
    sf.write(chemin,out,SR)

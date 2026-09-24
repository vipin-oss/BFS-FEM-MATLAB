"""P12D Part C: baseline-impact of each candidate fit rule, computed ONLY from committed
evidence (pure post-processing; no solver runs).  Data: p4b_5g_to_5i.json, the TXT omega
vector, and the 21-realization bundle."""
import json, math
J = json.load(open("/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.json"))
B = json.load(open("/home/user/repo/paper9/audit/evidence/p4b_b1/repro_realizations_summary.json"))
om_ex = J["5i"]["omega_exact"]; hs = [1/4, 1/8, 1/16, 1/32]
runs = {k: v["omega"] for k, v in B["realizations"].items()}
runs["committed_txt_run1"] = [1.164855406907999,1.164855390212705,1.1648553893826616,1.1648553893287734]

def lsq(hs, errs):
    x=[math.log(h) for h in hs]; y=[math.log(e) for e in errs]; n=len(x)
    xm=sum(x)/n; ym=sum(y)/n; sxx=sum((xi-xm)**2 for xi in x)
    p=sum((xi-xm)*(yi-ym) for xi,yi in zip(x,y))/sxx
    yh=[ym+p*(xi-xm) for xi in x]; dof=n-2
    se=math.sqrt((sum((yi-hi)**2 for yi,hi in zip(y,yh))/dof)/sxx)
    t={1:12.706,2:4.303,3:3.182,4:2.776}.get(dof,1.96)
    return p, p-t*se, p+t*se

def metrics(oms, rule):
    e=[abs(o-om_ex)/om_ex for o in oms]
    idx = [0,1,2] if rule=="fit3" else ([0,1,2,3] if rule=="fit4" else [i for i,x in enumerate(e) if x>1e-14])
    if len(idx)<3: return None
    p, lo, hi = lsq([hs[i] for i in idx], [e[i] for i in idx])
    d = abs(oms[3]-oms[2])/oms[3]
    return dict(nfit=len(idx), slope=p, lo=lo, hi=hi, eps=max(d, e[3]), d16=d, e32=e[3])

print("committed governing JSON   :", json.dumps({k: J["5i"][k] for k in ("slope","CI95","eps_Delta","d16_32")}))
print("TXT run-1 (deployed rule)  :", json.dumps({k: round(v,27) for k,v in metrics(runs["committed_txt_run1"],"deployed").items() if k in ("nfit","slope","lo","hi","eps")}))
print()
hdr = f"{'rule':10s} {'nfit':>10s} {'slope range':>26s} {'CI-lo range':>22s} {'CI-hi range':>22s} {'eps range':>24s}"
print(hdr); print("-"*len(hdr))
table={}
for rule in ("deployed","fit4","fit3"):
    ms=[metrics(o,rule) for o in runs.values()]; ms=[m for m in ms if m]
    nfits=sorted({m["nfit"] for m in ms})
    sl=[m["slope"] for m in ms]; lo=[m["lo"] for m in ms]; hi=[m["hi"] for m in ms]; ep=[m["eps"] for m in ms]
    table[rule]=dict(slope=(min(sl),max(sl)), lo=(min(lo),max(lo)), hi=(min(hi),max(hi)), eps=(min(ep),max(ep)), nfits=nfits, n=len(ms))
    print(f"{rule:10s} {str(nfits):>10s} {min(sl):.6f}..{max(sl):.6f} {min(lo):8.5f}..{max(lo):8.5f} {min(hi):8.5f}..{max(hi):8.5f} {min(ep):.3e}..{max(ep):.3e}")
print()
print("2-dp / quoted-precision re-baseline risk if the governing JSON were regenerated:")
for rule in ("deployed","fit4","fit3"):
    ms=[metrics(o,rule) for o in runs.values()]; ms=[m for m in ms if m]
    sl=[m["slope"] for m in ms]
    n417=sum(1 for v in sl if f"{v:.2f}"=="4.17"); n418=sum(1 for v in sl if f"{v:.2f}"=="4.18")
    n4179=sum(1 for v in sl if f"{v:.4f}"=="4.1739")
    lo=[f"{m['lo']:.2f}" for m in ms]; hi=[f"{m['hi']:.2f}" for m in ms]
    eps=[f"{m['eps']:.2e}" for m in ms]
    from collections import Counter
    print(f"  {rule:9s}: p@2dp {dict(Counter(f'{v:.2f}' for v in sl))} | 4.1739 exact {n4179}/{len(sl)}"
          f" | CI-lo@2dp {dict(sorted(Counter(lo).items()))} | CI-hi@2dp {dict(sorted(Counter(hi).items()))}"
          f" | eps@2sf {dict(sorted(Counter(eps).items()))}")
print()
print("32^2 datum trustworthiness (from committed data):")
e16 = J["5i"]["rel_err"][2]; e32 = J["5i"]["rel_err"][3]
for p_assumed, tag in ((4.0,"p=4 (pure h^4)"), (J["5i"]["slope"],"p=4.1739 (3-pt fitted)")):
    pred = e16 * (0.0625/0.03125)**(-p_assumed)
    print(f"  extrapolating 16^2 err {e16:.3e} to 32^2 with {tag:22s} -> {pred:.3e}; observed (JSON) {e32:.3e}  ratio obs/pred = {e32/pred:.2e}")
print(f"  declared solver tol=1e-12 (on lambda=omega^2) implies omega-level rel. error ~ tol/2 = {1e-12/2:.1e};")
print(f"  observed run-to-run jitter at 32^2 (probes) 1e-13..5e-13  -> consistent with the declared tolerance.")
print()
print("Therefore: the committed 4x4/8x8/16x16 errors are discretization-dominated; the 32^2 datum is")
print("simultaneously (i) below the extrapolated discretization trend and (ii) at/below the solver's own")
print("error bar -> no rule can make it a *discretization* sample; it can only act as a floor datum.")

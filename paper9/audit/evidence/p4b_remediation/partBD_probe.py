"""Part B/D: what would each candidate rule have reported? Pure post-processing on the
21 documented realizations (audit/evidence/p4b_b1) + the two committed runs. No new solves."""
import json, math, statistics
B = json.load(open("/home/user/repo/paper9/audit/evidence/p4b_b1/repro_realizations_summary.json"))
J = json.load(open("/home/user/repo/paper9/verification/suite/p4b_5g_to_5i.json"))
om_ex = J["5i"]["omega_exact"]; hs = [1/n for n in J["5i"]["meshes"]]

def lsq(hs, errs):
    x=[math.log(h) for h in hs]; y=[math.log(e) for e in errs]; n=len(x)
    xm=sum(x)/n; ym=sum(y)/n; sxx=sum((xi-xm)**2 for xi in x)
    sl=sum((xi-xm)*(yi-ym) for xi,yi in zip(x,y))/sxx
    yh=[ym+sl*(xi-xm) for xi in x]; dof=n-2
    se=math.sqrt((sum((yi-hi)**2 for yi,hi in zip(y,yh))/dof)/sxx)
    tc={1:12.706,2:4.303,3:3.182,4:2.776}.get(dof,1.96)
    return sl, se, (sl-tc*se, sl+tc*se), dof

runs = {k: v["omega"] for k, v in B["realizations"].items()}
runs["committed_json_run2"] = J["5i"]["omega"]                      # same as bundle
runs["committed_txt_run1"]  = [1.164855406907999,1.164855390212705,1.1648553893826616,1.1648553893287734]

def rule(oms, name):
    e=[abs(o-om_ex)/om_ex for o in oms]
    if name=="code_1e-14":      use=[(h,x) for h,x in zip(hs,e) if x>1e-14]
    elif name=="comment_10min": mn=min(e); use=[(h,x) for h,x in zip(hs,e) if x>10*mn]
    elif name=="fixed_4_8_16":  use=list(zip(hs[:3], e[:3]))
    elif name=="all_four":      use=list(zip(hs,e))
    if len(use)<3: return float("nan"), float("nan"), (float("nan"),)*2, len(use)
    sl,se,ci,dof = lsq([u[0] for u in use],[u[1] for u in use])
    return sl, se, ci, len(use)

print(f"{'rule':16s} {'nfit(s): 3/4':>14s} {'slope range over 21 realizations':>34s} {'spread':>8s} {'CI width (dof=1)':>18s}")
summary={}
for name in ("code_1e-14","comment_10min","fixed_4_8_16","all_four"):
    sls=[]; nfits=[]
    for k,oms in runs.items():
        s,se,ci,nf=rule(oms,name); sls.append(s); nfits.append(nf)
    ok=[s for s in sls if s==s]
    spread=100*(max(ok)-min(ok))/(sum(ok)/len(ok))
    cif=rule(J["5i"]["omega"],name)[2]
    summary[name]=dict(min=min(ok),max=max(ok),spread_pct=spread,nfit_counts={n:nfits.count(n) for n in set(nfits)},
                       ci_governing=[float(cif[0]),float(cif[1])] if cif[0]==cif[0] else None)
    print(f"{name:16s} {str({n:nfits.count(n) for n in sorted(set(nfits))}):>14s} {min(ok):.6f} .. {max(ok):.6f} ({spread:>5.3f}%) {str([round(c,4) for c in cif]):>18s}")

print()
print("Part D verification — commented rule (10*min_err) applied to the two committed arrays:")
for tag,oms in (("TXT run 1",runs["committed_txt_run1"]),("JSON run 2",runs["committed_json_run2"])):
    s1=rule(oms,"code_1e-14"); s2=rule(oms,"comment_10min")
    print(f"  {tag}: code rule -> slope {s1[0]:.6f} nfit={s1[3]} | commented rule -> slope {s2[0]:.6f} nfit={s2[3]}")
print(f"  (B1 docs claimed 4.1767 / 4.1739 for the commented rule: verified above)")
print()
print("eps_Delta stability across realizations (definition unchanged by any option):")
epss=[max(abs(o[3]-o[2])/o[3], abs(o[3]-om_ex)/om_ex) for o in runs.values()]
print(f"  eps_Delta = {min(epss):.6e} .. {max(epss):.6e}  spread {100*(max(epss)-min(epss))/(sum(epss)/len(epss)):.2f}%  (governing value {J['5i']['eps_Delta']:.6e})")
print()
print("Fit-count sensitivity to the 1e-14 window vs solver variation:")
w=2*1e-14*om_ex
print(f"  inclusion window width (|dW|) = {w:.3e}; observed n=32 call-to-call spread ~ 1e-13..5e-13 (probes) -> window SMALLER than solver jitter")
print()
print(json.dumps(summary, indent=1)[:900])

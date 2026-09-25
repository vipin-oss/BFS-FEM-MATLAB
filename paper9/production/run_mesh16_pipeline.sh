#!/usr/bin/env bash
# P5 mesh-16 repair: post-compute pipeline (runs unattended, logs each stage).
#
# Waits for the running compute pass to produce all 42 checkpoints, then:
#   1. assemble the n = 16 production outputs (raw JSON, table 5, highlights, run log)
#   2. P12B S7 steering sweep at n = 16
#   3. regenerate every figure/table that depends on production numbers
#   4. n = 8 production pass over the same 42 points (mesh-comparison evidence)
#   5. independent verification (assembly equivalence, dense accuracy, extrema, n8 vs n16)
set -u
cd /home/user/repo/paper9 || exit 1
LOG=audit/evidence/p5_mesh16/pipeline.log
CKPT=/home/user/p5_repair/checkpoints
mkdir -p audit/evidence/p5_mesh16
say() { echo "=== $(date -u +%H:%M:%S) $*" | tee -a "$LOG"; }

say "waiting for n = 16 compute (42 checkpoints in $CKPT)"
for i in $(seq 1 720); do
    n=$(ls "$CKPT"/*.json 2>/dev/null | wc -l)
    if [ "$n" -ge 42 ]; then break; fi
    sleep 30
done
n=$(ls "$CKPT"/*.json 2>/dev/null | wc -l)
say "checkpoints present: $n"
if [ "$n" -lt 42 ]; then say "FAILED stage 0: only $n checkpoints"; exit 1; fi
sleep 20

say "stage 1: assemble n = 16"
python3 -u production/run_p5_mesh16_production.py assemble >>"$LOG" 2>&1 || { say "FAILED stage 1"; exit 1; }

say "stage 2: p12b S7 theta sweep at n = 16"
python3 -u production/p12b_s7_theta_sweep_mesh16.py >>"$LOG" 2>&1 || { say "FAILED stage 2"; exit 1; }

say "stage 3: regenerate figures and tables from the n = 16 data"
for f in figures/gen/*.py; do python3 -u "$f" >>"$LOG" 2>&1 || { say "FAILED $f"; exit 1; }; done
for f in tables/gen/*.py; do python3 -u "$f" >>"$LOG" 2>&1 || { say "FAILED $f"; exit 1; }; done

say "stage 4: n = 8 production pass"
python3 -u production/run_p5_mesh16_production.py compute --n-elem 8 --workers 2 \
    --checkpoint-dir /home/user/p5_repair/checkpoints_n8 >>"$LOG" 2>&1 || { say "FAILED stage 4a"; exit 1; }
python3 -u production/run_p5_mesh16_production.py assemble --n-elem 8 \
    --checkpoint-dir /home/user/p5_repair/checkpoints_n8 >>"$LOG" 2>&1 || { say "FAILED stage 4b"; exit 1; }

say "stage 5: verification"
python3 -u verification/suite/verify_p5_mesh16.py --workers 2 >>"$LOG" 2>&1 || { say "FAILED stage 5"; exit 1; }

say "pipeline complete"

# Step-by-Step Run Order — Paper 10

Execute the commands in the following sequence from the root of the extracted package directory:

```bash
# 1. Verify Python and core libraries
python3 --version
python3 -c "import numpy, scipy, matplotlib; print('Core libraries OK')"

# 2. Run unit tests
python3 03_SOURCE_CODE/utilities/test_parameters.py
python3 03_SOURCE_CODE/utilities/test_antiplane.py
python3 03_SOURCE_CODE/utilities/test_coupled10.py

# 3. Run external validation benchmarks
python3 03_SOURCE_CODE/validation/run_benchmarks.py
python3 03_SOURCE_CODE/validation/run_periodic_pilot.py

# 4. Regenerate manuscript figures from frozen production data
python3 03_SOURCE_CODE/production/regenerate_calibrated_figures.py

# 5. (Optional) Run full 36-case parametric production sweep
python3 03_SOURCE_CODE/production/run_phase3b_production.py

# 6. Recompile manuscript PDF
cd 01_MANUSCRIPT && ./compile_manuscript.sh && cd ..
```

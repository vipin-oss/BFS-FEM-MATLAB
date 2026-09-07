# archive/ — historical package snapshots (deliberately NOT committed here)

This repository tracks `*.zip` via Git LFS (.gitattributes), and the
historical packages would be byte-duplicates of content already present
unpacked in this directory tree. They are therefore excluded from the Git
commit. Authoritative fingerprints:

- QC_First_Paper_FINAL_REPRODUCIBLE_PACKAGE_2026-09-06.zip
  SHA-256 b817860569293e4dfec88419068d83b59976e3d875095e698cb13ae0c4244ec2
  (upstream accepted reproducibility package: source of solver/, drivers/,
  tests/, and every byte of results/raw/)
- FINAL_QC_SURFACE_WAVES_PAPER_PACKAGE_2026-09-07.zip
  SHA-256 1c7c55d7672ecf8d9229a44a2b68b0dfe2348e7305042f11a9e87036e8042fe6
  (Task-15 reproducible package: identical content to this directory)
- FINAL_QC_SURFACE_WAVES_RESEARCH_ARCHIVE_2026-09-07.zip
  SHA-256 e6bc9fffe8e6e30efa2635bf7dd26719924ced7ea7c6206272507505de15800f
  (this archive as a single ZIP; equals this tree plus the two ZIPs above)

Integrity of the unpacked content is guaranteed by
manifests/CHECKSUMS.sha256 and results/manifests/RAW_DATA_CHECKSUMS.sha256,
so excluding the ZIP duplicates loses no information.

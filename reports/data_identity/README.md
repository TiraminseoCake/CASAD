# Data identity references (campaign cfval)

`cfval_smd28_swat51_reference_hashes.json` — file SHA256, array shapes/dtypes and array SHA256 (train/test/label) for all 28 SMD
entities (N=38) and SWaT51 (N=51), recorded on ks (legacy execution id server4). js/server8 must verify its copies against this
file before training; entities whose hashes differ are held back. No data is included here, only identifiers.

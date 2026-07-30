# Known limitations

This document makes the boundary between preserved evidence and reproducible
software explicit.

## Environment

- The original testbed VM or container is not included.
- Dependency versions and the P4 tutorials commit are not pinned.
- `Testbed/Makefile` depends on utilities outside this repository.
- No continuous-integration workflow currently compiles the P4 program.

## Analysis

- The MATLAB dataset is preserved, but its internal variable schema is not
  exported alongside it.
- Model-training scripts, random seeds, and exact split indices are absent.
- Reported prediction scores therefore cannot be independently regenerated from
  this checkout alone.

## Data and storage

- The repository stores roughly 1.8 GB of media directly in Git.
- Raw PCAP files may contain network metadata and should be reviewed before reuse.
- Checksums and an immutable data-release DOI have not been published here.

## Provenance and licensing

- Some player pages and Big Buck Bunny media are third-party-derived assets.
  Their upstream versions and licence notices are not recorded in this snapshot.
- No repository-wide software or data licence has been selected.
- Existing tracked `.DS_Store` files are historical noise; `.gitignore` prevents
  new ones but a future cleanup commit should remove the tracked copies.

## Legacy code

- The original `netsingle.py` monitor depends on a missing `constant` module.
- Its request threshold is a simple counter and should not be presented as a
  validated DDoS detection method.
- `HostMonitoring/http_request_monitor.py` provides a safer inspection helper,
  but it does not recreate the complete original experiment controller.

# Reproducibility guide

## Scope

This repository preserves research artifacts from a completed PhD. It is
possible to inspect the topology, P4 program, captures, media, and dataset from a
current checkout. Exact end-to-end reproduction is not yet guaranteed because
the original VM image, dependency versions, experiment automation, and MATLAB
model scripts are not included.

## Artifact chain

| Stage | Preserved artifact | What it establishes |
| --- | --- | --- |
| Video source | `Segments/` | DASH manifest and multiple encoded representations |
| Playback | `DASHIF Reference LocalHost Player/test_web.html` | Browser-side playback fixture |
| Programmable network | `Testbed/` | P4 pipeline, BMv2 table entries, and topology |
| Observation | `HostMonitoring/`, `experiment */` | HTTP request logging and packet captures |
| Training data | `Collected Data (Used for Training and Validation)/matlab.mat` | Consolidated MATLAB dataset |
| Analysis | Thesis, Chapter 5 | Algorithms, validation design, and reported results |

## P4/BMv2 testbed

`Testbed/Makefile` includes `../../utils/Makefile`, which means it was designed
to run from an exercise directory inside the P4 tutorials environment.

Expected components:

- Linux;
- P4_16 compiler (`p4c`);
- BMv2 `simple_switch_grpc`;
- Mininet;
- P4Runtime support; and
- the shared P4 tutorials Makefile utilities.

Suggested orientation workflow:

```bash
git clone https://github.com/p4lang/tutorials.git
cp -R Testbed tutorials/exercises/qoe-testbed
cd tutorials/exercises/qoe-testbed
make run
```

Treat this as a starting point. The repository does not record the historical
P4 tutorials commit, so current syntax or runtime behaviour may differ.

The topology defines five hosts and three switches. Runtime JSON files populate
IPv4 longest-prefix-match forwarding rules and attach switch identifiers to the
in-band network telemetry trace.

## HTTP request monitor

The original `netsingle.py` files are preserved for provenance. They depend on a
missing local `constant` module and maintain counters through text files.

`HostMonitoring/http_request_monitor.py` is a modern, stateless replacement:

```bash
python -m pip install -r requirements.txt
python HostMonitoring/http_request_monitor.py 10.0.1.1 \
  --interface any \
  --output observations.csv
```

External requirement: TShark must be installed and visible on `PATH`. Packet
capture may require administrator/root privileges.

The monitor writes:

- UTC timestamp;
- source and destination IP/port;
- transport protocol;
- HTTP request method and URI, when available; and
- the number of matching requests observed in the trailing 60 seconds.

Its configurable threshold is only a rate warning. It does not classify attacks.

## Data analysis

The preserved `matlab.mat` file should be opened read-only in MATLAB or a
compatible MAT-file reader. See `DATA_DICTIONARY.md` before interpreting fields.

The thesis describes classifiers including fine and medium decision trees, KNN,
bagged trees, SVM variants, and a neural network. Their training scripts and
random seeds are not present in this repository, so the published scores should
be treated as reported results rather than continuously verified benchmarks.

## Recommended path to a reproducible release

1. Recover the original VM image or record exact P4/BMv2/Mininet versions.
2. Export MATLAB variables with names, shapes, units, and a de-identified CSV
   companion.
3. Recover model scripts and record train/test splits and random seeds.
4. Add one automated smoke test for P4 compilation and topology validation.
5. Move large media and captures to a DOI-backed data archive, publish SHA-256
   checksums, and keep a small fixture in Git.
6. Choose explicit software, data, and third-party asset licences.

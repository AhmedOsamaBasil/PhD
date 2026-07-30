# Data dictionary

## Training and validation data

Primary file:
`Collected Data (Used for Training and Validation)/matlab.mat`

The thesis identifies the following generated dataset features. Variable names
and units should be confirmed in MATLAB before quantitative reuse because the
repository does not include an export schema.

| Concept | Meaning | Typical interpretation |
| --- | --- | --- |
| Initial buffer length | Buffered media before playback begins | Time; exact unit not recorded here |
| Live buffer length | Buffer occupancy during playback | Time; exact unit not recorded here |
| Bitrate downloading | Selected/downloaded DASH representation bitrate | Bits per second |
| Dropped frames | Frames not rendered during playback | Count or rate; confirm in source data |
| Latency | End-to-end delay observed during the trial | Time; exact unit not recorded here |
| Round-trip time | Network request/response delay | Time; exact unit not recorded here |
| Video resolution | Active representation dimensions/class | Categorical or pixel dimensions |
| vMOS | Subjective video Mean Opinion Score | Ordinal score from 1 (bad) to 5 (excellent) |

The thesis describes six source videos, 120 processed sequences, H.264 at six
quality levels, and impairments including initial buffering, stalling, switching,
and monitored network behaviour.

## Packet captures

Directories `experiment 1/`, `experiment 2/`, and `experiment 3/` contain
per-interface PCAP files. Filenames follow the approximate pattern:

```text
<switch>-eth<port>_<direction>.pcap
```

Examples:

- `s1-eth2_in.pcap`
- `s3-eth1_out.pcap`

Zero-byte captures are retained because they are part of the original
experimental record. Do not interpret an empty file as proof that an interface
was inactive without checking the topology and capture procedure.

Each experiment directory also contains a `matlab.mat` artifact. The repository
does not currently record a formal mapping between experiment numbers and the
480p, 720p, and 1080p load scenarios described in the thesis; avoid assigning
that mapping without recovering the original laboratory notes.

## DASH media

`Segments/` contains:

- MPD manifests;
- initialization fragments;
- `.m4s` media fragments grouped by representation bitrate; and
- local playback pages.

The directory names encode nominal representation bitrate, for example
`bunny_1174238bps`. These files account for most of the repository size.

## Data handling

- Treat the preserved MAT and PCAP files as immutable source artifacts.
- Record hashes before moving data to another storage system.
- Check captures for IP addresses or other operational metadata before public
  redistribution.
- Keep derived tables and model outputs separate from the originals.

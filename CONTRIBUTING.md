# Contributing

This repository is an archival record of PhD experiments. Contributions that
improve documentation, reproducibility, metadata, or safe inspection of the
artifacts are welcome.

## Preserve provenance

- Do not rewrite raw packet captures, MATLAB data, or DASH media in place.
- Put derived data in a new, clearly named directory and document the command,
  source files, environment, and date used to create it.
- Keep experimental claims traceable to the thesis or a peer-reviewed
  publication.
- Do not commit credentials, participant identifiers, or new personal data.
- Avoid adding large binaries directly to Git. Prefer an immutable research-data
  archive and record its DOI and checksums here.

## Proposing a change

1. Open an issue explaining the artifact and the intended improvement.
2. Keep source changes separate from documentation or bulk-data changes.
3. Include a reproducible validation command where possible.
4. Update `docs/REPRODUCIBILITY.md` when dependencies or commands change.

The repository currently has no declared reuse licence. A contribution does not
change the copyright status of existing artifacts.

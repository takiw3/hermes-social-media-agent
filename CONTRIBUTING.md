# Contributing

Thanks for helping. This profile makes safety claims, so changes are held to what can be tested.

## Before you open a pull request

```bash
python3 -m pip install pyyaml
python3 scripts/validate.py --history
python3 scripts/hyperframes_vendor.py verify
python3 scripts/run_evals.py
python3 tests/test_install.py
python3 tests/test_hyperframes_integration.py
```

The two test suites install the profile into a temporary `HERMES_HOME`. They need the Hermes CLI: set `HERMES_SRC` to a Hermes checkout and `HERMES_PYTHON` to an interpreter with its dependencies, or have `hermes` on your PATH. Without it, Hermes-dependent steps report `not run`.

For a change that touches rendering, the launcher, or the vendored skills, also run the full matrix and commit the results:

```bash
SOCIAL_TEST_BROWSER=/path/to/chrome-headless-shell \
  python3 tests/test_hyperframes_integration.py --toolchain --renders --json docs/test-results/integration.json
python3 tests/test_install.py --json docs/test-results/install.json
```

## Rules

- **Never edit a file under `skills/hyperframes-video/` by hand.** It is generated. Change a rule in `scripts/hyperframes_vendor.py` and rebuild. See `docs/updating-vendored-code.md`.
- **Never edit a file under `vendor/upstream/`.** It is an exact copy.
- **No claim without a test.** If the README or a skill says the profile can do something, a test must show it. A capability that was not rendered and inspected is described as `loaded only` or `not tested`.
- **No platform fact without a source.** Add it to `platform-facts.yaml` with the official URL, the access date, and a status. Read the page yourself.
- **No invented numbers.** Examples and fixtures are synthetic and labeled so. No benchmark, best time, or growth figure.
- **Synthetic fixtures only.** Test media is generated. No real people, accounts, footage, or audience data.
- **Keep the ownership allowlist narrow.** A new owned path needs a reason and a test that updates still preserve user state.
- **Do not invent Hermes or HyperFrames fields, flags, or variables.** Verify against the tagged source and say which tag.
- **Pin everything.** CI actions by full commit SHA. The CLI by lockfile.
- **One promotional link.** The community link lives in one README section and nowhere else.

## Adding a skill

Use the section set every core skill has: when to use, when not to use, inputs, missing information, source handling, procedure, output contract, checks, permission boundaries, failure behavior, templates, and a synthetic example. Start the description with its trigger. `scripts/validate.py` enforces this.

## Versioning

Semantic versioning. Update `CHANGELOG.md` and the version in `distribution.yaml` together.

## License of contributions

Contributions to original work are accepted under the MIT License. Vendored HyperFrames material stays under Apache-2.0.

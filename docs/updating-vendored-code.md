# Updating vendored code

HyperFrames ships several releases a week. The pin does not move by itself, and nothing in CI moves it. An update is a reviewed pull request.

## Steps

1. Check out the new upstream tag and note its commit:

   ```bash
   git clone --depth 1 --branch vX.Y.Z https://github.com/heygen-com/hyperframes.git /tmp/hyperframes
   git -C /tmp/hyperframes rev-parse HEAD
   npm view hyperframes@X.Y.Z dist.integrity
   ```

2. Read the upstream diff between the old and new tags, for `skills/`, `packages/cli/src/commands/`, `plugin.json`, `LICENSE`, and `CREDITS.md`. Look for new commands, new network calls, new environment switches, new bundled assets, and any `NOTICE` file.

3. Update `scripts/hf_vendor_config.py`: tag, commit, npm version, integrity, retrieval date. Adjust the included and excluded skills, withheld files, and asset license records if the tree changed.

4. Regenerate the toolchain lockfile in a scratch folder with the new exact versions, then copy `package.json` and `package-lock.json` into `skills/integrations/social-hyperframes/toolchain/`:

   ```bash
   npm install --package-lock-only --ignore-scripts
   ```

5. Rebuild:

   ```bash
   python3 scripts/hyperframes_vendor.py import --upstream /tmp/hyperframes
   python3 scripts/hyperframes_vendor.py derive
   python3 scripts/hyperframes_vendor.py lock
   python3 scripts/hyperframes_vendor.py verify
   python3 scripts/check_upstream_contract.py
   ```

   `derive` fails loudly when an upstream passage a patch depends on has changed. Fix the patch rule. Do not edit a derived file by hand.

6. Review the diff of `skills/hyperframes-video/`. Every changed line is either upstream's change or a rule's output.

7. Check every new or changed asset for a license. An asset with no identifiable license is added to the withheld list, and the affected workflow is tested or marked limited.

8. Verify the launcher's subcommand allowlist and refusal list against the new CLI's command list. A new command is refused until someone decides otherwise.

9. Run the tests against an installed temporary profile:

   ```bash
   python3 scripts/validate.py
   python3 tests/test_install.py
   python3 tests/test_hyperframes_integration.py --toolchain --renders
   ```

   That reruns skill loading, cross-link, name-collision, self-update, network-reach, and full render tests at the new pin.

10. Update `THIRD_PARTY_NOTICES.md` if licenses or assets changed, the pinned versions in `README.md` and `docs/`, and `CHANGELOG.md`. Bump the profile version.

## The pull request must show

- The upstream diff.
- The local patch changes.
- The new checksums and asset license inventory.
- Test results, with anything not executed marked `not run`.
- The security and secret scan result.

## What CI does

CI verifies the committed vendor copy and derivative. A scheduled job may report that upstream has moved. It never opens a merge, never auto-merges, and never replaces vendored code.

## Updating Hermes

When a new Hermes release ships, rerun `tests/test_install.py` and the integration suite against it before raising or lowering `hermes_requires`. The value in `distribution.yaml` is the earliest version actually tested.

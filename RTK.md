# RTK - Rust Token Killer (Codex Policy)

## Policy

Treat RTK as the default shell surface.

Before every shell command, first check whether RTK has an equivalent wrapper. If it does, use the RTK form instead of the raw command.

Only fall back to a raw command when:
- RTK has no equivalent wrapper
- you are debugging RTK itself
- you explicitly need unfiltered raw output

If you fall back to a raw command, briefly say why.

## Preferred Rewrites

- `git` -> `rtk git`
- `find` -> `rtk find`
- `grep` -> `rtk grep`
- `cat`, `head`, `tail` -> `rtk read`
- `ls` -> `rtk ls`
- `tree` -> `rtk tree`
- `pytest` -> `rtk pytest`
- `npm` -> `rtk npm`
- `npx` -> `rtk npx`
- `pnpm` -> `rtk pnpm`
- `cargo` -> `rtk cargo`
- `docker` -> `rtk docker`
- `kubectl` -> `rtk kubectl`
- `go` -> `rtk go`
- `ruff` -> `rtk ruff`
- `mypy` -> `rtk mypy`
- `tsc` -> `rtk tsc`
- `eslint`, `lint` -> `rtk lint`
- `playwright` -> `rtk playwright`
- `curl` -> `rtk curl`
- `wc` -> `rtk wc`

## Examples

```bash
rtk git status
rtk find . -name '*.ts'
rtk grep "TODO" src
rtk read package.json
rtk pytest -q
rtk npm run build
```

## Exceptions

Use `rtk proxy <cmd>` when you need the raw command behavior but still want RTK tracking.

## Verification

```bash
rtk --version
rtk gain
which rtk
```

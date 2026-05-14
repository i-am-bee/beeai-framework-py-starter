# AMD GPU Setup (ROCm)

This project is configured to run on an AMD RX 9060 XT (gfx1200, RDNA 4) using ROCm 6.4.

## The problem with `uv sync` alone

`beeai-framework[all]` hard-pins `torch==2.7.1` (a CUDA build) for Linux. `uv sync` installs
that version, which reports `cuda: False` on AMD hardware and has no HIP backend.

The pytorch ROCm wheel index also hosts `pytorch-triton-rocm`, a ROCm-specific package that
torch 2.9.1+rocm6.4 depends on. Due to an IPv6 reachability issue with the pytorch CDN from
this machine, `uv`'s dependency resolver cannot fetch metadata from that index during `uv lock`,
so a clean lock-file-based override isn't possible. The working solution is a post-sync install
via `pip` (which uses IPv4 and succeeds).

## Setup

```bash
# 1. Install base dependencies
uv sync

# 2. Replace CUDA torch with ROCm 6.4 build
uv run poe install-amd
```

`poe install-amd` installs `torch==2.9.1+rocm6.4` and `pytorch-triton-rocm==3.5.1` from
`https://download.pytorch.org/whl/rocm6.4`, then prints a confirmation line:

```
ROCm: 6.4.43484-123eb5128 | GPU: True | devices: 1
```

## Running agents

**Do not use `uv run python ...`** after `poe install-amd` — `uv run` re-syncs the environment
from the lock file first, which reverts torch back to the CUDA build.

Use `.venv/bin/python` directly, or pass `--no-sync`:

```bash
# Preferred
.venv/bin/python beeai_framework_starter/agent.py

# Also works
uv run --no-sync python beeai_framework_starter/agent.py
```

## Environment variables

The `.env` file (created from `.env.template`) includes:

```dotenv
ROCR_VISIBLE_DEVICES=0    # select GPU 0 (RX 9060 XT)
HIP_VISIBLE_DEVICES=0     # same, HIP layer
HSA_ENABLE_SDMA=0         # disable async DMA — stability fix for RDNA 3/4
```

`HSA_OVERRIDE_GFX_VERSION` is **not** needed — gfx1200 is natively supported in ROCm 6.4.

## Smoke test

```bash
.venv/bin/python -c "
import torch
print('torch:', torch.__version__)
print('HIP:', torch.version.hip)
print('GPU:', torch.cuda.is_available(), '| devices:', torch.cuda.device_count())
x = torch.tensor([1.0, 2.0, 3.0]).cuda()
print('GPU tensor sum:', x.sum().item())
"
```

Expected output:
```
torch: 2.9.1+rocm6.4
HIP: 6.4.43484-123eb5128
GPU: True | devices: 1
GPU tensor sum: 6.0
```

The `amdgpu.ids: No such file or directory` warning that appears on startup is harmless.

## After `uv sync` (e.g., dependency updates)

Whenever you run `uv sync` or `uv run` without `--no-sync`, torch will be reverted to the CUDA
build. Re-run `poe install-amd` to restore the ROCm version.

## Code interpreter

The `agent_code_interpreter.py` example requires Docker (k3s). AMD GPU passthrough into k3s
containers needs `/dev/kfd` and `/dev/dri` device mounts plus ROCm userspace libraries inside
the container image — this is deferred. All other agent examples work without Docker.

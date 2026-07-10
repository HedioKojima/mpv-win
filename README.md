# MPV Player Win64 Build (x86-64-v3)

## Installation
Grab the All-in-One archive from [releases](../../releases) under the `bleeding_edge-x86-64-v3` tag.  
Extract anywhere and run `mpv.exe`. All configurations go in the `portable_config` subdirectory.

## Build characteristics
- **Bleeding edge only** — all components built from git HEAD (latest commit on default branch)
- **x86-64-v3 only** — optimized for CPUs with AVX2 (most CPUs after 2013)
- **Dynamic linking** — built with MSYS2 gcc + mcfgthread, produces shared `.exe` + `.dll`
- **Manual trigger only** — no scheduled builds, run the workflow by hand from the Actions tab

## Main project site
<https://mpv.io/>

## Configuration
<https://mpv.io/manual/>  
Save your configs in `portable_config/mpv.conf`, key bindings in `portable_config/input.conf`.

## Awesome Links
- [User Scripts](https://github.com/mpv-player/mpv/wiki/User-Scripts)
- [uosc](https://github.com/tomasklaen/uosc) — modern UI
- [thumbfast](https://github.com/po5/thumbfast) — thumbnail generator
- [Anime4K](https://bloc97.github.io/Anime4K/) — anime shaders
- [SSim/Krig](https://gist.github.com/igv) — chroma upscaling
- [FSRCNNX](https://github.com/igv/FSRCNN-TensorFlow/releases) — anime upscaling
- [ACNet](https://github.com/TianZerL/ACNetGLSL/releases) — anime denoising

## How to Compile
1. Fork this repo
2. Run the **toolchain** workflow first (Actions tab → toolchain → Run workflow) — this builds and caches the MSYS2 + mcfgthread toolchain
3. Run the **build** workflow (Actions tab → build → Run workflow) — this builds all 18 components in dependency order, then packages them into `All-in-One-MPV-git-YYYYMMDD.7z`

**NOTICE**  
Don't build on your personal MSYS2 environment unless it's in a sandbox — these scripts will modify your system.

## Components
The FFmpeg and MPV binaries are built with:
- **nvcodec** — Nvidia hardware-accelerated encode/decode
- **lcms2** — ICC profile reading for color management
- **libass / freetype2 / fribidi / harfbuzz** — subtitle rendering
- **luajit** — Lua scripting
- **shaderc / spirv-cross / libplacebo** — D3D11 & Vulkan render context
- **libbluray** — Blu-ray disc playback
- **libwebp** — WebP image encode/decode
- **libjxl / highway / brotli** — JPEG XL image encode/decode

### Removed (compared to upstream nyfair/mpv-win64)
- lame, libogg, libvorbis-aotuv, opus — audio encoders (FFmpeg's native encoders are sufficient)
- vapoursynth — video processing framework
- libdvdcss / libdvdread / libdvdnav — DVD playback
- Latest (stable), universal, x86-64-v4, amd-zen4+ — other build variants
- mpv-stablelib, ffmpeg stable — stable release builds

### Source policy
All component sources use **git HEAD** (latest commit on default branch) from official repositories:
- GitHub: brotli, ffnvcodec, fribidi, harfbuzz, highway, libass, libjxl, libplacebo, libwebp, luajit, shaderc, spirv-cross, vulkan, ffmpeg, mpv, glslang, spirv-headers, spirv-tools
- GitLab (freetype2): official freedesktop.org repo
- VideoLAN (libbluray): official videolan.org repo

The only non-git source is mcfgthread, which is a tarball from gcc-mcf.lhmouse.com (no git repo available).

## Workflows
| Workflow | Purpose | Trigger |
| --- | --- | --- |
| `toolchain.yml` | Build & cache MSYS2 + mcfgthread toolchain | Manual only |
| `build.yml` | Build all 18 components + package All-in-One 7z | Manual only |
| `autoupdate.yml` | Update mcfgthread version + ffmpeg/mpv pre-release labels in PKGBUILDs and workflows | Manual only |
| `ci.yml` | Debug workflow (SSH into runner) | Manual only |

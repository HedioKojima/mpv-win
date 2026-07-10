import json
from urllib import request
import in_place

resp = request.urlopen('https://github.com/nyfair/workflow/raw/master/old.json')
x = json.loads(resp.read().decode('utf-8'))
x = dict(map(lambda p: (p, x['data'][p]['version']), x['data'].keys()))
mingw = x['Mingw-w64'][:x['Mingw-w64'].find('ucrt')+4]

# Update toolchain.yml: mcfgthread cache key + download URL
with in_place.InPlace('.github/workflows/toolchain.yml', newline='') as f:
  for l in f:
    if (i:=l.find('key: mcf_')) > -1:
      l = '%s%s\n' % (l[:i+9], mingw)
    elif (i:=l.find('curl')) > -1:
      l = '%s%s.7z --resolve "gcc-mcf.lhmouse.com:443:204.152.213.15"\n' % (l[:i+71], x['Mingw-w64'])
    f.write(l)

# Update build.yml: only the mcfgthread cache key (download URLs use GitHub API now)
with in_place.InPlace('.github/workflows/build.yml', newline='') as f:
  for l in f:
    if (i:=l.find('key: mcf_')) > -1:
      l = '%s%s\n' % (l[:i+9], mingw)
    f.write(l)

# mcfgthread version (first 8 chars of mingw build id)
pkgs = {'mcfgthread': mingw[:8]}

# ffmpeg and mpv pre-release labels (e.g. 8.2pre, 0.42pre)
# These are derived from the latest stable release version + 1 minor
# Used in PKGBUILD-git pkgver (makepkg needs a pkgver to name the output package)
ffmpeg_git = x['ffmpeg'].split('.')[:2]
mpv_git = x['mpv'].split('.')[:2]
pkgs['ffmpeg'] = '%s.%dpre' % (ffmpeg_git[0], int(ffmpeg_git[1])+1)
pkgs['mpv'] = '%s.%dpre' % (mpv_git[0], int(mpv_git[1])+1)

# Update PKGBUILD-git files for ffmpeg and mpv (only the pkgver line)
# pkgver is used by makepkg to name the output .pkg.tar.zst file
for p in ['ffmpeg', 'mpv']:
  with in_place.InPlace('%s/PKGBUILD-git' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)

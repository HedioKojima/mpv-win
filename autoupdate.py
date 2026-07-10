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

# mcfgthread version (first 8 chars of mingw build id)
pkgs = {'mcfgthread': mingw[:8]}

# ffmpeg and mpv pre-release labels (e.g. 8.2pre, 0.42pre)
# These are derived from the latest stable release version + 1 minor
ffmpeg_git = x['ffmpeg'].split('.')[:2]
mpv_git = x['mpv'].split('.')[:2]
pkgs['ffmpeg'] = '%s.%dpre' % (ffmpeg_git[0], int(ffmpeg_git[1])+1)
pkgs['mpv'] = '%s.%dpre' % (mpv_git[0], int(mpv_git[1])+1)

# Update PKGBUILD-git files for ffmpeg and mpv (only the pkgver line)
for p in ['ffmpeg', 'mpv']:
  with in_place.InPlace('%s/PKGBUILD-git' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)

# Update build.yml: mcfgthread cache key + download URLs for ffmpeg/mpv/mcfgthread
with in_place.InPlace('.github/workflows/build.yml', newline='') as f:
  for l in f:
    if (i:=l.find('key: mcf_')) > -1:
      l = '%s%s\n' % (l[:i+9], mingw)
    elif (i:=l.find('/bleeding_edge')) > -1:
      r = l[i+25:]
      if r.startswith('ffmpeg-git-dev'):
        l = '%sffmpeg-git-dev-%s-1-x86_64.pkg.tar.zst\n' % (l[0:i+25], pkgs['ffmpeg'])
      elif r.startswith('ffmpeg-git'):
        l = '%sffmpeg-git-%s-1-x86_64.pkg.tar.xz\n' % (l[0:i+25], pkgs['ffmpeg'])
      elif r.startswith('mpv-git'):
        l = '%smpv-git-%s-1-x86_64.pkg.tar.xz\n' % (l[0:i+25], pkgs['mpv'])
    elif (i:=l.find('/latest-x86-64-v3')) > -1:
      r = l[i+18:]
      if r.startswith('mcfgthread'):
        l = '%smcfgthread-%s-1-x86_64.pkg.tar.xz\n' % (l[0:i+18], pkgs['mcfgthread'])
    f.write(l)

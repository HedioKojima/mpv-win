import json
from urllib import request
import in_place

resp = request.urlopen('https://github.com/nyfair/workflow/raw/master/old.json')
x = json.loads(resp.read().decode('utf-8'))
x = dict(map(lambda p: (p, x['data'][p]['version']), x['data'].keys()))
mingw = x['Mingw-w64'][:x['Mingw-w64'].find('ucrt')+4]

# Update toolchain.yml
with in_place.InPlace('.github/workflows/toolchain.yml', newline='') as f:
  for l in f:
    if (i:=l.find('key: mcf_')) > -1:
      l = '%s%s\n' % (l[:i+9], mingw)
    elif (i:=l.find('curl')) > -1:
      l = '%s%s.7z --resolve "gcc-mcf.lhmouse.com:443:204.152.213.15"\n' % (l[:i+71], x['Mingw-w64'])
    f.write(l)

pkgs = {}
pkgs['mcfgthread'] = mingw[:8]
pkgs['ffmpeg'] = x['ffmpeg']
pkgs['mpv'] = x['mpv']
for p in ['brotli', 'ffnvcodec', 'freetype2', 'fribidi', 'harfbuzz', 'highway', 'lcms2', 'libass',
          'libbluray', 'libjxl', 'libplacebo', 'libwebp', 'shaderc', 'spirv-cross']:
  pkgs['%s-dev' % p] = x[p]
pkgs['vulkan-dev'] = x['spirv-cross']

# Update build.yml: version numbers in download URLs + cache key
with in_place.InPlace('.github/workflows/build.yml', newline='') as f:
  for l in f:
    if (i:=l.find('key: mcf_')) > -1:
      l = '%s%s\n' % (l[:i+9], mingw)
    elif (i:=l.find('/dev-x86-64-v3/')) > -1:
      r = l.find('-1-x86_64')
      rr = l.rfind('-', i, r)
      p = l[i+15:rr]
      if p in pkgs:
        l = '%s%s-%s%s' % (l[:i+15], p, pkgs[p], l[r:])
    elif (i:=l.find('/bleeding_edge-x86-64-v3/')) > -1:
      r = l.find('-1-x86_64')
      rr = l.rfind('-', i, r)
      p = l[i+25:rr]
      if p.startswith('ffmpeg-git-dev'):
        l = '%sffmpeg-git-dev-%s%s' % (l[0:i+25], pkgs['ffmpeg'].split('.')[0]+'.'+str(int(pkgs['ffmpeg'].split('.')[1])+1)+'pre', l[r:])
      elif p.startswith('ffmpeg-git'):
        l = '%sffmpeg-git-%s%s' % (l[0:i+25], pkgs['ffmpeg'].split('.')[0]+'.'+str(int(pkgs['ffmpeg'].split('.')[1])+1)+'pre', l[r:])
      elif p.startswith('mpv-git'):
        l = '%smpv-git-%s%s' % (l[0:i+25], pkgs['mpv'].split('.')[0]+'.'+str(int(pkgs['mpv'].split('.')[1])+1)+'pre', l[r:])
    elif (i:=l.find('/latest-x86-64-v3/')) > -1:
      r = l.find('-1-x86_64')
      rr = l.rfind('-', i, r)
      p = l[i+18:rr]
      if p == 'mcfgthread':
        l = '%smcfgthread-%s%s' % (l[0:i+18], pkgs['mcfgthread'], l[r:])
      elif p == 'luajit':
        l = '%sluajit-%s%s' % (l[0:i+18], '2.1', l[r:])
    f.write(l)

# Update PKGBUILD-git pkgver for ffmpeg and mpv
ffmpeg_git = pkgs['ffmpeg'].split('.')[:2]
mpv_git = pkgs['mpv'].split('.')[:2]
pkgs_git = {
  'ffmpeg': '%s.%dpre' % (ffmpeg_git[0], int(ffmpeg_git[1])+1),
  'mpv': '%s.%dpre' % (mpv_git[0], int(mpv_git[1])+1)
}
for p in pkgs_git:
  with in_place.InPlace('%s/PKGBUILD-git' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs_git[p]
      f.write(l)

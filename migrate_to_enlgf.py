import os
# Migrate nexus_pages.enlg -> nexus_pages.enlgf
src = r'd:\enlangg\nexus_app\nexus_pages.enlg'
dst = r'd:\enlangg\nexus_app\nexus_pages.enlgf'
if os.path.exists(src) and not os.path.exists(dst):
    os.rename(src, dst)
    print('Renamed nexus_pages.enlg -> nexus_pages.enlgf')
else:
    print('Already migrated or file not found')

# Remove @on directive from all .enlgf files in nexus_app
for f in [dst]:
    if os.path.exists(f):
        c = open(f, encoding='utf-8').read()
        c = c.replace('@on <frontend>', '').replace('@on frontend', '')
        open(f, 'w', encoding='utf-8').write(c)
        print(f'Cleaned: {f}')

# Also clean other apps
for path in [
    r'd:\enlangg\aero_app\aero.enlgf',
]:
    if os.path.exists(path):
        c = open(path, encoding='utf-8').read()
        c = c.replace('@on <frontend>', '').replace('@on frontend', '')
        open(path, 'w', encoding='utf-8').write(c)
        print(f'Cleaned: {path}')

print('Migration complete')

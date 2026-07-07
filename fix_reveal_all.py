import os, re

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['services.html', 'testimonials.html', 'process.html', 'about.html']

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Check if the observer is BEFORE the render calls
    obs_pos = html.find('\n// Scroll reveal\n')
    init_pos = html.find('// ─── INIT ───')
    
    if obs_pos >= 0 and init_pos >= 0 and obs_pos < init_pos:
        # Move observer after init
        counters_pos = html.find('\n// Counters\n', obs_pos)
        if counters_pos < 0:
            counters_pos = html.find('\nfunction animateCounters', obs_pos)
        
        if counters_pos >= 0:
            observer_block = html[obs_pos:counters_pos]
            html = html[:obs_pos] + html[counters_pos:]
            
            # Find end of init section (before </script>)
            script_end = html.find('</script>', init_pos)
            if script_end >= 0:
                insert_point = html.rfind('\n', 0, script_end)
                html = html[:insert_point+1] + observer_block + '\n' + html[insert_point+1:]
                
                with open(path, 'w') as f:
                    f.write(html)
                print(f'✅ {fname} — observer MOVED after init')
            else:
                print(f'❌ {fname} — script end not found')
        else:
            print(f'❌ {fname} — counters not found')
    elif obs_pos >= 0 and init_pos >= 0:
        print(f'✅ {fname} — observer already after init (line {obs_pos} > {init_pos})')
    else:
        print(f'❌ {fname} — observer or init not found')

# Also fix index.html if not already fixed
path = os.path.join(portfolio, 'index.html')
with open(path) as f:
    html = f.read()
obs_pos = html.find('\n// Scroll reveal\n')
init_pos = html.find('// ─── INIT ───')
if obs_pos > init_pos:
    print(f'✅ index.html — confirmed observer after init')
else:
    print(f'❌ index.html — observer before init, needs fixing')

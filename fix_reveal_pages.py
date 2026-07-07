import os

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['services.html', 'testimonials.html', 'process.html', 'about.html']

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    # Find exact observer block: from "// Scroll reveal" to next "// " or "function "
    obs_start = html.find('\n// Scroll reveal\n')
    
    # The observer block ends at the next "// " or "function" or blank-line-separated section
    after_obs = html[obs_start+1:]  # skip the leading \n
    
    # Find the next "// " or "function" or blank-line-followed-by-code
    end_markers = []
    for marker in ['\n\n// ', '\n\nfunction ', '\n\n// Counters']:
        pos = after_obs.find(marker, 80)
        if pos >= 0:
            end_markers.append((pos, marker))
    
    if end_markers:
        end_markers.sort()
        block_end = obs_start + 1 + end_markers[0][0]
        observer_block = html[obs_start+1:block_end]  # skip leading \n
        
        # Remove from current position
        html = html[:obs_start+1] + html[block_end:]
        
        # Insert before </script> (after init)
        script_end = html.find('</script>')
        html = html[:script_end] + '\n' + observer_block + '\n' + html[script_end:]
        
        with open(path, 'w') as f:
            f.write(html)
        print(f'✅ {fname} — observer moved ({len(observer_block)} chars)')
    else:
        print(f'❌ {fname} — block end not found')

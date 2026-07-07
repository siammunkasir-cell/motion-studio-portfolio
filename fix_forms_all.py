import os, re

portfolio = '/data/data/com.termux/files/home/portfolio'
pages = ['index.html', 'services.html', 'testimonials.html', 'process.html', 'about.html']

for fname in pages:
    path = os.path.join(portfolio, fname)
    with open(path) as f:
        html = f.read()
    
    changes = 0
    
    # Fix newsletter form: add action+method+redirect
    if 'id="newsletterForm"' in html:
        nf = html.find('id="newsletterForm"')
        before = html[nf-50:nf]
        if 'action=' not in html[nf:nf+200]:
            # Add action, method, redirect
            html = html[:nf-1] + ' action="https://api.web3forms.com/submit" method="POST" ' + html[nf:]
            changes += 1
        
        # Check if redirect hidden field exists
        redirect_check = html.find('redirect', nf, nf+500)
        if redirect_check < 0:
            # Add redirect hidden input after from_name
            from_name_pos = html.find('from_name', nf, nf+400)
            if from_name_pos >= 0:
                # Find end of this input
                input_end = html.find('>', from_name_pos)
                if input_end >= 0:
                    redirect_input = '\n          <input type="hidden" name="redirect" value="https://motionstudiocreative.surge.sh/#newsletter-success">'
                    html = html[:input_end+1] + redirect_input + html[input_end+1:]
                    changes += 1
    
    # Fix inquiry form: add action+method+redirect (only on index.html)
    if 'id="inquiryForm"' in html:
        nf = html.find('id="inquiryForm"')
        if 'action=' not in html[nf:nf+300]:
            # It should already be fixed from earlier patch
            # Just check redirect
            redirect_check = html.find('redirect', nf, nf+600)
            if redirect_check < 0:
                from_name_pos = html.find('from_name', nf, nf+400)
                if from_name_pos >= 0:
                    input_end = html.find('>', from_name_pos)
                    if input_end >= 0:
                        redirect_input = '\n          <input type="hidden" name="redirect" value="https://motionstudiocreative.surge.sh/#form-success">'
                        html = html[:input_end+1] + redirect_input + html[input_end+1:]
                        changes += 1
    
    if changes > 0:
        with open(path, 'w') as f:
            f.write(html)
        print(f'✅ {fname}: {changes} fix(es) applied')
    else:
        print(f'✅ {fname}: already fixed, no changes needed')

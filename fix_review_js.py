import re

with open('templates/hospital-proposal-review.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_script = '''    function confirmSubmit() {
        const btn = document.getElementById('modal-submit-btn');
        if (btn) {
            btn.innerHTML = '<i data-lucide="loader" class="w-5 h-5 animate-spin"></i> Submitting...';
            btn.disabled = true;
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
        const form = document.getElementById('proposal-submit-form');
        if (form) {
            form.submit();
        }
    }'''

new_script = '''    async function confirmSubmit() {
        const btn = document.getElementById('modal-submit-btn');
        if (btn) {
            btn.innerHTML = '<i data-lucide="loader" class="w-5 h-5 animate-spin"></i> Submitting...';
            btn.disabled = true;
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
        
        try {
            const form = document.getElementById('proposal-submit-form');
            if (!form) return;
            
            const res = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            });
            
            if (res.redirected) {
                window.location.href = res.url;
                return;
            }
            
            let data;
            try {
                data = await res.json();
            } catch(e) {
                // Not JSON, might be an error page HTML
                alert("An unexpected error occurred. Please try again.");
                if (btn) {
                    btn.innerHTML = 'Submit Proposal';
                    btn.disabled = false;
                }
                return;
            }
            
            if (data.status === 'success' && data.redirect_url) {
                window.location.href = data.redirect_url;
            } else if (data.status === 'error') {
                alert("Error: " + data.message);
                if (btn) {
                    btn.innerHTML = 'Submit Proposal';
                    btn.disabled = false;
                }
            } else {
                window.location.reload();
            }
        } catch (e) {
            alert("A network error occurred: " + e.message);
            if (btn) {
                btn.innerHTML = 'Submit Proposal';
                btn.disabled = false;
            }
        }
    }'''

if old_script in content:
    content = content.replace(old_script, new_script)
    with open('templates/hospital-proposal-review.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully")
else:
    print("Could not find old_script")

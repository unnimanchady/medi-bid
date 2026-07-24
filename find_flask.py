import psutil

print("Running Flask/Python processes:")
for p in psutil.process_iter(['pid', 'name', 'cmdline', 'environ', 'cwd', 'exe']):
    try:
        name = p.info['name'].lower() if p.info['name'] else ''
        cmd = p.info['cmdline']
        if cmd and ('python' in name or 'flask' in name or any('flask' in c.lower() for c in cmd)):
            print(f"PID: {p.info['pid']}")
            print(f"CMD: {cmd}")
            print(f"CWD: {p.info['cwd']}")
            print("-" * 40)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

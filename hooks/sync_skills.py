import json, os

cfg = os.environ.get("CLAUDE_CONFIG_DIR", os.path.expanduser("~/.claude"))
data = json.load(open(os.path.join(cfg, "plugins", "installed_plugins.json")))
skills_dir = os.path.join(cfg, "skills")

for entries in data.get("plugins", {}).values():
    if not entries:
        continue
    install_path = entries[0]["installPath"]
    plugin_skills = os.path.join(install_path, "skills")
    if not os.path.isdir(plugin_skills):
        continue
    for skill in os.listdir(plugin_skills):
        src = os.path.join(plugin_skills, skill)
        dst = os.path.join(skills_dir, skill)
        if os.path.islink(dst) and os.readlink(dst) != src:
            os.unlink(dst)
        if not os.path.exists(dst):
            os.symlink(src, dst)

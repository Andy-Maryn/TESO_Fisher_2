from definitions import ROOT_DIR

path = ROOT_DIR / 'doc/requirements.csv'
with open(path, "r", encoding="utf8") as file:
    requirements = file.read()

path = ROOT_DIR / 'README.md'

start = '### 3.2 Тестовая спецификация\n'
end = '___'
with open(path, "r", encoding="utf8") as file:
    readme = file.read()

    star = readme.find(start) + len(start)
    end = readme.find(end, star)
    readme = readme.replace(readme[star:end], requirements)

with open(path, "w", encoding="utf8") as file:
    file.write(readme)

# 读取所有的包
with open('all_packages.txt', 'r') as f:
    all_packages = set(line.split('==')[0] for line in f.readlines())

# 读取自动安装的包
with open('auto_packages.txt', 'r') as f:
    auto_packages = set(line.strip() for line in f.readlines())

# 筛选出手动安装的包
manual_packages = all_packages - auto_packages

# 将手动安装的包写入 requirements.txt
with open('requirements.txt', 'w') as f:
    for package in manual_packages:
        f.write(package + '\n')

print("手动安装的包已写入 requirements.txt")
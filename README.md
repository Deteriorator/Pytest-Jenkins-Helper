# Pytest-Jenkins-Helper

Python 3.10 使用 conda 进行包管理

安装依赖： 

```shell
conda install pyqt
```

安装 nuitka 打包 exe 可执行文件

```shell
pip install nuitka
```

在 GUI 目录执行如下命令

```bash
nuitka --standalone --mingw64 --show-memory --show-progress --nofollow-imports --enable-plugin=pyqt5 --follow-import-to=pyqt5 --windows-icon-from-ico=./static/helper.ico --output-dir=./ ./run.py
```
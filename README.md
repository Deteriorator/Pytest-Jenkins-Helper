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

修改从 ui 文件转换的 py 文件为如下内容

```python
from .QCodeEditor import QCodeEditor
import GUI.res_rc
```

在 run.py 同级目录执行如下命令

```bash
nuitka --standalone --windows-disable-console --mingw64 --show-memory --show-progress --nofollow-imports --enable-plugin=pyqt5 --follow-import-to=GUI --windows-icon-from-ico=./GUI/static/helper.ico --output-dir=./ ./run.py
```

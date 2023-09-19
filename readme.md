<!--
 * @Descripttion: 
 * @version: 0.1
 * @Author: Cheshire
 * @Date: 2023-09-19 03:19:04
 * @LastEditors: Cheshire
 * @LastEditTime: 2023-09-19 03:22:04
-->

主要是套个皮
https://github.com/Diaoxiaozhang/Ximalaya-XM-Decrypt


Nuitka 编译

```powershell
nuitka --mingw --clang --standalone --enable-plugins=pyside6 --include-data-file=xm_encryptor.wasm=xm_encryptor.wasm --include-data-dir=venv\Lib\site-packages\magic\libmagic=libmagic --windows-icon-from-ico=resource/Image/OIP-C.png --windows-disable-consol --output-dir=release XM_GUI.py
```


需要手动修改 magic.py 中关于 dll 的导入逻辑 

添加以下代码 至 186 行：

```python
if not libmagic or not libmagic._name:
    libmagic = ctypes.CDLL(r"./libmagic/libmagic.dll")
```

编译之后手动将 libmagic.dll 文件复制到 libmagic 文件夹

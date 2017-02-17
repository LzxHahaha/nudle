## 工具版本

* VS 2015
* OpenCV 2.4.13
* Boost 1.6.3
* Python 2.7 (64bit)

## 配置

### OpenCV

下载[OpenCV 2.4.13](http://opencv.org/downloads.html)，解压OpenCV到自定路径下，新建一个环境变量，命名为`OPENCV_DIR`，值为刚才的目录

在`PATH`中加入`%OPENCV_DIR%\build\x64\vc12\bin`。

### Boost

下载[Boost 1.6.3](https://sourceforge.net/projects/boost/files/boost-binaries/1.63.0/)，安装到自定路径，将`lib_msvc-14.0`更名为`lib`
新建一个环境变量，命名为`BOOST_DIR`

在`PATH`中加入`%BOOST_DIR%`和`%BOOST_DIR%\lib`

### Python

安装[Anaconda](https://www.continuum.io/downloads)，新建一个环境变量，命名为`ANACONDA_DIR`并加入PATH中

## 编译

用VS打开项目，将方案设为`Release`，平台设为`x64`，运行之后，会在`Saliency/x64`下生成一个`saliency_rc_cut.pyd`，将这个文件复制到`<Anaconda path>\DLLs`下即可

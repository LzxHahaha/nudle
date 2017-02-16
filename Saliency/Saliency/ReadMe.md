## 前置准备

必须
* swig 3.0.12或更高版本
* g++ 6.3.0或更高版本
* OpenCV 2.4.13
可选
* Visual Studio 2015 with Update 3

## 编译为python拓展

首先下载[OpenCV-SWIG](https://github.com/renatoGarcia/opencv-swig)，解压到任意位置

然后执行
```
$ swig -I<OpenCV-SWIG Path>\lib -I<OpenCV path>\build\include -python -c++ Saliency.i
```
会生成一个`Saliency.cxx`和`Saliency.py`

再执行
```
$ # On Windows
$ g++ -shared -fpic Saliency_wrap.cxx $(pkg-config --cflags --libs python2) $(pkg-config --libs opencv) -o _Saliency.so
```

## 运行测试

用VS打开项目，选择Release和x64，将`SaliencyTest`项目中的`main.cpp`里的路径改为自己的路径，然后运行就好

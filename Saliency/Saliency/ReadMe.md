## 前置准备

必须
* swig 3.0.12或更高版本
* g++ 6.3.0或更高版本
* OpenCV 2.4.13
可选
* Visual Studio 2015 with Update 3

## 编译为python拓展

首先下载[OpenCV-SWIG](https://github.com/renatoGarcia/opencv-swig)，解压到任意位置

然后运行
```
$ swig -I<OpenCV-SWIG Path>\lib -I<OpenCV path>\build\include -python -c++ Saliency.i
$ g++ -shared -fpic Saliency_wrap.cxx $(pkg-config --cflags --libs python3) $(pkg-config --libs opencv) -o _Saliency.so
```

例如：
```
$ swig -ID:\swigwin\opencv-swig\lib -ID:\OpenCV\build\include -python -c++ Saliency.i
```

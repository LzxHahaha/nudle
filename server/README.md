## 运行准备

1. 安装`Python 2.7`以及`pip`
    > pip源最好换成国内的
1. 安装配置`OpenCV 2.14.13`
1. 安装配置`MongoDB`，启动服务
1. 安装依赖

    > *NIX下注意权限问题
    
    ```
    $ pip install -r requirements.txt
    ```
    主要依赖的包：

    1. Flask
    1. numpy
    1. scipy
    1. scikit-image

## 运行

先将需要用到的图片库拷到`/static`目录下，目录名为图片库名

### 训练

> 此步骤耗时较长，且占用内存较大（400张图片约450M左右，耗时一个半小时），

> 训练图片数量暂时不能超过440张，否则会导致Python内存不足自杀

```
$ python ./train.py -l [library name]
```

### 导入数据

> 此步骤约2秒处理一张图片

```
$ python ./record_image.py -l [library name]
```

### 运行服务器

运行服务前需要先打开MongoDB的服务

#### 开发环境

```
$ python ./index.py
```

#### 生产环境

**TODO**

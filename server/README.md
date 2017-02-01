## 运行准备

1. 安装`Python 2.7 64bit`以及`pip`

    > pip源最好换成国内的

    > python必须为64位的版本，否则训练时可能会内存不足导致抛异常

1. 安装配置`OpenCV 2.14.13`
1. 安装配置`MongoDB`
1. 安装依赖

    > 最好都装64位的版本，*NIX下注意权限问题
    
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

例如`voc2006`的图片，就放到`/static/voc2006`下

执行前需要启动MongoDB的服务

### 训练

> 此步骤分两步

> 1. 提取SIFT特征时会开多进程，CPU占用可能会到100%，速度较快（8进程下2140张图片需要1~2分钟）
> 1. 进行聚类时内存占用会较大（一张图片大约换算成1M），**十分耗时**

```
$ python ./train.py -l [library name]
```

### 导入数据

> 此步骤约2秒处理一张图片

```
$ python ./record_image.py -l [library name]
```

### 运行服务器

服务器分为开发环境与生产环境，
开发环境在某些情况下容易出现crash的情况，所以只在开发时使用；
生产环境需要进行部署才能使用

#### 开发环境

```
$ python ./index.py
```

#### 生产环境

**TODO**

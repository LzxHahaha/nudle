## 运行条件

* `Saliency`项目完成`saliency_cut.pyd`的编译以及配置
* 前端项目完成`bundle.js`的打包

## 运行

1. 先将需要用到的图片库拷到`/static`目录下，目录名为`lib_图片库名`，
例如`voc2006`的图片，就放到`/static/lib_voc2006`下

2. 执行前需要启动MongoDB的服务

### 训练

训练分为两个步骤

1. 提取SIFT特征时会开多进程，CPU占用可能会到100%，速度较快（8进程下2140张图片需要1~2分钟）
1. 进行聚类时内存占用会较大（一张图片大约换算成1M），大约耗时一小时左右

```
$ python ./train.py -l <library name> -s <step>
```

其中`-l`为图片库名称；
`-s`为训练图片选择的步长，即每隔s张选择一张图片，默认为1，最大为8

### 可视化特征

在完成训练后，执行`python ./visual_demo -v <library name> -i <image path>`
即可查看图片的前景、背景以及各个统计直方图

### 导入数据

> 此步骤约2秒处理一张图片

```
$ python ./record_image.py -l <library name>
```

### 运行服务器

服务器分为开发环境与生产环境，
开发环境在某些情况下容易出现crash的情况，所以只在开发时使用；
生产环境需要进行部署

#### 开发环境

```
$ python ./index.py
```

#### 生产环境

**TODO**

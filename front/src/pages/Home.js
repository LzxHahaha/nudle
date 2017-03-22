import React from 'react';
import FontAwesome from 'react-fontawesome';
import classNames from 'classnames';
import echarts from 'echarts';
import { Link } from 'react-router';

import globalStyles from './site.css';
import styles from './Home.css';

import Modal from '../components/modal';
import Button from '../components/Button';
import ResultImage from '../components/ResultImage';
import TabView from '../components/TabView';

import { HOST } from '../utils/Request';
import { searchUrl, searchUpload, getLibraries, HIST_NAMES } from '../logic/image';

export default class Home extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      modalVisible: false,
      searching: false,
      searchText: '',
      sourceImage: '',
      display: [],
      libraries: [],
      chooseLibrary: null,
      searchTime: 0,
      size: 20
    };

    this.selectedImage = '';
    this.imageReader = new FileReader();
    this.imageReader.onload =  e => {
      this.selectedImage = e.target.result;
      this.forceUpdate();
    };
    this.searchLibrary = '';
    this.currentHistogrom = HIST_NAMES[0];

    this.histograms = null;
    this.chart = null;
    this.imageData = {};
  }

  async componentDidMount() {
    try {
      const libraries = await getLibraries(true);
      this.setState({
        libraries,
        chooseLibrary: libraries[0]
      });
    }
    catch (err) {
      alert(err.message);
    }
  }

  onLibraryChange = e => {
    this.setState({ chooseLibrary: e.target.value });
  };

  onSearchTextChange = (e) => {
    this.setState({ searchText: e.target.value });
  };

  onSearchTextSubmit = e => {
    if ((e.keyCode || e.which) === 13) {
      this.onSearchPress(true);
    }
  };

  onImageChange = (e) => {
    const image = e.target.files[0];
    this.imageReader.readAsDataURL(image);
  };

  onSearchPress = async (isUrl) => {
    const { chooseLibrary, searchText, size } = this.state;

    if (!chooseLibrary) {
      return null;
    }

    this.searchLibrary = chooseLibrary;
    await this.setState({searching: true, display: []});

    let result = null;
    try {
      if (isUrl) {
        this.setState({ sourceImage: searchText });
        result = await searchUrl(searchText, chooseLibrary, size);
      }
      else {
        this.setState({ sourceImage: this.selectedImage });
        result = await searchUpload(this.selectedImage, chooseLibrary, size);
      }

      this.setState({ display: result.list, searchTime: result.search_time }, () => {
        // 更新图片信息
        const { type, height, width } = result;
        this.imageData = { type, height, width };

        // 更新直方图
        this.histograms = result.histograms;
        this.updateChart(this.currentHistogrom);

        // 绘制裁剪图像
        this.updateCutImage(result.rc_mask, height, width);
      });
    }
    catch (err) {
      alert(err.message);
      await this.setState({ sourceImage: '' });
      this.searchLibrary = '';
      this.histograms = null;
      this.imageData = {};
    }
    finally {
      this.setState({ searching: false });
      this.chart.hideLoading();
    }
  };

  onHistChange = (e) => {
    this.currentHistogrom = e.target.value;
    this.updateChart(e.target.value);
  };

  onSizeTextChange = e => {
    const value = parseInt(e.target.value);
    let size = this.state.size;
    if (0 < value && value <= 50) {
      size = value;
    }
    else if (value > 50) {
      size = 50;
    }
    else {
      size = 1;
    }
    this.setState({ size });
  };

  updateChart = (histName) => {
    if (!this.histograms || !this.histograms[histName]) {
      return;
    }

    if (!this.chart) {
      this.chart = echarts.init(document.getElementById('histContainer'));
      window.onresize = this.chart.resize;
    }

    const data = this.histograms[histName];
    this.chart.setOption({
      title: {
        text: histName,
        left: 'center',
        padding: [20, 0, 5, 0]
      },
      xAxis: {
        data: []
      },
      yAxis: {
        splitLine: {show: true}
      },
      animationDurationUpdate: 1000,
      backgroundColor: '#E5E5E5',
      series: [{
        name: histName,
        type: 'bar',
        itemStyle: {
          normal: {
            color: '#3B85F7'
          }
        },
        animationDelay: idx => idx * 10,
        data
      }]
    });
  };

  updateCutImage = (src, height, width) => {
    const cutImage = new Image();
    cutImage.onload = () => {
      this.foregroundCanvas.height = height;
      this.foregroundCanvas.width = width;
      this.backgroundCanvas.height = height;
      this.backgroundCanvas.width = width;
      const fgctx = this.foregroundCanvas.getContext('2d');
      const bgctx = this.backgroundCanvas.getContext('2d');
      fgctx.clearRect(0, 0, width, height);
      bgctx.clearRect(0, 0, width, height);

      // 画上cut，记下数据
      bgctx.drawImage(cutImage, 0, 0);
      const cutData = bgctx.getImageData(0, 0, width, height);

      // 画上原图
      const source = new Image();
      source.src = this.state.sourceImage;
      fgctx.drawImage(source, 0, 0);
      bgctx.drawImage(source, 0, 0);
      const fgData = fgctx.getImageData(0, 0, width, height);
      const bgData = bgctx.getImageData(0, 0, width, height);

      // 计算
      for (let i = 0; i < cutData.data.length; i += 4) {
        if (cutData.data[i] === 255 && cutData.data[i + 1] === 255 && cutData.data[i + 2] === 255) {
          bgData.data[i] = 0;
          bgData.data[i + 1] = 0;
          bgData.data[i + 2] = 0;
          bgData.data[i + 3] = 0;
        }
        else if (cutData.data[i] === 0 && cutData.data[i + 1] === 0 && cutData.data[i + 2] === 0) {
          fgData.data[i] = 0;
          fgData.data[i + 1] = 0;
          fgData.data[i + 2] = 0;
          fgData.data[i + 3] = 0;
        }
      }
      fgctx.putImageData(fgData, 0, 0);
      bgctx.putImageData(bgData, 0, 0);
    };
    cutImage.src = src;
  };

  render() {
    const { libraries, searching, display, searchText, sourceImage, searchTime, size } = this.state;

    return (
      <div className={globalStyles.container}>
        <div className={globalStyles.row}>
          <div className={classNames(styles.logo, (searching || display.length > 0) && styles.logoFold)}>
            <img src={require('../image/nudle.png')} height="80" />
          </div>
          <div className={styles.searchBox}>
            <select onChange={this.onLibraryChange} className={styles.libraryBox}>
              {
                libraries && libraries.map((el, index) => (
                  <option value={el} key={`lib${index}`}>
                    {el.toUpperCase()}
                  </option>
                ))
              }
            </select>
            <div className={styles.searchInputView}>
              <input
                className={styles.searchInput}
                placeholder="输入图片URL"
                onChange={this.onSearchTextChange}
                value={searchText}
                onKeyDown={this.onSearchTextSubmit}
              />
            </div>
            <a className={styles.imageButton} onClick={()=>this.imagePickerModal.show()}>
              <FontAwesome name="cloud-upload" />
            </a>
            <Button
              className={styles.searchButton}
              onClick={()=>this.onSearchPress(true)}
              disabled={libraries.length === 0 || searching || !searchText}
            >
              搜索
            </Button>
          </div>

          {
            searching && (
              <p className={styles.searchingText}>
                搜索中...
              </p>
            )
          }
        </div>

        <div className={globalStyles.row}>
          <TabView
            labels={['搜索结果', '图片详情']}
            style={display.length === 0 ? {display: 'none'} : {}}
          >
            <div>
              {
                (display.length > 0 && !!this.searchLibrary) && (
                  <div>
                    <div className={styles.searchInfo}>
                      搜索用时：{searchTime}秒<br/>
                      搜索算法：Saliency-BoF<br/>
                      显示结果：{display.length}条
                    </div>
                    {
                      display.map((el, index) => {
                        return (
                          <Link target="_blank" to={`/detail?lib=${this.searchLibrary}&name=${el.name}`}>
                            <ResultImage
                              key={`result${index}`}
                              src={`${HOST}static/lib_${this.searchLibrary}/${el.name}`}
                              className={styles.imagePreviewBox}
                              info={`[${index + 1}]\n${el.distance}`}
                              name={el.name}
                            />
                          </Link>
                        );
                      })
                    }
                  </div>
                )
              }
            </div>
            {
              !!sourceImage ? (
                <div>
                  <div className={styles.searchInfo}>
                    图像大小：{this.imageData.height}×{this.imageData.width}px<br/>
                    图像类型：{this.imageData.type}
                  </div>
                  <div className={styles.inputImageView}>
                    <div className={styles.inputHistogramBox} id="histContainer">
                      <p style={{textAlign: 'center', margin: 0}}>生成中...</p>
                    </div>
                    {
                      !!this.histograms && (
                        <select onChange={this.onHistChange} className={styles.histSelector}>
                          {
                            HIST_NAMES.map((el, index) => (
                              <option key={`hist${index}`}>{el}</option>
                            ))
                          }
                        </select>
                      )
                    }
                  </div>
                  <div className={styles.sourceImageContainer}>
                    <img src={sourceImage} />
                    <canvas ref={ref=>this.foregroundCanvas=ref}>
                    </canvas>
                    <canvas ref={ref=>this.backgroundCanvas=ref}>
                    </canvas>
                  </div>
                </div>
              ) : <div></div>
            }
          </TabView>
        </div>

        <div className={styles.settingButton} onClick={()=>this.settingModal.show()}>
          <FontAwesome name="gear" />
        </div>

        <Modal ref={ref=>this.imagePickerModal=ref}>
          <Modal.Header>
            上传图片进行搜索
          </Modal.Header>
          <input
            type="file"
            accept=".png, .jpg, .jpeg"
            onChange={this.onImageChange}
          />
          <Modal.Footer>
            <Button
              onClick={()=>this.onSearchPress(false)}
              dismiss={true}
              disabled={libraries.length === 0 || searching || !this.selectedImage}
            >
              确定
            </Button>
          </Modal.Footer>
        </Modal>

        <Modal ref={ref=>this.settingModal=ref}>
          <Modal.Header>
            设置
          </Modal.Header>
          <span>结果数量 [1, 50]</span>
          <input
            className={styles.searchInput}
            value={size}
            onChange={this.onSizeTextChange}
          />
          <hr style={{margin: 0}} />
        </Modal>
      </div>
    );
  }
}

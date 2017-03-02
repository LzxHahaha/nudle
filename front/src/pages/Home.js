import React from 'react';
import FontAwesome from 'react-fontawesome';
import classNames from 'classnames';
import echarts from 'echarts';

import styles from './Home.css';

import Modal from '../components/modal';
import Button from '../components/Button';
import ResponseImage from '../components/ResponseImage';

import Request from '../utils/Request';

const HIST_NAMES = [
  'foreground-h', 'foreground-s', 'foreground-lbp', 'sift-statistics',
  'background-h', 'background-s', 'background-lbp'];

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
      searchTime: 0
    };

    this.selectedImage = '';
    this.imageReader = new FileReader();
    this.imageReader.onload =  e => this.selectedImage = e.target.result;
    this.searchLibrary = '';
    this.histograms = null;
    this.chart = null;
  }

  async componentWillMount() {
    try {
      const { libraries } = await Request.get(Request.URLs.libraries);
      this.setState({
        libraries,
        chooseLibrary: libraries[0]
      });
    }
    catch (err) {
      alert(err.message);
    }
  }

  async searchUrl() {
    return await Request.post(Request.URLs.searchUrl, {
      url: this.state.searchText,
      library: this.state.chooseLibrary
    });
  }

  async searchUpload() {
    return await Request.post(Request.URLs.searchUpload, {
      image: this.selectedImage,
      library: this.state.chooseLibrary
    });
  }

  onLibraryChange = e => {
    this.setState({ chooseLibrary: e.target.value });
  };

  onSearchTextChange = (e) => {
    this.setState({ searchText: e.target.value });
  };

  onImageChange = (e) => {
    const image = e.target.files[0];
    this.setState({ image });
    this.imageReader.readAsDataURL(image);
  };

  onSearchPress = async (isUrl) => {
    if (!this.state.chooseLibrary) {
      return null;
    }

    this.waitChart();
    await this.setState({searching: true, display: []});

    let result = null;
    try {
      if (isUrl) {
        this.setState({ sourceImage: this.state.searchText });
        result = await this.searchUrl();
      }
      else {
        this.setState({ sourceImage: this.selectedImage });
        result = await this.searchUpload();
      }

      this.searchLibrary = this.state.chooseLibrary;
      this.histograms = result.histograms;
      await this.setState({ display: result.list, searchTime: result.search_time });
      this.updateChart(HIST_NAMES[0]);
    }
    catch (err) {
      alert(err.message);
      await this.setState({ sourceImage: '' });
    }
    finally {
      this.setState({ searching: false });
      this.chart.hideLoading();
    }
  };

  onHistChange = (e) => {
    this.updateChart(e.target.value);
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
      animationDurationUpdate: 1200,
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

  waitChart = () => {
    if (this.histograms) {
      this.histograms = null;
    }
    if (this.chart) {
      this.chart.clear();
      this.chart.setOption({
        backgroundColor: '#E5E5E5'
      });
      this.chart.showLoading();
    }
  };

  render() {
    const { libraries, searching, display, searchText, sourceImage, searchTime } = this.state;

    return (
      <div className={styles.container}>
        <div className={styles.row}>
          <div className={classNames(styles.logo, (searching || display.length > 0) && styles.logoFold)}>
            <img src={require('../image/nudle.png')} height="80" />
          </div>
          <div className={styles.searchBox}>
            <select onChange={this.onLibraryChange} className={styles.libraryBox}>
              {
                libraries.map(el => <option value={el}>{el.toUpperCase()}</option>)
              }
            </select>
            <div className={styles.searchInputView}>
              <input
                className={styles.searchInput}
                placeholder="输入图片URL"
                onChange={this.onSearchTextChange}
                value={searchText}
              />
            </div>
            <a className={styles.imageButton} onClick={()=>this.modal.show()}>
              <FontAwesome name="cloud-upload" />
            </a>
            <Button className={styles.searchButton} onClick={()=>this.onSearchPress(true)}>
              搜索
            </Button>
          </div>

          {
            sourceImage && (
              <div>
                <h3>输入图片信息</h3>
                <div className={styles.inputImageView}>
                  <img src={sourceImage} className={styles.inputImage} />
                  <div className={styles.inputHistogramBox} id="histContainer">
                    <p style={{textAlign: 'center'}}>生成中...</p>
                  </div>
                  {
                    !!this.histograms && (
                      <select onChange={this.onHistChange} className={styles.histSelector}>
                        {
                          HIST_NAMES.map(el => (
                            <option>{el}</option>
                          ))
                        }
                      </select>
                    )
                  }
                </div>
              </div>
            )
          }

          {
            searching && (
              <p className={styles.searchingText}>
                搜索中...
              </p>
            )
          }

          {
            display.length > 0 && (
              <div>
                <h3>
                  搜索结果
                </h3>
                <p>
                  用时：{searchTime}秒
                </p>
                {
                  display.map(el => {
                    return (
                      <ResponseImage
                        src={`http://localhost:5000/static/lib_${this.searchLibrary}/${el.name}`}
                        className={styles.imagePreviewBox}
                        info={`${el.distance}`}
                      />
                    );
                  })
                }
              </div>
            )
          }
        </div>

        <Modal ref={ref=>this.modal=ref}>
          <Modal.Header>
            上传图片进行搜索
          </Modal.Header>
          <input
            type="file"
            accept=".png, .jpg, .jpeg"
            onChange={this.onImageChange}
          />
          <Modal.Footer>
            <Button onClick={()=>this.onSearchPress(false)} dismiss={true}>
              确定
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}

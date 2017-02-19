import React from 'react';
import FontAwesome from 'react-fontawesome';
import classNames from 'classnames';

import styles from './Home.css';

import Modal from '../components/modal';
import Button from '../components/Button';
import ResponseImage from '../components/ResponseImage';

import Request from '../utils/Request';

const LIBRARYS = [
  {label: 'VOC 2006', value: 'voc2006'}
];

export default class Home extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      modalVisible: false,
      searching: false,
      searchText: '',
      sourceImage: '',
      display: [],
      feature: [],
      library: LIBRARYS[0].value,
      searchTime: 0
    };

    this.selectedImage = '';
    this.imageReader = new FileReader();
    this.imageReader.onload =  e => this.selectedImage = e.target.result;
    this.searchLibrary = '';
    this.SIFTCount = 0
  }

  async searchUrl() {
    return await Request.post(Request.URLs.searchUrl, {
      url: this.state.searchText,
      library: this.state.library
    });
  }

  async searchUpload() {
    return await Request.post(Request.URLs.searchUpload, {
      image: this.selectedImage,
      library: this.state.library
    });
  }

  onLibraryChange = e => {
    this.setState({ library: e.target.value });
  };

  onHistogramChange = e => {
    this[`render${e.target.value}Histogram`]();
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
    this.setState({searching: true, display: [], feature: []});
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

      this.searchLibrary = this.state.library;
      this.SIFTCount = result.feature.length - 2 * (64 + 16 + 256);
      await this.setState({ display: result.list, feature: result.feature, searchTime: result.search_time });
      this.renderAllHistogram(result.feature);
    }
    catch (err) {
      alert(err.message);
      await this.setState({ sourceImage: '' });
      this.SIFTCount = 0;
    }
    finally {
      this.setState({ searching: false });
    }
  };

  renderAllHistogram(feature) {
    const ctx = this.histogram.getContext('2d');
    const { height } = this.histogram;

    ctx.clearRect(0, 0, feature.length * 3, height);
    ctx.save();
    ctx.fillStyle="#ff0000";

    const max = Math.max(...feature);
    const step = height / max;

    const segments = [
      63,
      63 + 16,
      63 + 16 + 256,
      63 + 16 + 256 + this.SIFTCount,
      63 + 16 + 256 + this.SIFTCount + 64,
      63 + 16 + 256 + this.SIFTCount + 64 + 16,
      feature.length
    ];
    const colors = [
      '#f00',
      '#0f0',
      '#00f',
      '#ff0',
      '#f00',
      '#0f0',
      '#00f'
    ];

    let j = 0;
    for (let i = 0; i < segments.length; ++i) {
      ctx.fillStyle = colors[i];
      for (; j < segments[i]; ++j) {
        const h = feature[j] * step;
        ctx.translate(0, height - h - 1);
        ctx.fillRect(0, 0, 3, h + 1);
        ctx.translate(3, h - height + 1);
      }
    }

    ctx.restore();
  }

  render() {
    const { searching, display, searchText, sourceImage, feature, searchTime } = this.state;

    return (
      <div className={styles.container}>
        <div className={styles.row}>
          <div className={classNames(styles.logo, (searching || display.length > 0) && styles.logoFold)}>
            <img src={require('../image/nudle.png')} height="80" />
          </div>
          <div className={styles.searchBox}>
            <select onChange={this.onLibraryChange} className={styles.libraryBox}>
              {
                LIBRARYS.map(el => <option value={el.value}>{el.label}</option>)
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
                  <div className={styles.inputHistogramBox}>
                    {
                      feature.length > 0 ? (
                        <div>
                          <div className={styles.inputHistogram}>
                            <canvas ref={ref => this.histogram = ref} height="190" width={feature.length * 3}>
                              请更新浏览器版本
                            </canvas>
                          </div>
                        </div>
                      ) : <h3>生成中...</h3>
                    }
                  </div>
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

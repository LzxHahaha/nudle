import React from 'react';
import FontAwesome from 'react-fontawesome';
import classNames from 'classnames';

import styles from './Home.css';

import Modal from '../components/modal';
import Button from '../components/Button';

import Request from '../utils/Request';

export default class Home extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      modalVisible: false,
      searching: false,
      searchText: '',
      sourceImage: '',
      display: [],
      feature: []
    };

    this.list = [];
    this.selectedImage = '';
    this.imageReader = new FileReader();
    this.imageReader.onload =  e => this.selectedImage = e.target.result;
  }

  async searchUrl() {
    const res = await Request.post(Request.URLs.searchUrl, {
      url: this.state.searchText
    });
    return res;
  }

  async searchUpload() {
    const res = await Request.post(Request.URLs.searchUpload, {
      image: this.selectedImage
    });
    return res;
  }

  onSearchTextChange = (e) => {
    this.setState({ searchText: e.target.value });
  };

  onImageChange = (e) => {
    const image = e.target.files[0];
    this.setState({ image });
    this.imageReader.readAsDataURL(image);
  };

  onSearchPress = async (isUrl) => {
    this.setState({searching: true, display: []});
    let result = null;
    let display = null;
    try {
      if (isUrl) {
        this.setState({ sourceImage: this.state.searchText });
        result = await this.searchUrl();
      }
      else {
        this.setState({ sourceImage: this.selectedImage });
        result = await this.searchUpload();
      }

      this.list = result.list;
      display = this.list.splice(0, 20);
      await this.setState({ display, feature: result.feature });
      this.renderHistogram(result.feature);
    }
    catch (err) {
      alert(err.message);
    }
    finally {
      this.setState({ searching: false });
    }
  };

  renderHistogram(feature) {
    const ctx = this.histogram.getContext('2d');
    const { height } = this.histogram;

    ctx.clearRect(0, 0, feature.length * 3, height);
    ctx.save();
    ctx.fillStyle="#ff0000";

    const max = Math.max(...feature);
    const step = height / max;

    // TODO: 区分开HSV和feature，以及前景背景
    for (let i = 0; i < feature.length; ++i) {
      if (i == 63) {
        ctx.fillStyle="#00ff00";
      }
      else if (i == 79) {
        ctx.fillStyle="#0000ff";
      }
      else if (i == 335) {
        ctx.fillStyle="#f0f";
      }

      const h = feature[i] * step;
      ctx.translate(0, height - h - 1);
      ctx.fillRect(0, 0, 3, h + 1);
      ctx.translate(3, h - height + 1);
    }

    ctx.restore();
  }

  render() {
    const { searching, display, searchText, sourceImage, feature } = this.state;

    return (
      <div className={styles.container}>
        <div className={classNames(styles.logo, (searching || display.length > 0) && styles.logoFold)}>
          <img src={require('../image/nudle.png')} height="80" />
        </div>
        <div className={styles.searchBox}>
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

        <div className={styles.row}>
          {
            sourceImage && (
              <div className={styles.inputImageView}>
                <img src={sourceImage} className={styles.inputImage} />
                <div className={styles.inputHistogram}>
                  <h3>图片信息直方图</h3>
                  <canvas ref={ref=>this.histogram=ref} height="150" width={feature.length * 3}>
                    加载中...
                  </canvas>
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
              display.map(el => {
                return (
                  <div className={styles.imagePreviewBox}>
                    <img
                      src={`http://localhost:5000/static/voc2006/${el}`}
                      className={styles.imagePreview}
                    />
                  </div>
                );
              })
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
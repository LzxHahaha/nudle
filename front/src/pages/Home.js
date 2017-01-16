import React from 'react';
import FontAwesome from 'react-fontawesome';
import classNames from 'classnames';

import styles from './Home.css';

import Modal from '../components/modal';
import Button from '../components/Button';

export default class Home extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      modalVisible: false,
      searching: false,
      searchText: '',
      image: '',
      display: []
    };

    this.list = [];
    this.imageReader = new FileReader();
    this.imageReader.onload =  e => this.setState({ sourceImage: e.target.result });
  }

  async searchUrl() {
    this.setState({ sourceImage: this.state.searchText });
    const res = await fetch('http://localhost:5000/api/search/url', {
      method: 'POST',
      body: JSON.stringify({url: this.state.searchText})
    });
    const text = await res.text();
    const json = JSON.parse(text);
    return json.result;
  }

  async searchUpload() {
    const formData = new FormData();
    formData.append('image', this.state.image);

    const res = await fetch('http://localhost:5000/api/search/upload', {
      method: 'POST',
      body: formData
    });
    const text = await res.text();
    const json = JSON.parse(text);
    return json.result;
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
    let list = null;
    let display = null;
    try {
      if (isUrl) {
        list = await this.searchUrl();
      }
      else {
        list = await this.searchUpload();
      }

      if (list) {
        this.list = list;
        display = list.splice(0, 20);
      }
      this.setState({ display });
    }
    catch (err) {
      alert(err.message);
    }
    finally {
      this.setState({ searching: false });
    }
  };

  render() {
    const { searching, display, searchText } = this.state;

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

        {
          searching && (
            <p className={styles.searchingText}>
              搜索中...
            </p>
          )
        }

        <img src={this.state.sourceImage} />

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

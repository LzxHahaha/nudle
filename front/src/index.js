import React from 'react';
import FontAwesome from 'react-fontawesome';

import styles from './index.css';

import Modal from './components/modal';
import Button from './components/Button';

export default class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      modalVisible: false
    };
  }

  onImageChange = (e) => {
    console.log({...e.target});
  };

  render() {
    return (
      <div className={styles.container}>
        <div className={styles.logo}>
          <img src={require('./image/nudle.png')} height="80" />
        </div>
        <div className={styles.searchBox}>
          <div className={styles.searchInputView}>
            <input className={styles.searchInput} placeholder="输入图片URL" />
          </div>
          <a className={styles.imageButton} onClick={()=>this.modal.show()}>
            <FontAwesome name="cloud-upload" />
          </a>
          <Button className={styles.searchButton}>
            搜索
          </Button>
        </div>

        <Modal ref={ref=>this.modal=ref}>
          <Modal.Header>
            上传图片进行搜索
          </Modal.Header>
          <input type="file" accept=".png, .jpg, .jpeg" onChange={this.onImageChange} />
          <Modal.Footer>
            <Button onClick={()=>{}}>
              确定
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}

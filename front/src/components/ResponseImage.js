/**
 * Created by LzxHahaha on 2017/2/19.
 */

import React from 'react';

import styles from './ResponseImage.css';

export default class ResponseImage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    const { src, info } = this.props;

    return (
      <div className={styles.box}>
        <img src={src} className={styles.image} />
        <div className={styles.infoBox}>
          <p className={styles.infoText}>{info}</p>
        </div>
      </div>
    );
  }
}

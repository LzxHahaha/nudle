/**
 * Created by LzxHahaha on 2017/1/7.
 */

import React, { PropTypes } from 'react';
import FontAwesome from 'react-fontawesome';

import styles from './Header.css';

export default class Header extends React.Component {
  static contextTypes = {
    hide: PropTypes.func
  };

  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    return (
      <div className={styles.container}>
        <div className={styles.content}>
          <h4 className={styles.header}>
            {this.props.children}
          </h4>
        </div>
        <FontAwesome name="close" className={styles.closeButton} onClick={this.context.hide} />
      </div>
    );
  }
}

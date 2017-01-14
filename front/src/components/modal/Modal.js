/**
 * Created by LzxHahaha on 2017/1/7.
 */

import React, { PropTypes } from 'react';
import classNames from 'classnames';

import styles from './Modal.css';

import Header from './Header';
import Footer from './Footer';

export default class Modal extends React.Component {
  static propTypes = {
    backdrop: PropTypes.bool,
    children: PropTypes.any
  };

  static defaultProps = {
    backdrop: true
  };

  static childContextTypes = {
    hide: PropTypes.func
  };

  constructor(props) {
    super(props);

    this.state = {
      visible: false
    };
  }

  getChildContext() {
    return {
      hide: this.hide
    };
  }

  show = () => {
    if (!this.state.visible) {
      this.setState({ visible: true });
    }
  };

  hide = () => {
    if (this.state.visible) {
      this.setState({ visible: false });
    }
  };

  toggle = () => {
    this.setState({ visible: !this.state.visible });
  };

  _onBackgroundClick = () => {
    if (this.props.backdrop) {
      this.setState({ visible: false });
    }
  };

  render() {
    const { children } = this.props;
    const { visible } = this.state;

    return (
      <div
        className={classNames(styles.container, !visible && styles.hide)}
        onClick={this._onBackgroundClick}
      >
        <div
          className={classNames(styles.content, !visible && styles.contentHide)}
          onClick={(e)=>e.stopPropagation()}
        >
          {children}
        </div>
      </div>
    );
  }
}

Modal.Header = Header;
Modal.Footer = Footer;

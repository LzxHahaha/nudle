/**
 * Created by LzxHahaha on 2017/1/7.
 */

import React, { PropTypes } from 'react';
import classNames from 'classnames';

import styles from './Button.css';

export default class Button extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  renderAnchor = () => {
    const { href, children, className, ...other } = this.props;

    return (
      <a href={href} {...this.props} className={classNames(styles.button, className)}>
        {children}
      </a>
    );
  };

  renderButton = () => {
    const { children, className, ...other } = this.props;

    return (
      <button {...other} className={classNames(styles.button, className)}>
        {children}
      </button>
    );
  };

  render() {
    const { href } = this.props;

    if (href) {
      return this.renderAnchor();
    }

    return this.renderButton();
  }
}

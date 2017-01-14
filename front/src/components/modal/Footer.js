/**
 * Created by LzxHahaha on 2017/1/7.
 */

import React, { PropTypes } from 'react';

import styles from './Footer.css';

export default class Footer extends React.Component {
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
        {
          React.Children.map(this.props.children, el => {
            if (!el.props) {
              return el;
            }
            const dismiss = el.props.dismiss;
            delete el.props.dismiss;

            if (!dismiss || !el.props.onClick) {
              return el;
            }

            return React.cloneElement(el, {
              onClick: () => {
                el.props.onClick();
                this.context.hide();
              }
            })
          })
        }
      </div>
    );
  }
}

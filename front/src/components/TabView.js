/**
 * Created by LzxHahaha on 2017/3/18.
 */

import React, { PropTypes } from 'react';
import classNames from 'classnames';

import styles from './TabView.css';

export default class TabView extends React.Component {
  static propTypes = {
    labels: PropTypes.arrayOf(PropTypes.string)
  };

  constructor(props) {
    super(props);

    this.state = {
      activeIndex: 0
    };
  }

  onLabelClick = (activeIndex) => {
    if (activeIndex !== this.state.activeIndex) {
      this.setState({ activeIndex });
    }
  };

  render() {
    const { activeIndex } = this.state;
    const { labels, className, children, ...other } = this.props;

    if (!labels || !labels.length) {
      return null;
    }

    const tabPresent = 100 / labels.length;

    return (
      <div {...other} className={classNames([className, styles.container])}>
        <div className={styles.labelContainer}>
          {
            labels.map((el, index) => {
              const active = index === activeIndex;
              return (
                <span
                  key={`label${index}`}
                  className={classNames([styles.label, active && styles.labelActive])}
                  onClick={()=>this.onLabelClick(index)}
                >
                  {el}
                </span>
              );
            })
          }
          <div
            className={styles.labelUnderline}
            style={{
              width: `${tabPresent / 4}%`,
              left: `${tabPresent * 1.5 / 4 + activeIndex * tabPresent}%`
            }}
          />
        </div>
        <div
          className={styles.tabContainer}
          style={{
            width: `${labels.length * 100}%`,
            left: `-${activeIndex * 100}%`
          }}
        >
          {
            React.Children.map(children, (el, index) => {
              return React.cloneElement(el, {
                key: `tab${index}`,
                className: classNames([el.props.className, styles.tab])
              });
            })
          }
        </div>
      </div>
    );
  }
}

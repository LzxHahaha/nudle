/**
 * Created by LzxHahaha on 2017/3/22.
 */

import React from 'react';

import styles from './Detail.css';

export default class Detail extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    return (
      <div>
        <p>{this.props.location.query.name}</p>
      </div>
    );
  }
}

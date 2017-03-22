/**
 * Created by LzxHahaha on 2017/3/22.
 */

import React from 'react';
import echarts from 'echarts';

import globalStyles from './site.css';
import styles from './Detail.css';

import { getImageDetail, HIST_NAMES } from '../logic/image';
import { HOST } from '../utils/Request';

export default class Detail extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      failed: false,
      imageLoading: true
    };
  }

  async componentDidMount() {
    try {
      const { lib, name } = this.props.location.query;

      if (!lib || !name) {
        this.setState({failed: true});
        return;
      }

      const result = await getImageDetail(lib, name);
      this.setState({
        ...result,
        loading: false
      }, () => this.renderHist(result.feature));
    }
    catch (err) {
      this.setState({failed: true});
    }
  }

  renderHist = (features) => {
    for (let i = 0; i < HIST_NAMES.length; ++i) {
      const dom = document.getElementById(HIST_NAMES[i]);
      const chartName = `chart${i}`;
      this[chartName] = echarts.init(dom);
      const data = features[i];
      this[chartName].setOption({
        xAxis: {
          data: []
        },
        yAxis: {
          splitLine: {show: true}
        },
        animationDurationUpdate: 1000,
        backgroundColor: '#E5E5E5',
        series: [{
          name: HIST_NAMES[i],
          type: 'bar',
          itemStyle: {
            normal: {
              color: '#3B85F7'
            }
          },
          animationDelay: idx => idx * 10,
          data
        }]
      });
    }
    window.onresize = () => {
      for (let i = 0; i < HIST_NAMES.length; ++i) {
        const chartName = `chart${i}`;
        this[chartName].resize();
      }
    };
  };

  render() {
    const { loading, failed, imageLoading, height, width } = this.state;
    const { lib, name } = this.props.location.query;

    if (failed) {
      return (
        <div className={globalStyles.container}>
          <div className={globalStyles.row}>
            <h3 style={{textAlign: 'center'}}>404 Not Found.</h3>
          </div>
        </div>
      );
    }

    return (
      <div className={globalStyles.container}>
        <div className={globalStyles.row}>
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <img src={require('../image/nudle.png')} height="50" />
              <span className={styles.cardHeaderText}>图片详情</span>
            </div>
            <div>
              {loading && '加载中...'}
            </div>
            <div className={styles.imageView}>
              <div className={styles.imageContainer}>
                {imageLoading && '图片加载中'}
                <img
                  src={`${HOST}static/lib_${lib}/${name}`} className={styles.image}
                  onLoad={()=>this.setState({imageLoading: false})}
                />
              </div>
              <div className={styles.info}>
                <p className={styles.infoTitle}>图片名称</p>{name}
                <p className={styles.infoTitle}>图片来源</p>{lib}
                <p className={styles.infoTitle}>图片尺寸</p>{height || 0}×{width || 0}
              </div>
            </div>
            <div>
              {
                HIST_NAMES.map((el, index) => {
                  return (
                    <div key={`hist${index}`}>
                      <h4>{el}</h4>
                      <div id={el} className={styles.chartContainer}>
                      </div>
                    </div>
                  )
                })
              }
            </div>
          </div>
        </div>
      </div>
    );
  }
}

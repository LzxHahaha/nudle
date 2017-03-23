/**
 * Created by LzxHahaha on 2017/3/22.
 */

import React from 'react';
import echarts from 'echarts';

import globalStyles from './site.css';
import styles from './Detail.css';

import { getInputFeature, getImageDetail, HIST_NAMES } from '../logic/image';
import { HOST } from '../utils/Request';

export default class Detail extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      failed: false,
      imageLoading: true,
      showDistance: false,
      distances: []
    };
  }

  async componentDidMount() {
    try {
      const { lib, name } = this.props.location.query;

      if (!lib || !name) {
        this.setState({failed: true});
        return;
      }

      this.input = getInputFeature();

      const result = await getImageDetail(lib, name);
      this.setState({
        ...result,
        loading: false
      }, () => this.renderHist(result.feature));
      if (this.input) {
        this.renderDistance(result.feature);
      }
    }
    catch (err) {
      console.log(err);
      this.setState({failed: true});
    }
  }

  renderDistance = (features) => {
    const distances = HIST_NAMES.map((el, index) => chisquare_distance(this.input[el], features[index]));
    this.setState({
      showDistance: true,
      distances
    });
  };

  renderHist = (features) => {
    const baseOptions = {
      yAxis: { splitLine: {show: true} },
      animationDurationUpdate: 1000,
      backgroundColor: '#E5E5E5',
      legend: {
        data: this.input ? ['当前图片', '输入图片'] : ['当前图片'],
        x: 'right',
        orient: 'vertical'
      },
      dataZoom: [{ type: 'slider' }],
    };

    for (let i = 0; i < HIST_NAMES.length; ++i) {
      const dom = document.getElementById(HIST_NAMES[i]);
      const chartName = `chart${i}`;
      this[chartName] = echarts.init(dom);
      const data = features[i];

      const series = [{
        name: '当前图片',
        type: 'bar',
        itemStyle: { normal: { color: '#3B85F7' } },
        animationDelay: idx => idx * 10,
        barGap: '-30%',
        data
      }];
      if (this.input) {
        series.push({
          name: '输入图片',
          type: 'bar',
          itemStyle: { normal: { color: '#FF4C41' } },
          animationDelay: idx => idx * 10,
          data: this.input[HIST_NAMES[i]]
        });
      }

      this[chartName].setOption({
        ...baseOptions,
        xAxis: { data: data.map((el, index) => index) },
        series
      });
    }
    window.onresize = () => HIST_NAMES.forEach((el, i) => this[`chart${i}`].resize());
  };

  render() {
    const { loading, failed, imageLoading, height, width, showDistance, distances } = this.state;
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
                      <h4>
                        {el}<br/>
                        {
                          showDistance && (
                            <span>
                              卡方距离：{distances[index] || 'Error'}
                            </span>
                          )
                        }
                      </h4>
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

function chisquare_distance(obs, exp) {
  let distance = 0;
  let mean = 0;
  obs.forEach((obsVal, index) => {
    const expVal = exp[index];
    mean += obsVal;
    if (obsVal + expVal > 0) {
      distance += (Math.sqrt(Math.abs(obsVal - expVal)) / (obsVal + expVal));
    }
  });
  mean /= obs.length;

  let std = 0;
  obs.forEach(el => std += Math.pow(el - mean, 2));
  std = Math.sqrt(std / obs.length);

  return (distance - mean) / std;
}

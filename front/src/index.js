import React from "react";
import { Router, Route, IndexRoute, browserHistory } from 'react-router';

import Home from './pages/Home';
import Detail from './pages/Detail';

export default class App extends React.Component {
  render() {
    return (
      <Router history={browserHistory}>
        <Route path="/">
          <IndexRoute component={Home} />
          <Route path="detail" component={Detail} />
        </Route>
      </Router>
    );
  }
}

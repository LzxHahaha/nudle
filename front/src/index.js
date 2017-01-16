import React from "react";
import { Router, Route, IndexRoute, browserHistory } from 'react-router';

import Home from './pages/Home';

export default class App extends React.Component {
  render() {
    return (
      <Router history={browserHistory}>
        <Route path="/">
          <IndexRoute component={Home} />
        </Route>
      </Router>
    );
  }
}

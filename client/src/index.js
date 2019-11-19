import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import defaultLogger from 'redux-logger';
import thunkMiddleware from 'redux-thunk';
import reducer from './reducer';
import './index.css';
import App from './App';
import INIT_STATE from './init_state';
import {
  fetchUserInfo,
  fetchSyncConfig,
  fetchAvailableCalendars,
  fetchDatabaseDetails,
} from './actions';
import * as serviceWorker from './serviceWorker';

let middleware = [thunkMiddleware];
if (process.env.NODE_ENV !== 'production') {
  middleware.push(defaultLogger);
}

const store = createStore(reducer, applyMiddleware(...middleware));

store.dispatch({
  type: 'SET_STATE',
  state: INIT_STATE
});
store.dispatch(fetchUserInfo());
store.dispatch(fetchSyncConfig());
store.dispatch(fetchAvailableCalendars());
store.dispatch(fetchDatabaseDetails());

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

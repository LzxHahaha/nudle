/**
 * Created by LzxHahaha on 2017/1/18.
 */

import URI from 'urijs';

export const HOST = process.env.NODE_ENV === 'production' ? '/' : 'http://localhost:5001/';

export default class Request {
  static async get(url, data) {
    return await Request.request(url, 'GET', data);
  }

  static async post(url, data) {
    return await Request.request(url, 'POST', data);
  }

  static async request(url, method, data) {
    let requestURL = HOST + url;

    let body = undefined;
    if (method === 'GET') {
      if (data) {
        const uri = new URI(requestURL);
        uri.query(data);
        requestURL = uri.toString();
      }
    }
    else if (method === 'POST') {
      body = new FormData();
      for (let i in data) {
        body.append(i, data[i]);
      }
    }
    else {
      throw new Error('Unknown method.');
    }

    let headers = {
      'Accept': 'application/json'
    };

    const res = await fetch(requestURL, {
      method,
      headers,
      body
    });
    if (res.ok) {
      const text = await res.text();
      const json = JSON.parse(text);
      if (json.code === 200) {
        return json.data;
      }
      else {
        throw new Error(json.message);
      }
    }
    else {
      throw new Error(res.code);
    }
  }
}

Request.URLs = {
  libraries: 'api/libraries',
  searchUpload: 'api/search/upload',
  searchUrl: 'api/search/url',
  detail: 'api/image'
};

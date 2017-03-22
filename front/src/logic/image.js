/**
 * Created by LzxHahaha on 2017/3/22.
 */

import Request from '../utils/Request';

let libraries = null;

export const HIST_NAMES = [
  'foreground-h', 'foreground-s', 'foreground-lbp', 'sift-statistics',
  'background-h', 'background-s', 'background-lbp'
];

export async function searchUrl(url, library, size) {
  return await Request.post(Request.URLs.searchUrl, { url, library, size });
}

export async function searchUpload(image, library, size) {
  return await Request.post(Request.URLs.searchUpload, { image, library, size });
}

export async function getLibraries(update = false) {
  if (update || !libraries) {
    const data = await Request.get(Request.URLs.libraries);
    libraries = data.libraries;
  }
  return libraries;
}

export async function getImageDetail(lib, name) {
  const url = `${Request.URLs.detail}/${lib}/${name}`;
  return await Request.get(url);
}

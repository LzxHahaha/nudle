/**
 * Created by LzxHahaha on 2017/3/22.
 */

import Request from '../utils/Request';

let libraries = null;

const INPUT_FEATURE_KEY = 'inputFeature';

export const HIST_NAMES = [
  'foreground-h', 'foreground-s', 'foreground-lbp', 'sift-statistics',
  'background-h', 'background-s', 'background-lbp'
];

function saveInputFeature(feature) {
  sessionStorage.setItem(INPUT_FEATURE_KEY, JSON.stringify(feature));
}

export function getInputFeature() {
  return JSON.parse(sessionStorage.getItem(INPUT_FEATURE_KEY));
}

export async function searchUrl(url, library, size) {
  const result = await Request.post(Request.URLs.searchUrl, { url, library, size });
  saveInputFeature(result.histograms);
  return result;
}

export async function searchUpload(image, library, size) {
  const result = await Request.post(Request.URLs.searchUpload, { image, library, size });
  saveInputFeature(result.histograms);
  return result;
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

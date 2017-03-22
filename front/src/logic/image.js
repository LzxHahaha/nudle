/**
 * Created by LzxHahaha on 2017/3/22.
 */

import Request from '../utils/Request';

let inputFeature = null;
let libraries = null;

export function getInputFeature() {
  return inputFeature;
}

export async function searchUrl(url, library, size) {
  const result = await Request.post(Request.URLs.searchUrl, { url, library, size });
  inputFeature = result.histograms;
  return result;
}

export async function searchUpload(image, library, size) {
  const result = await Request.post(Request.URLs.searchUpload, { image, library, size });
  inputFeature = result.histograms;
  return result;
}

export async function getLibraries(update = false) {
  if (update || !libraries) {
    const data = await Request.get(Request.URLs.libraries);
    libraries = data.libraries;
  }
  return libraries;
}

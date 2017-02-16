#pragma once

#include <string>
#include <opencv.hpp>

using std::string;
using cv::Mat;

#ifndef GPP

#ifdef SALIENCY_DLL
#define SALIENCY_DLL extern "C" _declspec(dllimport) 
#else
#define SALIENCY_DLL extern "C" _declspec(dllexport) 
#endif

SALIENCY_DLL Mat RC_cut_from(char* path);
SALIENCY_DLL Mat RC_cut(Mat image);

#endif // !GPP

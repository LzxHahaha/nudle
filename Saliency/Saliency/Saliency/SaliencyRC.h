#pragma once

#include "../Basic/Definition.h"

struct SaliencyRC
{
	typedef Mat(*GET_SAL_FUNC)(CMat &);

	// Region Contrast 
	static Mat GetRC(CMat &img3f);
	static Mat GetRC(CMat &img3f, CMat &idx1i, int regNum, double sigmaDist = 0.4);
	static Mat GetRC(CMat &img3f, double sigmaDist, double segK, int segMinSize, double segSigma);

	static void SmoothByHist(CMat &img3f, Mat &sal1f, float delta);
	static void SmoothByRegion(Mat &sal1f, CMat &idx1i, int regNum, bool bNormalize = true);

private:
	static const int SAL_TYPE_NUM = 5;

	static void SmoothSaliency(Mat &sal1f, float delta, const vector<vector<CostfIdx>> &similar);
	static void SmoothSaliency(CMat &colorNum1i, Mat &sal1f, float delta, const vector<vector<CostfIdx>> &similar);

	struct Region
	{
		Region() { pixNum = 0; ad2c = Point2d(0, 0); }
		int pixNum;  // Number of pixels
		vector<CostfIdx> freIdx;  // Frequency of each color and its index
		Point2d centroid;
		Point2d ad2c; // Average distance to image center
	};
	static void BuildRegions(CMat& regIdx1i, vector<Region> &regs, CMat &colorIdx1i, int colorNum);
	static void RegionContrast(const vector<Region> &regs, CMat &color3fv, Mat& regSal1d, double sigmaDist);

	static int Quantize(CMat& img3f, Mat &idx1i, Mat &_color3f, Mat &_colorNum, double ratio = 0.95, const int colorNums[3] = DefaultNums);
	static const int DefaultNums[3];

	// Get border regions, which typically corresponds to background region
	static Mat GetBorderReg(CMat &idx1i, int regNum, double ratio = 0.02, double thr = 0.3);
};

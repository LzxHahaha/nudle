#pragma once
#include <opencv.hpp>

#include "../Basic/Definition.h"
#include "../Cluster/GMM.h"
#include "../Segmentation/Maxflow/graph.h"

class SaliencyCut
{
public:
	enum TrimapValue { TrimapBackground = 0, TrimapUnknown = 128, TrimapForeground = 255 };

	void drawResult(Mat& maskForeGround) { compare(_segVal1f, 0.5, maskForeGround, CMP_GT); }

	SaliencyCut(CMat &img3f);
	~SaliencyCut();

	static Mat cut(string path);
	static Mat cut(Mat img3f);
	static Mat CutObjs(CMat &img3f, CMat &sal1f, float t1 = 0.2f, float t2 = 0.9f,
		CMat &borderMask = Mat(), int wkSize = 20);

	// Initial rect region in between thr1 and thr2 and others below thr1 as the Grabcut paper 
	void initialize(const Rect &rect);
	void initialize(CMat &sal1f, float t1, float t2);
	void initialize(CMat &sal1u); // Background = 0, unknown = 128, foreground = 255

	void fitGMMs();
	int refineOnce();

private:
	void initGraph();	// builds the graph for GraphCut

	// Update hard segmentation after running GraphCut, 
	// Returns the number of pixels that have changed from foreground to background or vice versa.
	int updateHardSegmentation();

	// Return number of difference and then expand fMask to get mask1u.
	static int ExpandMask(CMat &fMask, Mat &mask1u, CMat &bdReg1u, int expandRatio = 5);

private:
	float _lambda;		// lambda = 50. This value was suggested the GrabCut paper.
	float _beta;		// beta = 1 / ( 2 * average of the squared color distances between all pairs of neighboring pixels (8-neighborhood) )
	float _L;			// L = a large value to force a pixel to be foreground or background

	int _w, _h;		// Width and height of the source image

	int _directions[4]; // From DIRECTION8 for easy location

	GMM _bGMM, _fGMM; // Background and foreground GMM

	Mat _imgBGR3f, _imgLab3f; // BGR images is used to find GMMs and Lab for pixel distance
	Mat _trimap1i;	// Trimap value
	Mat _segVal1f;	// Hard segmentation with type SegmentationValue
	Mat _bGMMidx1i, _fGMMidx1i;	// Background and foreground GMM components, supply memory for GMM, not used for Grabcut 
	Mat _show3u; // Image for display medial results
	
	// Storage for N-link weights, each pixel stores links to only four of its 8-neighborhood neighbors.
	// This avoids duplication of links, while still allowing for relatively easy lookup.
	// First 4 directions in DIRECTION8 are: right, rightBottom, bottom, leftBottom.
	Mat_<Vec4f> _NLinks;

	GraphF *_graph;
};


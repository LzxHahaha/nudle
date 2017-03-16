#include "SaliencyCut.h"
#include "SaliencyRC.h"
#include "../Basic/Cv.h"

SaliencyCut::SaliencyCut(CMat &img3f)
	:_fGMM(5), _bGMM(5), _w(img3f.cols), _h(img3f.rows), _lambda(50)
{
	CV_Assert(img3f.data != NULL && img3f.type() == CV_32FC3);
	_imgBGR3f = img3f;
	cvtColor(_imgBGR3f, _imgLab3f, CV_BGR2Lab);
	_trimap1i = Mat::zeros(_h, _w, CV_32S);
	_segVal1f = Mat::zeros(_h, _w, CV_32F);
	_graph = NULL;

	_L = 8 * _lambda + 1;// Compute L
	_beta = 0;
	{// compute beta
		int edges = 0;
		double result = 0;
		for (int y = 0; y < _h; ++y)
		{
			const Vec3f* img = _imgLab3f.ptr<Vec3f>(y);
			for (int x = 0; x < _w; ++x)
			{
				Point pnt(x, y);
				for (int i = 0; i < 4; i++)
				{
					Point pntN = pnt + DIRECTION8[i];
					if (CHK_IND(pntN))
						result += vecSqrDist(_imgLab3f.at<Vec3f>(pntN), img[x]), edges++;
				}
			}
		}
		_beta = (float)(0.5 * edges / result);
	}
	_NLinks.create(_h, _w);
	{
		// computeNLinks
		static const float dW[4] = { 1, (float)(1 / SQRT2), 1, (float)(1 / SQRT2) };
		for (int y = 0; y < _h; y++)
		{
			Vec4f *nLink = _NLinks.ptr<Vec4f>(y);
			const Vec3f* img = _imgLab3f.ptr<Vec3f>(y);
			for (int x = 0; x < _w; x++, nLink++)
			{
				Point pnt(x, y);
				const Vec3f& c1 = img[x];
				for (int i = 0; i < 4; i++)
				{
					Point pntN = pnt + DIRECTION8[i];
					if (CHK_IND(pntN))
						(*nLink)[i] = _lambda * dW[i] * exp(-_beta * vecSqrDist(_imgLab3f.at<Vec3f>(pntN), c1));
				}
			}
		}
	}

	for (int i = 0; i < 4; i++)
		_directions[i] = DIRECTION8[i].x + DIRECTION8[i].y * _w;
}

SaliencyCut::~SaliencyCut()
{
	if (_graph)
		delete _graph;
}

Mat SaliencyCut::Cut(string path)
{
	Mat img = imread(path);
	CV_Assert_(img.data != NULL, ("Can't load image %s\n", _S(path)));
	return SaliencyCut::Cut(img);
}

Mat SaliencyCut::Cut(Mat img)
{
	img.convertTo(img, CV_32FC3, 1.0 / 255);
	Mat sal = SaliencyRC::GetRC(img);
	//imshow("map", sal);
	//waitKey(1);

	Mat cutMat;
	float t = 0.9f;
	int maxIt = 4;
	GaussianBlur(sal, sal, Size(9, 9), 0);
	normalize(sal, sal, 0, 1, NORM_MINMAX);
	while (cutMat.empty() && maxIt--)
	{
		cutMat = SaliencyCut::CutObjs(img, sal, 0.1f, t);
		t -= 0.2f;
	}
	return cutMat;
}

Mat SaliencyCut::CutObjs(CMat &_img3f, CMat &_sal1f, float t1, float t2, CMat &_border1u, int wkSize)
{
	Mat border1u = _border1u;
	if (border1u.data == NULL || border1u.size != _img3f.size)
	{
		int bW = cvRound(0.02 * _img3f.cols), bH = cvRound(0.02 * _img3f.rows);
		border1u.create(_img3f.rows, _img3f.cols, CV_8U);
		border1u = 255;
		border1u(Rect(bW, bH, _img3f.cols - 2 * bW, _img3f.rows - 2 * bH)) = 0;
	}
	Mat sal1f, wkMask;
	_sal1f.copyTo(sal1f);
	sal1f.setTo(0, border1u);

	cv::Rect rect(0, 0, _img3f.cols, _img3f.rows);
	if (wkSize > 0)
	{
		threshold(sal1f, sal1f, t1, 1, THRESH_TOZERO);
		sal1f.convertTo(wkMask, CV_8U, 255);
		threshold(wkMask, wkMask, 70, 255, THRESH_TOZERO);
		wkMask = Cv::GetNZRegionsLS(wkMask, 0.005);
		if (wkMask.data == NULL)
			return Mat();
		rect = Cv::GetMaskRange(wkMask, wkSize);
		sal1f = sal1f(rect);
		border1u = border1u(rect);
		wkMask = wkMask(rect);
	}
	CMat img3f = _img3f(rect);

	Mat fMask;
	SaliencyCut salCut(img3f);
	salCut.initialize(sal1f, t1, t2);
	const int outerIter = 4;
	//salCut.showMedialResults("Ini");
	for (int j = 0; j < outerIter; j++)
	{
		salCut.fitGMMs();
		int changed = 1000, times = 8;
		while (changed > 50 && times--)
		{
			//salCut.showMedialResults("Medial results");
			changed = salCut.refineOnce();
			//waitKey(1);
		}
		//salCut.showMedialResults(format("It%d", j));
		//waitKey(0);
		salCut.drawResult(fMask);

		fMask = Cv::GetNZRegionsLS(fMask);
		if (fMask.data == NULL)
			return Mat();

		if (j == outerIter - 1 || ExpandMask(fMask, wkMask, border1u, 5) < 10)
			break;

		salCut.initialize(wkMask);
		fMask.copyTo(wkMask);
	}

	Mat resMask = Mat::zeros(_img3f.size(), CV_8U);
	fMask.copyTo(resMask(rect));
	return resMask;
}

// Initialize using saliency map. In the Trimap: background < t1, foreground > t2, others unknown.
// Saliency values are in [0, 1], "sal1f" and "1-sal1f" are used as weight to train fore and back ground GMMs
void SaliencyCut::initialize(CMat &sal1f, float t1, float t2)
{
	CV_Assert(sal1f.type() == CV_32F && sal1f.size == _imgBGR3f.size);
	sal1f.copyTo(_segVal1f);

	for (int y = 0; y < _h; y++)
	{
		int* triVal = _trimap1i.ptr<int>(y);
		const float *segVal = _segVal1f.ptr<float>(y);
		for (int x = 0; x < _w; x++)
		{
			triVal[x] = segVal[x] < t1 ? TrimapBackground : TrimapUnknown;
			triVal[x] = segVal[x] > t2 ? TrimapForeground : triVal[x];
		}
	}
}

void SaliencyCut::initialize(CMat &sal1u) // Background = 0, unknown = 128, foreground = 255
{
	CV_Assert(sal1u.type() == CV_8UC1 && sal1u.size == _imgBGR3f.size);
	for (int y = 0; y < _h; y++)
	{
		int* triVal = _trimap1i.ptr<int>(y);
		const byte *salVal = sal1u.ptr<byte>(y);
		float *segVal = _segVal1f.ptr<float>(y);
		for (int x = 0; x < _w; x++)
		{
			triVal[x] = salVal[x] < 70 ? TrimapBackground : TrimapUnknown;
			triVal[x] = salVal[x] > 200 ? TrimapForeground : triVal[x];
			segVal[x] = salVal[x] < 70 ? 0 : 1.f;
		}
	}
}

// Initial rect region in between thr1 and thr2 and others below thr1 as the Grabcut paper 
void SaliencyCut::initialize(const Rect &rect)
{
	_trimap1i = TrimapBackground;
	_trimap1i(rect) = TrimapUnknown;
	_segVal1f = 0;
	_segVal1f(rect) = 1;
}


void SaliencyCut::fitGMMs()
{
	_fGMM.BuildGMMs(_imgBGR3f, _fGMMidx1i, _segVal1f);
	_bGMM.BuildGMMs(_imgBGR3f, _bGMMidx1i, 1 - _segVal1f);
}

int SaliencyCut::refineOnce()
{
	// Steps 4 and 5: Learn new GMMs from current segmentation
	if (_fGMM.GetSumWeight() < 50 || _bGMM.GetSumWeight() < 50)
		return 0;

	_fGMM.RefineGMMs(_imgBGR3f, _fGMMidx1i, _segVal1f);
	_bGMM.BuildGMMs(_imgBGR3f, _bGMMidx1i, 1 - _segVal1f);

	// Step 6: Run GraphCut and update segmentation
	initGraph();
	if (_graph)
		_graph->maxflow();

	return updateHardSegmentation();
}

void SaliencyCut::initGraph()
{
	// Set up the graph (it can only be used once, so we have to recreate it each time the graph is updated)
	if (_graph == NULL)
		_graph = new GraphF(_w * _h, 4 * _w * _h);
	else
		_graph->reset();
	_graph->add_node(_w * _h);

	for (int y = 0, id = 0; y < _h; ++y)
	{
		int* triMapD = _trimap1i.ptr<int>(y);
		const float* img = _imgBGR3f.ptr<float>(y);
		for (int x = 0; x < _w; x++, img += 3, id++)
		{
			float back, fore;
			if (triMapD[x] == TrimapUnknown)
			{
				fore = -log(_bGMM.P(img));
				back = -log(_fGMM.P(img));
			}
			else if (triMapD[x] == TrimapBackground)
				fore = 0, back = _L;
			else		// TrimapForeground
				fore = _L, back = 0;

			// Set T-Link weights
			_graph->add_tweights(id, fore, back); // _graph->set_tweights(_nodes(y, x), fore, back);

												  // Set N-Link weights from precomputed values
			Point pnt(x, y);
			const Vec4f& nLink = _NLinks(pnt);
			for (int i = 0; i < 4; i++)
			{
				Point nPnt = pnt + DIRECTION8[i];
				if (CHK_IND(nPnt))
					_graph->add_edge(id, id + _directions[i], nLink[i], nLink[i]);
			}
		}
	}
}

int SaliencyCut::updateHardSegmentation()
{
	int changed = 0;
	for (int y = 0, id = 0; y < _h; ++y)
	{
		float* segVal = _segVal1f.ptr<float>(y);
		int* triMapD = _trimap1i.ptr<int>(y);
		for (int x = 0; x < _w; ++x, id++)
		{
			float oldValue = segVal[x];
			if (triMapD[x] == TrimapBackground)
				segVal[x] = 0.f; // SegmentationBackground
			else if (triMapD[x] == TrimapForeground)
				segVal[x] = 1.f; // SegmentationForeground
			else
				segVal[x] = _graph->what_segment(id) == GraphF::SOURCE ? 1.f : 0.f;
			changed += abs(segVal[x] - oldValue) > 0.1 ? 1 : 0;
		}
	}
	return changed;
}

int SaliencyCut::ExpandMask(CMat &fMask, Mat &mask1u, CMat &bdReg1u, int expandRatio)
{
	compare(fMask, mask1u, mask1u, CMP_NE);
	int changed = cvRound(sum(mask1u).val[0] / 255.0);

	Mat bigM, smalM;
	dilate(fMask, bigM, Mat(), Point(-1, -1), expandRatio);
	erode(fMask, smalM, Mat(), Point(-1, -1), expandRatio);
	static const double erodeSmall = 255 * 50;
	if (sum(smalM).val[0] < erodeSmall)
		smalM = fMask;
	mask1u = bigM * 0.5 + smalM * 0.5;
	mask1u.setTo(0, bdReg1u);
	return changed;
}

#include "stdafx.h"
#include "Saliency.h"
#include "Saliency/SaliencyCut.h"

Mat RC_cut_from(char* path)
{
	string p = path;
	return SaliencyCut::cut(p);
}

Mat RC_cut(Mat image)
{
	return SaliencyCut::cut(image);
}

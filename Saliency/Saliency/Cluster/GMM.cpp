#include "GMM.h"

void GMM::reWeights(vecD &mulWs)
{
	double sumW = 0;
	vecD newW(_K);
	for (int i = 0; i < _K; i++)
	{
		newW[i] = _Guassians[i].w * mulWs[i];
		sumW += newW[i];
	}
	for (int i = 0; i < _K; i++)
		_Guassians[i].w = newW[i] / sumW;
}

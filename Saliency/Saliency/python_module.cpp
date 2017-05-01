#define PY_ARRAY_UNIQUE_SYMBOL pbcvt_ARRAY_API

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include "pyboostcvconverter/pyboostcvconverter.hpp"
#include "Saliency/SaliencyCut.h"
#include "Saliency/SaliencyRC.h"

namespace pbcvt
{
	using namespace boost::python;

	PyObject *rc_mask(PyObject *input, double sigmaDist = 0.4, double segK = 50, int segMinSize = 200, double segSigma = 0.5)
	{
		auto image = pbcvt::fromNDArrayToMat(input);
		auto mask = SaliencyCut::Cut(image, sigmaDist, segK, segMinSize, segSigma);
		return pbcvt::fromMatToNDArray(mask);
	}

	PyObject *rc_map(PyObject *input)
	{
		auto image = pbcvt::fromNDArrayToMat(input);
		image.convertTo(image, CV_32FC3, 1.0 / 255);
		auto map = SaliencyRC::GetRC(image);
		return pbcvt::fromMatToNDArray(map);
	}

#if (PY_VERSION_HEX >= 0x03000000)
	static void *init_ar()
#else
	static void init_ar()
#endif
	{
		Py_Initialize();

		import_array();
		return NUMPY_IMPORT_ARRAY_RETVAL;
	}

	BOOST_PYTHON_FUNCTION_OVERLOADS(rc_mask_overloads, rc_mask, 1, 5)
	BOOST_PYTHON_MODULE(saliency_cut)
	{
		init_ar();

		to_python_converter<cv::Mat, pbcvt::matToNDArrayBoostConverter>();
		pbcvt::matFromNDArrayBoostConverter();

		def("rc_mask", rc_mask, rc_mask_overloads());
		def("rc_map", rc_map);
	}
}

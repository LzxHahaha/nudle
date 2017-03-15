#define PY_ARRAY_UNIQUE_SYMBOL pbcvt_ARRAY_API

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include "pyboostcvconverter/pyboostcvconverter.hpp"
#include "Saliency/SaliencyCut.h"

namespace pbcvt
{
	using namespace boost::python;

	PyObject *rc_cut(PyObject *input)
	{
		auto image = pbcvt::fromNDArrayToMat(input);
		auto mask = SaliencyCut::cut(image);
		return pbcvt::fromMatToNDArray(mask);
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

	BOOST_PYTHON_MODULE(saliency_cut)
	{
		init_ar();

		to_python_converter<cv::Mat, pbcvt::matToNDArrayBoostConverter>();
		pbcvt::matFromNDArrayBoostConverter();

		def("rc_cut", rc_cut);
	}
}

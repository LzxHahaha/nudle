#define PY_ARRAY_UNIQUE_SYMBOL pbcvt_ARRAY_API

#include <boost/python.hpp>
#include "pyboostcvconverter/pyboostcvconverter.hpp"
#include "Saliency/SaliencyCut.h"

namespace pbcvt
{
	using namespace boost::python;

	/**
	 * Example function. Basic inner matrix product using explicit matrix conversion.
	 * @param left left-hand matrix operand (NdArray required)
	 * @param right right-hand matrix operand (NdArray required)
	 * @return an NdArray representing the dot-product of the left and right operands
	 */
	PyObject *cut(PyObject *input)
	{
		auto image = pbcvt::fromNDArrayToMat(input);
		auto mask = SaliencyCut::cut(image);
		return pbcvt::fromMatToNDArray(mask);
	}

#if (PY_VERSION_HEX >= 0x03000000)

	static void *init_ar()
	{
#else
	static void init_ar()
	{
#endif
		Py_Initialize();

		import_array();
		return NUMPY_IMPORT_ARRAY_RETVAL;
	}

	BOOST_PYTHON_MODULE(saliency_rc_cut)
	{
		//using namespace XM;
		init_ar();

		//initialize converters
		to_python_converter<cv::Mat,
			pbcvt::matToNDArrayBoostConverter>();
		pbcvt::matFromNDArrayBoostConverter();

		//expose module-level functions
		def("cut", cut);
	}
} //end namespace pbcvt

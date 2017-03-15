#ifndef CVBOOSTCONVERTER_HPP_
#define CVBOOSTCONVERTER_HPP_

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/ndarrayobject.h>
#include <opencv2/core/core.hpp>
#include <boost/python.hpp>
#include <cstdio>

namespace pbcvt
{
	using namespace cv;

	static PyObject* opencv_error = 0;

#define ERRWRAP2(expr) \
try \
{ \
    PyAllowThreads allowThreads; \
    expr; \
} \
catch (const cv::Exception &e) \
{ \
    PyErr_SetString(opencv_error, e.what()); \
    return 0; \
}

	static int failmsg(const char *fmt, ...);
	static PyObject* failmsgp(const char *fmt, ...);

	class PyAllowThreads;
	class PyEnsureGIL;

	static size_t REFCOUNT_OFFSET = (size_t)&(((PyObject*)0)->ob_refcnt) +
		(0x12345678 != *(const size_t*)"\x78\x56\x34\x12\0\0\0\0\0") * sizeof(int);

	static inline PyObject* pyObjectFromRefcount(const int* refcount)
	{
		return (PyObject*)((size_t)refcount - REFCOUNT_OFFSET);
	}

	static inline int* refcountFromPyObject(const PyObject* obj)
	{
		return (int*)((size_t)obj + REFCOUNT_OFFSET);
	}

	class NumpyAllocator;

	PyObject* fromMatToNDArray(const Mat& m);
	Mat fromNDArrayToMat(PyObject* o);

	struct matToNDArrayBoostConverter
	{
		static PyObject* convert(Mat const& m);
	};

	struct matFromNDArrayBoostConverter
	{
		matFromNDArrayBoostConverter();

		/// @brief Check if PyObject is an array and can be converted to OpenCV matrix.
		static void* convertible(PyObject* object);

		/// @brief Construct a Mat from an NDArray object.
		static void construct(PyObject* object,
			boost::python::converter::rvalue_from_python_stage1_data* data);
	};
}
#endif /* CVBOOSTCONVERTER_HPP_ */

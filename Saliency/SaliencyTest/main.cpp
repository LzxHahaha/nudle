#include <Saliency.h>
#include <opencv.hpp>

using namespace cv;

int main()
{
	auto res = RC_cut_from("D:/Works/Code/image-retrieval/server/static/voc2006/000003.png");
	namedWindow("image");
	imshow("image", res);
	waitKey(0);
}

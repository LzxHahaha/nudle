%module Saliency

%include <opencv.i>
%cv_instantiate_all_defaults

%{
    #include "Saliency.cpp"
%}

%include "Saliency.cpp"
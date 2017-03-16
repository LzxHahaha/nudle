#pragma once

#include <string>

// 导出给SaliencyTest项目做测试用
extern "C" __declspec(dllexport) void rc_cut(std::string path);

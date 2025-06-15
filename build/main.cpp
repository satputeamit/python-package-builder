
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(main, m) {
    m.doc() = "main module";
    m.def("main", []() {
        std::cout << "aaa" << std::endl;
        return 0;
    });
}

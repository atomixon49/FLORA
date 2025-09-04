cmake_minimum_required(VERSION 3.15)
project(flora_cpp_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenSSL REQUIRED)

add_library(flora_cpp_core
	src/aes_gcm.cpp
)

target_include_directories(flora_cpp_core
	PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(flora_cpp_core
	PUBLIC OpenSSL::Crypto
)

add_library(flora::core ALIAS flora_cpp_core)

# Opcional: ejemplo
add_executable(flora_example examples/example_encrypt.cpp)
target_link_libraries(flora_example PRIVATE flora::core)

add_library(flora_c SHARED src/c_api.cpp)

target_include_directories(flora_c
	PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(flora_c
	PRIVATE flora::core
)


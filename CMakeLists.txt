cmake_minimum_required(VERSION 3.20)
project(symbolic_alpha_synthesizer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler warnings and optimization flags
if(MSVC)
    add_compile_options(/W4 /WX /O2 /fp:fast)
else()
    add_compile_options(-O3 -Wall -Wextra -Werror -fPIC -ffast-math)
    if(APPLE)
        add_compile_options(-arch arm64)
    endif()
endif()

# Shared library target
add_library(chimera_eval SHARED
    csrc/chimera_eval.cpp
    csrc/chimera_eval.hpp
)

set_target_properties(chimera_eval PROPERTIES
    PREFIX "lib"
    OUTPUT_NAME "chimera_eval"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/csrc"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/csrc"
)

# Python environment detection (.venv preferred)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin/python")
    set(PYTHON_EXECUTABLE "${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin/python")
else()
    find_program(PYTHON_EXECUTABLE NAMES python3 python)
endif()

if(PYTHON_EXECUTABLE)
    add_custom_target(audit
        COMMAND ${PYTHON_EXECUTABLE} scripts/audit_safety_invariants.py
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        COMMENT "Running Power of 10 Safety Invariants AST Audit"
    )

    add_custom_target(run_tests
        COMMAND ${CMAKE_COMMAND} -E env PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/src ${PYTHON_EXECUTABLE} -m pytest tests/ -v
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        DEPENDS chimera_eval
        COMMENT "Running Pytest test suite"
    )
endif()

CXX ?= clang++
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
    TARGET = libchimera_eval.dylib
    CXXFLAGS = -std=c++20 -O3 -Wall -Wextra -Werror -fPIC -ffast-math -arch arm64
    LDFLAGS = -shared
else
    TARGET = libchimera_eval.so
    CXXFLAGS = -std=c++20 -O3 -Wall -Wextra -Werror -fPIC -ffast-math
    LDFLAGS = -shared
endif

all: $(TARGET)

$(TARGET): chimera_eval.cpp chimera_eval.hpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ chimera_eval.cpp

clean:
	rm -f libchimera_eval.dylib libchimera_eval.so *.o

.PHONY: all clean

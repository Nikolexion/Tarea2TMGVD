CXX = g++
CXXFLAGS = -std=c++11 -O3 -Wall -w
TARGET = main.out
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC) mrl.h
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)


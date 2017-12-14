all: tempviewer

tempviewer: tempviewer.cpp
	g++ -lgmic -o tempviewer tempviewer.cpp

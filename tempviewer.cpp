#include <gmic.h>
#include <sys/stat.h>
#include <iostream>
#include <string>
using namespace std;

int main(int argc, char **argv) {
	struct stat sb;
	gmic interpreter;
	gmic_list<float> images;
	gmic_list<char> names;
	string buffer;
	int i;

	for(i = 1;argv[i];++i) {
		buffer += ' ';
		buffer += argv[i];

		if (stat(argv[i], &sb) == -1)
			continue;
		else if (sb.st_size == 76800)
			buffer += ",160,120";
		else if (sb.st_size == 19200)
			buffer += ",80,60";
	}

	if(i > 1) {
		buffer += " -d";
		try {
			interpreter.run(buffer.c_str(), images, names);
		} catch (gmic_exception &e) {
			fprintf(stderr,"ERROR: %s\n", e.what());
		}
	}

	while(!cin.eof()) {
		cout << "> ";
		getline(cin, buffer);
		try {
			interpreter.run(buffer.c_str(), images, names);
		} catch (gmic_exception &e) {
			fprintf(stderr,"ERROR: %s\n", e.what());
		}
	}
}

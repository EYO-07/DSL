#include <iostream>
#include <string>
#include <vector>
#include <filesystem>

namespace fs = std::filesystem;

void displayMessage() {
    std::cout << "[ File Map ]\n";
    std::cout << "1. exit : exit the application\n";
    std::cout << "write a file extension beginning with '.'\n";
}

void processInput(const std::string& input, std::vector<std::string>& files) {
    if (input == "exit") {
        std::cout << "Exiting application.\n";
        exit(0);
    }
    else if (input == "show") {
        if (files.size() > 0) {
            std::cout << "Stored files:\n";
            for (const auto& file : files) {
                std::cout << file << "\n";
            }
        }
        else {
            std::cout << "No files stored yet.\n";
        }
    }
    else if (!input.empty() && input[0] == '.' && input.length() > 1) {
        files.clear(); // Clear previous results
        std::string extension = input;
        try {
            for (const auto& entry : fs::recursive_directory_iterator(".")) {
                if (entry.is_regular_file() && entry.path().extension() == extension) {
                    files.push_back(entry.path().string());
                }
            }
            std::cout << "Found " << files.size() << " files with extension " << extension << ".\n";
        }
        catch (const fs::filesystem_error& e) {
            std::cout << "Error accessing filesystem: " << e.what() << "\n";
        }
    }
    else {
        std::cout << "Invalid input. Try 'exit', 'show', or a file extension like '.txt'.\n";
    }
}

int main() {
    std::vector<std::string> files; // Declare the string vector "files"
    std::string input;

    while (true) { // Main loop
        displayMessage();
        std::cout << "> ";
        std::getline(std::cin, input);
        processInput(input, files);
        std::cout << "\n";
    }

    return 0;
}
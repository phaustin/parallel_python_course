#include <mutex>
#include <iostream>
#include <chrono>
#include <thread>

std::mutex mutex;

void my_thread() {
    int counter = 100;
    while (counter--) {
        std::lock_guard<std::mutex> lg(mutex);
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        std::cout << "." << std::flush;
    }
}

int main (int argc, char *argv[]) {
    std::thread t1(my_thread);
    auto start = std::chrono::system_clock::now();
    // added sleep to ensure that the other thread locks lock first
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    {
        std::lock_guard<std::mutex> lg(mutex);
        auto end = std::chrono::system_clock::now();
        auto diff = end - start;
        std::cout << "Took me " << diff.count() << std::endl;
    }
    t1.join();
    return 0;
};

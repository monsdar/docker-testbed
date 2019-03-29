
#include <concatlib/generator.h>
#include <leetlib/generator.h>

#include <iostream>

int main()
{
    ConcatGenerator concat;
    LeetGenerator leet;
    
    std::cout << "Concat: " << concat.generate() << std::endl;
    std::cout << "Leet: " << leet.generate() << std::endl;
    
    return 0;
}

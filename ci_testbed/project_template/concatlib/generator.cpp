
#include "concatlib/generator.h"

#include <hellolib/generator.h>
#include <foobarlib/generator.h>

std::string ConcatGenerator::generate()
{
    HelloGenerator hello;
    FoobarGenerator foobar;
    
    return hello.generate() + foobar.generate();
}

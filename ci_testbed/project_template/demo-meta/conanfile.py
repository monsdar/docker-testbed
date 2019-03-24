from conans import ConanFile, CMake

class MetaConan(ConanFile):
    name = "demo-meta"
    version = "1.0.0"
    generators = "cmake", "virtualrunenv"

    def requirements(self):
        self.requires.add("foobarlib/HEAD@demo/release")
        self.requires.add("hellolib/HEAD@demo/release")
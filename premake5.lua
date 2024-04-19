workspace "SampleSelection"
    architecture "x64"
    startproject "SampleSelection"
    configurations { 
        "Debug", 
        "Release" 
    }

    IncDir = {}
    IncDir["glfw"] = "3rdparty/glfw/include"
    IncDir["glad"] = "3rdparty/glad/include"
    IncDir["glm"] = "3rdparty/glm"
    IncDir["stb"] = "3rdparty/stb"

    group "3rdparty"
    include "3rdparty/glfw"
    include "3rdparty/glad"
    group ""

    project "SampleSelection"
        kind "ConsoleApp"
        language "C++"
        cppdialect "C++17"
        targetdir "bin/%{prj.name}/%{cfg.buildcfg}"
        objdir "obj/%{prj.name}/%{cfg.buildcfg}"

        links {
            "glad",
            "glfw",
            "opengl32.lib"
        }

        includedirs {
            "%{IncDir.glfw}",
            "%{IncDir.glad}",
            "%{IncDir.glm}",
            "%{IncDir.stb}",
            "src",
        }

        files { 
            "src/**.cpp",
            "src/**.hpp"
        }

        filter "system:windows"
            staticruntime "on"
            systemversion "latest"

        filter "configurations:Debug"
            symbols "on"

        filter "configurations:Release"
            optimize "on"
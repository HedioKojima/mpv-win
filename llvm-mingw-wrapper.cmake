foreach(compiler clang++ g++ c++ clang gcc as)
    set(driver_mode "")
    set(clang_compiler "")
    set(linker "")

    if (compiler STREQUAL "g++" OR compiler STREQUAL "c++")
        set(driver_mode "--driver-mode=g++ -pthread")
        set(clang_compiler "clang++")
    elseif(compiler STREQUAL "clang++")
        set(driver_mode "--driver-mode=g++")
        set(clang_compiler "clang++")
        set(linker "-lc++abi")
    else()
        set(driver_mode "")
        set(clang_compiler "clang")
    endif()
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/llvm-compiler.in
                   ${LLVM_LOCATION}/bin/${TARGET_ARCH}-${compiler}
                   FILE_PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
                   @ONLY)
endforeach()

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/llvm-ld.in
               ${LLVM_LOCATION}/bin/${TARGET_ARCH}-ld
               FILE_PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
               @ONLY)

# llvm-mingw ships no libstdc++, but CMake/meson-generated pkg-config files
# (uchardet, ffmpeg's gfxcapture filter, ...) still emit "-lstdc++". lld maps
# -lstdc++ to -lc++ and prefers "libc++.dll.a" over static "libc++.a" when
# searching, which would silently pull the C++ runtime dynamically on top of
# the static copy and fail with duplicate symbols. Alias -lstdc++ to the
# static libc++ so every occurrence resolves inside the sysroot.
if(EXISTS "${MINGW_INSTALL_PREFIX}/lib/libc++.a" AND NOT EXISTS "${MINGW_INSTALL_PREFIX}/lib/libstdc++.a")
    file(CREATE_LINK "${MINGW_INSTALL_PREFIX}/lib/libc++.a"
                     "${MINGW_INSTALL_PREFIX}/lib/libstdc++.a" SYMBOLIC)
endif()

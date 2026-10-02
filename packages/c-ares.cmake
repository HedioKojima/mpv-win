ExternalProject_Add(c-ares
    GIT_REPOSITORY https://github.com/c-ares/c-ares.git
    SOURCE_DIR ${SOURCE_LOCATION}
    GIT_CLONE_FLAGS "--filter=tree:0"
    UPDATE_COMMAND ""
    GIT_REMOTE_NAME origin
    GIT_TAG main
    CONFIGURE_COMMAND ${EXEC} CONF=1 cmake -B <BINARY_DIR> -S <SOURCE_DIR>
        -G Ninja
        -DCMAKE_BUILD_TYPE=Release
        -DCMAKE_TOOLCHAIN_FILE=${TOOLCHAIN_FILE}
        -DCMAKE_INSTALL_PREFIX=${MINGW_INSTALL_PREFIX}
        -DBUILD_SHARED_LIBS=OFF
        -DCARES_BUILD_TESTS=OFF
        -DCARES_BUILD_TOOLS=OFF
        -DCARES_INSTALL=ON
        -DCARES_SHARED=OFF
        -DCARES_STATIC=ON
        -DCARES_THREADS=ON
    BUILD_COMMAND ${EXEC} ninja
    INSTALL_COMMAND ${EXEC} ninja install
    LOG_DOWNLOAD 1 LOG_UPDATE 1 LOG_CONFIGURE 1 LOG_BUILD 1 LOG_INSTALL 1
)

force_rebuild_git(c-ares)
cleanup(c-ares install)

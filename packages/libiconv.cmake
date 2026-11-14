ExternalProject_Add(libiconv
    URL https://www.mirrorservice.org/sites/ftp.gnu.org/gnu/libiconv/libiconv-1.19.1.tar.gz
    URL_HASH SHA256=9a06844846d664d7122161700c10a64480d7c7bcead3091925a785b38c91edab
    DOWNLOAD_DIR ${SOURCE_LOCATION}
    CONFIGURE_COMMAND ${EXEC} CONF=1 <SOURCE_DIR>/configure
        --host=${TARGET_ARCH}
        --prefix=${MINGW_INSTALL_PREFIX}
        --disable-nls
        --disable-shared
        --enable-extra-encodings
    BUILD_COMMAND ${MAKE}
    INSTALL_COMMAND ${MAKE} install
    LOG_DOWNLOAD 1 LOG_UPDATE 1 LOG_CONFIGURE 1 LOG_BUILD 1 LOG_INSTALL 1
)

cleanup(libiconv install)

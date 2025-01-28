HOMEPAGE = "https://pypi.org/project/aiomqtt/"
SUMMARY = "The idiomatic asyncio MQTT client"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a462083fa4d830bdcf8c22a8ddf453cf"

inherit pypi python_poetry_core


SRC_URI[sha256sum] = "312feebe20bc76dc7c20916663011f3bd37aa6f42f9f687a19a1c58308d80d47"

PYPI_PACKAGE = "aiomqtt"

BBCLASSEXTEND = "native nativesdk"

PROVIDE = "python3-aiomqtt"

# RDEPENDS:${PN} += " python3-logging"

DEPENDS += " python3-build python3-poetry-core python3-poetry-dynamic-versioning"

FROM python:3.11-bookworm as build


#The application name for the installation dir
ARG APP_NAME

#The package names to install. This can be multiple packages but need to be space separated
ARG PYTHON_PACKAGE_NAMES

# Disable Python STDOUT and STDERROR message buffering
ENV PYTHONUNBUFFERED=1

# Create a Python VENV to protect the application from Python system packages and settings
# This is best practice even when using containers

# By using the PYTHON_VIRTUAL_ENV name for the variable
# Python and 3th party tools know that a venv is used
ENV PYTHON_VIRTUAL_ENV=/opt/${APP_NAME}/venv
RUN python -m venv ${PYTHON_VIRTUAL_ENV}

# Now add add the Python venv binary to the PATH variable in first path position
# This will ensure the venv Python is the preffered Python binary
# This has the same effect as activating a venv
ENV PATH="${PYTHON_VIRTUAL_ENV}/bin:${PATH}"

# Install the Python packages in the VENV
RUN pip install ${PYTHON_PACKAGE_NAMES} --no-cache

FROM python:3.11-slim-bookworm as runtime
# Switching to the slim final runtime image
# No builds or installations in this image
# All ENVs in this image will be distributed!

# Arguments for setting container image labels
ARG APP_DESCRIPTION
ARG APP_LICENSE
ARG APP_MAINTAINER
ARG APP_NAME
ARG APP_TITLE
ARG APP_VCS_COMMIT_HASH
ARG APP_VCS_URL
ARG APP_VENDOR
ARG APP_VERSION
ARG IMAGE_BUILD_DATETIME

# The binary to launch the app and the launch arguments
ARG APP_BIN_NAME
ARG APP_BIN_ARGS
ARG APP_BIN_PORT
ARG RUNTIME_USERNAME


# Copy the ARGs to ENVs. The ARGs are needed for supporting build variables.
# The ENVs are needed because we need to make sure that these build variables are available at container runtime.
ENV APP_BIN_NAME=${APP_BIN_NAME}
ENV APP_BIN_ARGS=${APP_BIN_ARGS}


# Disable Python STDOUT and STDERROR message buffering
ENV PYTHONUNBUFFERED=1

#Set the Python virtual environment
ENV PYTHON_VIRTUAL_ENV=/opt/${APP_NAME}/venv
ENV PATH="${PYTHON_VIRTUAL_ENV}/bin:${PATH}"

# Copy the Python files from the builder image
COPY --from=build ${PYTHON_VIRTUAL_ENV} ${PYTHON_VIRTUAL_ENV}

# Create a nonpriv user and group called $RUNTIME_USERNAME
# Set readonly permissions for the $RUNTIME_USERNAME on the application directory
# This prevents exploits like priv escallations or changing source files
# This does mean that we should run on an port number higher then 1024 because we are non root
RUN groupadd -r ${RUNTIME_USERNAME} &&  \
    useradd -r -g ${RUNTIME_USERNAME} ${RUNTIME_USERNAME} && \
    chmod 550 -R ${PYTHON_VIRTUAL_ENV} &&  \
    chown -R ${RUNTIME_USERNAME}:${RUNTIME_USERNAME} ${PYTHON_VIRTUAL_ENV}

# Switch to the non priv runtime user
USER ${RUNTIME_USERNAME}

# Switch the WORKDIR to the VENV to ensure we have a known location where the user has permissions
WORKDIR ${PYTHON_VIRTUAL_ENV}

# Start the BIN at runtime
CMD $(echo ${APP_BIN_NAME} ${APP_BIN_ARGS})

# Lets make our image better than other open source projects and set some labels :)
# Using https://github.com/opencontainers/image-spec/blob/main/annotations.md for needed labels
LABEL maintainer = ${APP_MAINTAINER}
LABEL org.opencontainers.image.authors = ${APP_MAINTAINER}
LABEL org.opencontainers.image.created = ${IMAGE_BUILD_DATETIME}
LABEL org.opencontainers.image.description = ${APP_DESCRIPTION}
LABEL org.opencontainers.image.documentation = ${APP_VCS_URL}
LABEL org.opencontainers.image.licenses = ${APP_LICENSE}
LABEL org.opencontainers.image.name = ${APP_NAME}
LABEL org.opencontainers.image.revision = ${APP_VCS_COMMIT_HASH}
LABEL org.opencontainers.image.source = ${APP_VCS_URL}
LABEL org.opencontainers.image.title = ${APP_TITLE}
LABEL org.opencontainers.image.url = ${APP_VCS_URL}
LABEL org.opencontainers.image.vendor = ${APP_VENDOR}
LABEL org.opencontainers.image.version = ${APP_VERSION}

FROM python:3.11-bookworm as build


#The application name for the installation dir
ARG APP_NAME

#The package names to install. This can be multiple packages but need to be space separated
ARG PYTHON_PACKAGE_NAMES

# Disable Python STDOUT and STDERROR message buffering
ENV PYTHONUNBUFFERED=1

# Create a Python VENV to protect the application from Python system packages and settings
# This is best practice even when using containers

# By using the VIRTUAL_ENV name for the variable
# Python and 3th party tools know that a venv is used
ENV VIRTUAL_ENV=/opt/${APP_NAME}/venv
RUN python -m venv ${VIRTUAL_ENV}

# Now add add the Python venv binary to the PATH variable in first path position
# This will ensure the venv Python is the preffered Python binary
# This has the same effect as activating a venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Install the Python packages in the VENV
RUN pip install ${PYTHON_PACKAGE_NAMES}

FROM python:3.11-slim-bookworm as runtime
# Switching to the slim final runtime image
# No builds or installations in this image
# All ENVs in this image will be distributed!

# Lets make our image better than other open source project and set labels :)
LABEL maintainer="arnoud@famstolk.com"

#The application name for the installation dir
ARG APP_NAME

# The binary to start and the arguments
ARG APP_BIN_NAME
ARG APP_BIN_ARGS

# Copy the ARGs to ENVs. The ARGs are needed for supporting build variables.
# The ENVs are needed because we need to make sure that the ARG build variables are available at runtime.
ENV APP_BIN_NAME=${APP_BIN_NAME}
ENV APP_BIN_ARGS=${APP_BIN_ARGS}

# The user that runs the APP
ARG APP_USERNAME

# Disable Python STDOUT and STDERROR message buffering
ENV PYTHONUNBUFFERED=1

#Set the Python virtual environment
ENV VIRTUAL_ENV=/opt/${APP_NAME}/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy the Python files from the builder image
COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Create a nonpriv user and group called $APP_USERNAME
# Set readonly permissions for the $APP_USERNAME on the application directory
# This prevents exploits like priv escallations or changing source files
# This does mean that we should run on an port number higher then 1024 because we are non root
RUN groupadd -r ${APP_USERNAME} && useradd -r -g ${APP_USERNAME} ${APP_USERNAME}
RUN chmod 550 -R ${VIRTUAL_ENV} && chown -R ${APP_USERNAME}:${APP_USERNAME} ${VIRTUAL_ENV}

# Switch to the non priv user
USER ${APP_USERNAME}

# Switch the WORKDIR to the VENV to ensure we have a know location the user has permissions
WORKDIR ${VIRTUAL_ENV}

# Start the BIN
CMD $(echo ${APP_BIN_NAME} ${APP_BIN_ARGS})
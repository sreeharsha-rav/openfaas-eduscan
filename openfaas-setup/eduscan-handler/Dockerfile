# Define global args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.8"

# Stage 1 - Use the openfaas/classic-watchdog as the base image
FROM ghcr.io/openfaas/classic-watchdog:0.2.3 as watchdog

# Stage 2 - bundle base image + runtime
FROM python:${RUNTIME_VERSION} as python-alpine

# Install necessary packages
RUN apt-get update \
    && apt-get install -y cmake ca-certificates libgl1-mesa-glx ffmpeg \
    && python${RUNTIME_VERSION} -m pip install --upgrade pip

# Stage 3 - make minimal runtime image
FROM python:${RUNTIME_VERSION} as builder

# include global arg in this stage of the build
ARG FUNCTION_DIR
ARG RUNTIME_VERSION

# Create function directory
RUN mkdir -p ${FUNCTION_DIR}
# Set the working directory to the location of our code
WORKDIR ${FUNCTION_DIR}

# install necessary packages
COPY requirements.txt ${FUNCTION_DIR}
RUN python${RUNTIME_VERSION} -m pip install --no-cache-dir -r requirements.txt --target ${FUNCTION_DIR}

# Copy function code
COPY handler.py ${FUNCTION_DIR}
COPY face_recognition_module.py ${FUNCTION_DIR}
COPY processVideo_module.py ${FUNCTION_DIR}
COPY helper_functions.py ${FUNCTION_DIR}
COPY encoding ${FUNCTION_DIR}

# Stage 4 - Final stage
FROM python-alpine

# include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy the watchdog binary from the first stage
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
# Make the watchdog executable
RUN chmod +x /usr/bin/fwatchdog

# Copy the built function code from the builder stage
COPY --from=builder ${FUNCTION_DIR} ${FUNCTION_DIR}

# move to function directory
WORKDIR ${FUNCTION_DIR}

# Set the fprocess environment variable to be the entrypoint for the container
ENV fprocess="python handler.py"
# Set to true to see request in function logs
ENV write_debug="false"

# Expose port 8080 to external traffic
EXPOSE 8080
# Healthcheck interval
HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1
# Start watchdog
CMD ["fwatchdog"]

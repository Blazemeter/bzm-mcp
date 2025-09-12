# Copyright 2025 BlazeMeter author
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:24.04


WORKDIR /app

# Update system packages for security patches
RUN apt-get update -y && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

ARG TARGETPLATFORM

# Copy all pre-built binaries
COPY dist/ ./dist/

# Select and copy the appropriate binary based on target platform
RUN case "${TARGETPLATFORM}" in \
    "linux/amd64") cp ./dist/bzm-mcp-linux-amd64 ./bzm-mcp ;; \
    "linux/arm64") cp ./dist/bzm-mcp-linux-arm64 ./bzm-mcp ;; \
    *) echo "Unsupported platform: ${TARGETPLATFORM}. Supported: linux/amd64, linux/arm64" && exit 1 ;; \
    esac && \
    echo "Selected binary for platform: ${TARGETPLATFORM}" && \
    rm -rf ./dist/

    
RUN chmod +x ./bzm-mcp && \
    chown appuser:appgroup ./bzm-mcp

# Switch to non-root user
USER appuser

# Command to run the application
ENTRYPOINT ["./bzm-mcp"]


# For NVIDIA image from dockerhub, but currently using nvcr.io
# ARG UBUNTU_VERSION="22.04"
# ARG CUDA_VERSION="12.1.1"
# ARG CUDNN_VERSION="8.9.2.26"
# ARG CUDNN_V="8"
# ARG PYTHON_VERSION="3.11"

# FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_V}-devel-ubuntu${UBUNTU_VERSION} AS base
FROM nvcr.io/nvidia/pytorch:24.09-py3 as base

# For coder
USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    jq \
    sudo \
    && rm -rf /var/lib/apt/lists/*

ARG DEBIAN_FRONTEND=noninteractive

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt update &&  \
#     apt -y install --no-install-recommends <your-package-list-here>

# Do NOT modify UID from 1000
# vscode updates this UID to the user building the container
# ARG USERNAME=developer
ARG USERNAME=coder
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt update \
    && apt install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Cleanup
# RUN pip3 cache purge # cache is not enabled in the nvcr image
RUN apt autoremove -y
RUN apt clean

USER $USERNAME

# Allow container to stop. See: https://github.com/microsoft/vscode-remote-release/issues/3512#issuecomment-1267053890
# NOTE: May affect benchmarking
# NOTE: Long interval is necessary so container is not closed during vscode initialization
CMD while sleep 120 && ps aux | egrep 'vscode.*[b]ootstrap-fork.*extensionHost.*' > /dev/null; do :; done
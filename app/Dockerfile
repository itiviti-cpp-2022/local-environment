FROM dokken/ubuntu-20.04:latest

LABEL maintainer="renbou"

# Like in workflow
RUN apt update
RUN a./runpt install -y \
      clang-tidy-10; \
    sudo update-alternatives --install \
      /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-10 100;

# Install clang, cmake for compiling and using ICA
RUN apt install clang cmake -y

# Make clang the default compiler
RUN update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++-10 60
RUN update-alternatives --install /usr/bin/cc cc /usr/bin/clang-10 60

RUN mkdir /env
WORKDIR /env

COPY app/libica-plugin.so .
COPY app/app.sh .

ENV REPO_PATH {{container_repo_path}}

ENTRYPOINT ["bash", "app.sh"]

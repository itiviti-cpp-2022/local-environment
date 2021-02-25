FROM dokken/ubuntu-20.04:latest

LABEL maintainer="renbou"

# Like in workflow
RUN sudo apt-get install -y \
      clang-tidy-10; \
    sudo update-alternatives --install \
      /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-10 100;

# Install clang, cmake for compiling and using ICA
RUN apt install clang cmake -y

RUN mkdir /env
WORKDIR /env

COPY app/libica-plugin.so .
COPY app/app.sh .

ENV REPO_PATH {{container_repo_path}}

ENTRYPOINT ["bash", "app.sh"]